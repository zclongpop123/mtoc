#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Fri Jul  1 14:48:26 2022
#========================================
import os
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
TEX_TEMP_PATH = os.path.expanduser('~/mtoc_tex.json').replace('\\', '/').replace('/Documents/', '/')

MAYA_CLA_ATTR_MAPPING = {
    'aiStandardSurface': {
        'baseColor'         : 'base_color',
        'metalness'         : 'metalness',
        'normalCamera'      : 'normal_input',
        'opacity'           : 'opacity',
        'specularRoughness' : 'specular_roughness'    
        },

    'RedshiftMaterial': {
        'diffuse_color'     : 'base_color',
        'bump_input'        : 'normal_input',
        'opacity_color'     : 'opacity',
        'refl_metalness'    : 'metalness',
        'refl_roughness'    : 'specular_roughness'    
    }
}
