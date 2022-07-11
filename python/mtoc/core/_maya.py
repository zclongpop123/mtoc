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
EXPORT_ARGS   = '-stripNamespaces -uvWrite -writeUVSets -writeFaceSets -worldSpace -writeVisibility -dataFormat ogawa'

def export_alembic(_abc):
    '''
    '''
    if not mc.pluginInfo('AbcExport.mll', q=True, loaded=True):
        try:
            mc.loadPlugin('AbcExport.mll', quiet=True)
        except:
            return False

    export_objects = mc.ls(assemblies=True)
    for cam in ['persp', 'top', 'front', 'side']:
        export_objects.remove(cam)

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

    mel.eval(export_cmds)



def get_ai_tex_data(shader):
    '''
    '''
    data = dict()
    for attr in env.MAYA_CLA_ATTR_MAPPING.keys():
        attr_pml_node = pm.PyNode('{0}.{1}'.format(shader, attr))
        attr_api_node = attr_pml_node.__apiobject__()
        iterator = OpenMaya.MItDependencyGraph(attr_api_node, 
                                               OpenMaya.MFn.kFileTexture, 
                                               OpenMaya.MItDependencyGraph.kUpstream,
                                               OpenMaya.MItDependencyGraph.kDepthFirst,
                                               OpenMaya.MItDependencyGraph.kPlugLevel)

        while not iterator.isDone():
            file_api_mfn  = OpenMaya.MFnDependencyNode(iterator.currentItem())
            file_api_plug = file_api_mfn.findPlug('ftn')
            data.setdefault('{0}.{1}'.format(shader, attr), file_api_plug.asString())
            iterator.next()

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



def get_all_tex_data():
    '''
    '''
    data = dict()
    for shd in mc.ls(typ='aiStandardSurface'):
        sg = list(get_ai_shading_group(shd))
        data.setdefault(sg[0], dict())[shd] = get_ai_tex_data(shd)
    return data



def export_tex_data(_json):
    '''
    '''
    with open(_json, 'w') as f:
        json.dump(get_all_tex_data(), f, indent=4)
    return True
