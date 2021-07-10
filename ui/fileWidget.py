import pathlib
from PyQt5 import uic
from PyQt5.Qt import *
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *
from ui.codeEdit import CodeEditor
from xast.syntaxtree import TreeBuilder
import json

_Ui, _UiBase = uic.loadUiType(
    pathlib.Path(__file__).with_name('fileWidget.ui'), resource_suffix='', import_from="ui"
)


class FileWidget(_UiBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rawData = []
        self.ast = None

        self.ui = _Ui()
        self.ui.setupUi(self)

        codeEdit = CodeEditor(self.ui.verticalLayout.parent())
        codeEdit.setLineWrapMode(self.ui.textEdit.lineWrapMode())
        codeEdit.setEnabled(self.ui.textEdit.isEnabled())
        codeEdit.setReadOnly(True)
        codeEdit.setFont(self.ui.textEdit.font())
        codeEdit.hihghlightColor = QColor(Qt.cyan).lighter(160)

        self.ui.verticalLayout.removeWidget(self.ui.textEdit)
        self.ui.textEdit = codeEdit
        self.ui.verticalLayout.insertWidget(1, self.ui.textEdit)

        self.ui.actionOpen.triggered.connect(self.__openFileDialog)
        self.ui.actionClear.triggered.connect(self.__clear)

    def __openFileDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        self.__readData(fname)
        self.__updateCodeEdit()

    def __clear(self):
        self.rawData = []
        self.ast = None
        self.__updateCodeEdit()

    def __updateCodeEdit(self):
        self.ui.textEdit.setPlainText(''.join(self.rawData))
        self.ui.textEdit.setEnabled(len(self.rawData) > 0)

    def __readData(self, filename):
        file = open(filename, 'r')
        self.rawData = file.readlines()
        file.close()
        with open('xast/weights.json') as json_file:
            weights = json.load(json_file)
        self.ast = TreeBuilder.build(self.rawData, weights)
        print(self.ast)

    def isLoaded(self):
        return self.ast is not None

    def setPlagiarized(self, plagiarized):
        back_color = QColor(Qt.red) if plagiarized else QColor(Qt.green)
        self.ui.textEdit.setBackgroundColor(back_color)
