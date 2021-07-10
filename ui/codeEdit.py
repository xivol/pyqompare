import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class LineNumberArea(QWidget):
    def __init__(self, editor, color):
        super().__init__(editor)
        self.editor = editor
        self.color = color

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self, QColor(Qt.darkGray))

        self.hihghlightColor = QColor(Qt.yellow).lighter(160)

        # self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)

        self.updateLineNumberAreaWidth(0)

    def lineNumberAreaWidth(self):
        """ This method has been slightly modified (use of log and uses actual
        font rather than standart.) """
        n_lines = self.blockCount()
        digits = np.ceil(np.log10(n_lines)) + 0.5
        return digits * QFontMetrics(self.font()).width('9') + 3

    def updateLineNumberAreaWidth(self, _):
        # print('CodeEditor.updateLineNumberAreaWidth: margin = {}'.format(self.lineNumberAreaWidth()))
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        # print('CodeEditor.updateLineNumberArea: rect = {}, dy = {}'.format(rect, dy))

        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
                                       rect.height())

        # print('CodeEditor.updateLineNumberArea: rect.contains(self.viewport().rect()) = {}'.format(
        #     rect.contains(self.viewport().rect())))
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                                              self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        # print('CodeEditor.lineNumberAreaPaintEvent')
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), self.lineNumberArea.color.lighter(160))

        if self.blockCount() > 1:
            block = self.firstVisibleBlock()
            blockNumber = block.blockNumber()
            top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
            bottom = top + self.blockBoundingRect(block).height()

            # Just to make sure I use the right font
            height = QFontMetrics(self.font()).height()
            while block.isValid() and (top <= event.rect().bottom()):
                if block.isVisible() and (bottom >= event.rect().top()):
                    number = str(blockNumber + 1)
                    painter.setPen(self.lineNumberArea.color.darker(160))
                    painter.drawText(0, top, self.lineNumberArea.width(), height,
                                     Qt.AlignRight, number)

                block = block.next()
                top = bottom
                bottom = top + self.blockBoundingRect(block).height()
                blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(self.hihghlightColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
            self.setExtraSelections(extraSelections)

    def setBackgroundColor(self, color):
        self.lineNumberArea.color = color

        p = self.viewport().palette()
        p.setColor(self.viewport().backgroundRole(), color.lighter(190))
        self.viewport().setPalette(p)

        self.update()
