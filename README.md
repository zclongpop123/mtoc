#------------------------------------------------------------
import sys

path = 'D:/work/mtoc/python'
path in sys.path or sys.path.append(path)

path_list = [
    'C:/Program Files/Python37/Lib/site-packages',
    'V:/pileline/packages/PySide2/xxx/xxx/xxx/xxx/python',
    'V:/pileline/packages/shiboken2/xxx/xxx/xxx/xxx/python',
]

for p in path_list:
    if p not in sys.path:
        sys.path.append(p)
		
import mtoc.ui
mtoc.ui.main()
