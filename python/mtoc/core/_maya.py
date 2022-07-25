#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Fri Jul  1 14:18:26 2022
#========================================
import json
import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import maya.OpenMaya as OpenMaya
from .. import env
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
EXPORT_ARGS   = '-stripNamespaces -uvWrite -writeVisibility -eulerFilter -writeUVSets -writeFaceSets -worldSpace -dataFormat ogawa'

def export_alembic(_abc):
    '''
    '''
    if not mc.pluginInfo('AbcExport.mll', q=True, loaded=True):
        try:
            mc.loadPlugin('AbcExport.mll', quiet=True)
        except:
            return False

    export_objects = mc.ls(sl=True)
    if not export_objects:
        return

    start_frame = int(mc.currentTime(q=True))
    end_frame   = int(mc.currentTime(q=True))

    export_cmds = 'AbcExport'

    cache_file = _abc.replace('\\', '/')
    export_cmds += ' -j "-frameRange {0} {1} {2} -root {3} -file {4}"'.format(start_frame,
                                                                              end_frame, 
                                                                              EXPORT_ARGS, 
                                                                              ' -root '.join(export_objects), 
                                                                              cache_file)

    for sg in mc.ls(typ='shadingEngine'):
        members = mc.sets(sg, q=True)
        if not members:
            continue
        members.extend(['{0}.f[:]'.format(s) for s in members if '.' not in s])

        for m in members:
            if '.' not in m:
                mc.sets(m, e=True, remove=sg)
            else:
                mc.sets(m, e=True, forceElement=sg)

    mel.eval(export_cmds)



def get_ai_tex_data(shader):
    '''
    '''
    data = dict()
    shader_type = mc.nodeType(shader)
    data['type'] = shader_type
    for attr in env.MAYA_CLA_ATTR_MAPPING.get(shader_type, dict()).keys():
        attr_pml_node = pm.PyNode('{0}.{1}'.format(shader, attr))
        attr_api_node = attr_pml_node.__apiobject__()
        iterator = OpenMaya.MItDependencyGraph(attr_api_node, 
                                               OpenMaya.MFn.kDependencyNode, 
                                               OpenMaya.MItDependencyGraph.kUpstream,
                                               OpenMaya.MItDependencyGraph.kDepthFirst,
                                               OpenMaya.MItDependencyGraph.kPlugLevel)

        while not iterator.isDone():
            file_api_mfn  = OpenMaya.MFnDependencyNode(iterator.currentItem())
            if file_api_mfn.typeName() == 'file':
                file_api_plug = file_api_mfn.findPlug('ftn')
                data.setdefault('{0}.{1}'.format(shader, attr), dict())['path'] = file_api_plug.asString()
            elif file_api_mfn.typeName() == 'RedshiftNormalMap':
                file_api_plug = file_api_mfn.findPlug('tex0')
                data.setdefault('{0}.{1}'.format(shader, attr), dict())['path'] = file_api_plug.asString()                
            iterator.next()

        #- 0: bump
        #- 1: normal
        bump_node_type = [x.nodeType() for x in attr_pml_node.connections()]
        if 'aiBump2d' in bump_node_type:
            data.setdefault('{0}.{1}'.format(shader, attr), dict())['bumpInterp'] = 0

        elif 'aiNormalMap' in bump_node_type:
            data.setdefault('{0}.{1}'.format(shader, attr), dict())['bumpInterp'] = 1

        elif 'RedshiftBumpMap' in bump_node_type:
            data.setdefault('{0}.{1}'.format(shader, attr), dict())['bumpInterp'] = attr_pml_node.connections()[0].attr('inputType').get()

        elif 'RedshiftNormalMap' in bump_node_type:
            data.setdefault('{0}.{1}'.format(shader, attr), dict())['bumpInterp'] = 1

        elif 'bump2d' in bump_node_type:
            data.setdefault('{0}.{1}'.format(shader, attr), dict())['bumpInterp'] = attr_pml_node.connections()[0].attr('bumpInterp').get()

    return data



def get_ai_shading_group(shader):
    '''
    '''
    attr_pml_node = pm.PyNode(shader)
    attr_api_node = attr_pml_node.__apiobject__()
    iterator = OpenMaya.MItDependencyGraph(attr_api_node, 
                                           OpenMaya.MFn.kShadingEngine, 
                                           OpenMaya.MItDependencyGraph.kDownstream)

    while not iterator.isDone():
        yield OpenMaya.MFnDependencyNode(iterator.currentItem()).name()
        iterator.next()



def get_sg_displace(sg):
    '''
    '''
    attr_pml_node = pm.PyNode('{0}.displacementShader'.format(sg))
    attr_api_node = attr_pml_node.__apiobject__()    
    iterator = OpenMaya.MItDependencyGraph(attr_api_node, 
                                           OpenMaya.MFn.kFileTexture, 
                                           OpenMaya.MItDependencyGraph.kUpstream,
                                           OpenMaya.MItDependencyGraph.kDepthFirst,
                                           OpenMaya.MItDependencyGraph.kPlugLevel)

    while not iterator.isDone():
        file_api_mfn  = OpenMaya.MFnDependencyNode(iterator.currentItem())
        file_api_plug = file_api_mfn.findPlug('ftn')
        yield file_api_plug.asString()
        iterator.next()



def get_all_tex_data():
    '''
    '''
    data = dict()
    for shd in mc.ls(typ=('aiStandardSurface', 'RedshiftMaterial')):
        sg = list(get_ai_shading_group(shd))
        data.setdefault(sg[0], dict()).setdefault('shader', dict())[shd] = get_ai_tex_data(shd)
        data.setdefault(sg[0], dict())['displacement']  = list(get_sg_displace(sg[0]))
    return data



def export_tex_data(_json):
    '''
    '''
    with open(_json, 'w') as f:
        json.dump(get_all_tex_data(), f, indent=4)
    return True
