#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Fri Jul  1 14:47:27 2022
#========================================
import os
import json
import ix
from .. import env
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def read_tex_data():
    '''
    '''
    if not os.path.exists(env.TEX_TEMP_PATH):
        return dict()

    with open(env.TEX_TEMP_PATH, 'r') as f:
        return json.load(f)



def create_tex_network():
    '''
    '''
    data = read_tex_data()
    for shd, textures in data.items():
        shader_node = ix.cmds.CreateObject(shd, 'MaterialPhysicalAutodeskStandardSurface', 'Global', 'build://project/scene')

        for attr, _map in textures.items():
            _cla_attr = env.MAYA_CLA_ATTR_MAPPING.get(attr.split('.')[-1])
            if not _cla_attr:
                continue
            map_node = ix.cmds.CreateObject(attr.replace('.', '__'), 'TextureMapFile', 'Global', 'build://project/scene')
            ix.cmds.SetValues(['{0}.filename[0]'.format(map_node)], [_map])
            ix.cmds.SetTexture(['{0}.{1}'.format(shader_node, _cla_attr)], map_node)
