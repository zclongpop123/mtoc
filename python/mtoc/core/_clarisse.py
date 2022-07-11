#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Fri Jul  1 14:47:27 2022
#========================================
import os
import re
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




def create_clarisse_hierarchy():
    '''
    '''
    factory = ix.application.get_factory()


    if not factory.item_exists('build://project/scene/mat'):
        ix.cmds.CreateContext('mat', 'Global', 'build://project/scene')

    if not factory.item_exists('build://project/scene/tex'):
        ix.cmds.CreateContext('tex', 'Global', 'build://project/scene')



def create_tex_network():
    '''
    '''
    factory = ix.application.get_factory()

    create_clarisse_hierarchy()
    data = read_tex_data()
    for shd, textures in data.items():
        if not factory.item_exists('build://project/scene/mat/{0}'.format(shd)):
            shader_node = ix.cmds.CreateObject(shd, 'MaterialPhysicalAutodeskStandardSurface', 'Global', 'build://project/scene/mat')

        for attr, _map in textures.items():
            _cla_attr = env.MAYA_CLA_ATTR_MAPPING.get(attr.split('.')[-1])
            if not _cla_attr:
                continue
            if not factory.item_exists('build://project/scene/tex/{0}'.format(attr.replace('.', '__'))):
                map_node = ix.cmds.CreateObject(attr.replace('.', '__'), 'TextureMapFile', 'Global', 'build://project/scene/tex')
                ix.cmds.SetValues(['{0}.filename[0]'.format(map_node)],  [_map])

                if _cla_attr == 'specular_roughness':
                    ix.cmds.SetValues(['{0}.single_channel_file_behavior'.format(map_node)],  ['1'])
                    ix.cmds.SetValues(['{0}.use_raw_data'.format(map_node)],                  ['1'])

                elif _cla_attr == 'normal_input':
                    ix.cmds.SetValues(['{0}.use_raw_data'.format(map_node)],                  ['1'])
                    if re.search('normal\.', _map, re.I):
                        normal_map = ix.cmds.CreateObject('normal_map', 'TextureNormalMap', 'Global', 'build://project/scene/tex')
                    elif re.search('bump\.', _map, re.I):
                        normal_map = ix.cmds.CreateObject('bump_map',   'TextureBumpMap',   'Global', 'build://project/scene/tex')
                    else:
                        normal_map = ix.cmds.CreateObject('dot',        'NodalItemDot',     'Global', 'build://project/scene/tex')

                    ix.cmds.SetTexture(['{0}.input'.format(normal_map)], map_node)
                    ix.cmds.SetTexture(['{0}.{1}'.format(shader_node, _cla_attr)], normal_map)
                    continue

                #-
                ix.cmds.SetTexture(['{0}.{1}'.format(shader_node, _cla_attr)], map_node)
