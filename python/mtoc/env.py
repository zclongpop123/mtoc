#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Fri Jul  1 14:48:26 2022
#========================================
import os
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
TEX_TEMP_PATH = os.path.expanduser('~/mtoc_tex.json').replace('\\', '/').replace('/Documents/', '/')

MAYA_CLA_ATTR_MAPPING = {
    'baseColor'         : 'base_color',
    'normalCamera'      : 'normal_input',
    'specularRoughness' : 'specular_roughness'
}
