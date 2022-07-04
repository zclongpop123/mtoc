#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Fri Jul  1 14:18:26 2022
#========================================
import json
import maya.cmds as mc
import pymel.core as pm
import maya.OpenMaya as OpenMaya
from .. import env
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def get_ai_tex_data(shader):
    '''
    '''
    data = dict()
    for attr in ('baseColor', 'specularRoughness', 'opacity', 'normalCamera'):
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



def get_all_tex_data():
    '''
    '''
    data = dict()
    for shd in mc.ls(typ='aiStandardSurface'):
        data[shd] = get_ai_tex_data(shd)
    return data



def export_tex_data():
    '''
    '''
    with open(env.TEX_TEMP_PATH, 'w') as f:
        json.dump(get_all_tex_data(), f, indent=4)
    return True
