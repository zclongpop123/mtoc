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
