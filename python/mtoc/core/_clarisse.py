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
def refrence_abc(_abc):
    '''
    '''
    if os.path.isfile(_abc):
        ix.cmds.CreateFileReference("build://project/scene", [_abc])


def read_tex_data(_json):
    '''
    '''
    if not os.path.exists(_json):
        return dict()

    with open(_json, 'r') as f:
        return json.load(f)




def create_clarisse_hierarchy():
    '''
    '''
    factory = ix.application.get_factory()


    if not factory.item_exists('build://project/scene/mat'):
        ix.cmds.CreateContext('mat', 'Global', 'build://project/scene')

    if not factory.item_exists('build://project/scene/tex'):
        ix.cmds.CreateContext('tex', 'Global', 'build://project/scene')



def create_tex_network(_json):
    '''
    '''
    factory = ix.application.get_factory()

    create_clarisse_hierarchy()
    data = read_tex_data(_json)

    #-
    sg_list = list()
    object_list = ix.api.OfObjectArray()
    ix.application.get_factory().get_all_objects('GeometryAbcMesh', object_list)

    for i in range(object_list.get_count()):
        sg = object_list[i].get_module().get_geometry().get_shading_group_names()
        sg_list.extend([sg[j] for j in range(sg.get_count())])

    #- create dispalce
    for sg, sg_data in data.items():
        for dis in sg_data.get('displacement', list()):
            map_node = ix.cmds.CreateObject('displacement', 'TextureStreamedMapFile', 'Global', 'build://project/scene/tex')
            ix.cmds.SetValues(['{0}.use_raw_data'.format(map_node)], ['1'])
            ix.cmds.SetValues(['{0}.filename[0]'.format(map_node)],  [re.sub('\.\d{4}\.', '.<UDIM>.', dis)])

            dis_node = ix.cmds.CreateObject('{0}__displacement'.format(sg), 'Displacement', 'Global', 'build://project/scene/mat')
            ix.cmds.SetTexture(['{0}.front_value'.format(dis_node)], map_node)

    #- create shader
    shder_data = dict()
    for sg, _dt in data.items():
        if sg not in sg_list:
            continue
        shder_data.update(_dt.get('shader', dict()))

    for shd, shd_data in shder_data.items():
        if not factory.item_exists('build://project/scene/mat/{0}'.format(shd)):
            shader_node = ix.cmds.CreateObject(shd, 'MaterialPhysicalAutodeskStandardSurface', 'Global', 'build://project/scene/mat')

        for attr, attr_data  in shd_data.items():
            if attr in ('type', ):
                continue

            _cla_attr = env.MAYA_CLA_ATTR_MAPPING.get(shd_data.get('type', 'aiStandardSurface')).get(attr.split('.')[-1])
            if not _cla_attr:
                continue
            if not factory.item_exists('build://project/scene/tex/{0}'.format(attr.replace('.', '__'))):
                map_node = ix.cmds.CreateObject(attr.replace('.', '__'), 'TextureStreamedMapFile', 'Global', 'build://project/scene/tex')
                ix.cmds.SetValues(['{0}.filename[0]'.format(map_node)],  [re.sub('\.\d{4}\.', '.<UDIM>.', attr_data['path'])])

                if _cla_attr == 'specular_roughness':
                    ix.cmds.SetValues(['{0}.use_raw_data'.format(map_node)],                  ['1'])

                elif _cla_attr == 'metalness':
                    ix.cmds.SetValues(['{0}.use_raw_data'.format(map_node)],                  ['1'])

                elif _cla_attr == 'normal_input':
                    ix.cmds.SetValues(['{0}.use_raw_data'.format(map_node)],                  ['1'])
                    if attr_data.get('bumpInterp') == 0:
                        normal_map = ix.cmds.CreateObject('bump_map',   'TextureBumpMap',   'Global', 'build://project/scene/tex')
                    elif attr_data.get('bumpInterp') == 1:
                        normal_map = ix.cmds.CreateObject('normal_map', 'TextureNormalMap', 'Global', 'build://project/scene/tex')
                    else:
                        normal_map = ix.cmds.CreateObject('dot',        'NodalItemDot',     'Global', 'build://project/scene/tex')

                    ix.cmds.SetTexture(['{0}.input'.format(normal_map)], map_node)
                    ix.cmds.SetTexture(['{0}.{1}'.format(shader_node, _cla_attr)], normal_map)
                    continue

                #-
                ix.cmds.SetTexture(['{0}.{1}'.format(shader_node, _cla_attr)], map_node)

    #- assign shader
    object_list = ix.api.OfObjectArray()
    ix.application.get_factory().get_all_objects('GeometryAbcMesh', object_list)

    for i in range(object_list.get_count()):
        sg = object_list[i].get_module().get_geometry().get_shading_group_names()
        for j in range(sg.get_count()):
            shader = data.get(sg[j], dict()).get('shader')
            if not shader:
                continue
            ix.cmds.SetValues(['{0}.materials[{1}]'.format(object_list[i], j)],     ['build://project/scene/mat/{0}'.format(list(shader.keys())[0])])
            dis_mat = 'build://project/scene/mat/{0}__displacement'.format(sg[j])
            if factory.item_exists(dis_mat):
                ix.cmds.SetValues(['{0}.displacements[{1}]'.format(object_list[i], j)], [dis_mat])
