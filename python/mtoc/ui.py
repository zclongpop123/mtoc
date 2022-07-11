#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Fri Jul  1 14:48:35 2022
#========================================
import os
import maya.cmds as mc
import maya.OpenMayaUI as OpenMayaUI
from PySide2 import QtWidgets, QtCore
import shiboken2
from . import widgets, core
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def get_maya_window():
    '''
    '''
    maya_window = OpenMayaUI.MQtUtil.mainWindow()
    if maya_window:
        return shiboken2.wrapInstance(int(maya_window), QtWidgets.QMainWindow)




class MtoCUI(QtWidgets.QMainWindow, widgets.Ui_MainWindow):
    '''
    '''
    def __init__(self, parent=None):
        super(MtoCUI, self).__init__(parent)
        self.setupUi(self)



    @QtCore.Slot(bool)
    def on_btn_export_clicked(self, args):
        '''
        '''
        output_file = mc.fileDialog2(fm=0, ff='Alembic(*.abc);;Json File(*.json);;')
        if not output_file:
            return
        file_prefix = os.path.splitext(output_file[0])[0]

        if self.cbx_exp_abc.isChecked():
            abc_path = '{0}.abc'.format(file_prefix)
        else:
            abc_path = None

        if self.cbx_exp_json.isChecked():
            json_path = '{0}.json'.format(file_prefix)
        else:
            json_path = None

        core.export_data(abc_path, json_path)



    @QtCore.Slot(bool)
    def on_btn_import_clicked(self, args):
        '''
        '''
        print(2)



def main():
    '''
    '''
    wnd = MtoCUI(get_maya_window())
    wnd.show()



if __name__ == '__main__':
    main()
