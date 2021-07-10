import pathlib
from PyQt5 import uic
from PyQt5.QtWidgets import *
from ui.fileWidget import FileWidget


def drop_args(target, *args, **kwargs):
    def f(*_, **kw):
        kw.update(kwargs)
        target(*args, **kw)

    return f


_Ui, _UiBase = uic.loadUiType(
    pathlib.Path(__file__).with_name('mainWindow.ui'), resource_suffix='', import_from="ui"
)


class MainWindow(_UiBase):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = _Ui()
        self.ui.setupUi(self)

        # Я пытался разобраться как загрузить вложенные виджеты через UIC,
        # но у меня так и не заработало

        self.ui.widget_left = FileWidget(self.ui.centralwidget)
        self.ui.mainLayout.addWidget(self.ui.widget_left)

        self.ui.separator = QFrame(self.ui.centralwidget)
        self.ui.separator.setFrameShape(QFrame.VLine)
        self.ui.mainLayout.addWidget(self.ui.separator)

        self.ui.widget_right = FileWidget(self.ui.centralwidget)
        self.ui.mainLayout.addWidget(self.ui.widget_right)

        self.ui.compare.pressed.connect(self.__compare)

    def __compare(self):
        if self.ui.widget_left.isLoaded() and self.ui.widget_right.isLoaded():
            if self.ui.widget_left.data != self.ui.widget_right.data:
                self.ui.widget_left.setPlagiarized(False)
                self.ui.widget_right.setPlagiarized(False)
            else:
                self.ui.widget_left.setPlagiarized(True)
                self.ui.widget_right.setPlagiarized(True)