#------------------------------------------------------------
import sys
import imp
path = 'D:/work/mtoc/python'
path in sys.path or sys.path.append(path)

from mtoc import ui
ui.main()


#------------------------------------------------------------
import sys

path = 'D:/work/mtoc/python'
path in sys.path or sys.path.append(path)

from mtoc.core import _clarisse
_clarisse.create_tex_network("D:/ball.json")
