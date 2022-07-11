#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Fri Jul  1 14:46:01 2022
#========================================
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def export_data(_abc=None, _json=None):
    '''
    '''
    from . import _maya
    if _abc:
        _maya.export_alembic(_abc)
    if _json:
        _maya.export_tex_data(_json)
