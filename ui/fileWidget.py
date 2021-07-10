import pathlib
from PyQt5 import uic
from PyQt5.Qt import *
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

from simple_comp.bow import BagOfWords
from ui.codeEdit import CodeEditor
from xast.syntaxtree import TreeBuilder
import json

_Ui, _UiBase = uic.loadUiType(
    pathlib.Path(__file__).with_name('fileWidget.ui'), resource_suffix='', import_from="ui"
)


class FileWidget(_UiBase):
    def __init__(self, parent=None):
        super().__init__(parent)

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

        self.__clear()

    def __openFileDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать файл', '*.py')[0]
        if fname:
            self.__readData(fname)
            self.__updateCodeEdit()

    def __clear(self):
        self.rawData = []
        self.data = None
        self.__updateCodeEdit()

    def __updateCodeEdit(self):
        self.ui.textEdit.setPlainText(''.join(self.rawData))
        self.ui.textEdit.setEnabled(len(self.rawData) > 0)
        self.setPlagiarized(None)

    def __readData(self, filename):
        file = open(filename, 'r')
        self.rawData = file.readlines()
        file.close()
        # with open('xast/weights.json') as json_file:
        #     weights = json.load(json_file)
        # self.data = TreeBuilder.build(self.rawData, weights)
        self.data = BagOfWords(self.rawData)

    def isLoaded(self):
        return self.data is not None

    def setPlagiarized(self, plagiarized):
        back_color = QColor(Qt.green)
        if plagiarized is None:
            back_color = QColor(Qt.darkGray)
        elif plagiarized:
            back_color = QColor(Qt.red)
        self.ui.textEdit.setBackgroundColor(back_color)
