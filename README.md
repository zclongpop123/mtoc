#------------------------------------------------------------
import sys

path = 'D:/work/mtoc/python'
path in sys.path or sys.path.append(path)


from mtoc.core import _maya
_maya.export_tex_data()

#------------------------------------------------------------
import sys

path = 'D:/work/mtoc/python'
path in sys.path or sys.path.append(path)

from mtoc.core import _clarisse
_clarisse.create_tex_network()
