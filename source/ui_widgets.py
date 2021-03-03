'''
Module with wrapper classes on standart qt widget.
Its used to customize widgets's behavior and appearence
in specific situations.
'''


import os
import sys
import decimal

from datetime import datetime

from PyQt4 import QtGui
from PyQt4 import QtCore

from ui_config import config


checked = QtCore.Qt.Checked
unchecked = QtCore.Qt.Unchecked


default_font_size = 12
default_alignment = 'AlignVCenter|AlignRight'


def scientific_form(s):
    return '%.2E' % decimal.Decimal(s)


def fixed_form(s):
    return '{0:.1f}'.format(float(s))


def fixed_form_plus(s):
    return '{0:.4f}'.format(float(s))


class UiQLabel(QtGui.QLabel):

    def __init__(self, text='', width=None, height=None, font_size=default_font_size, alignment=default_alignment, bold=False):
        super(UiQLabel, self).__init__(text)
        bold_str = 'font: bold; ' if bold else ''
        self.setStyleSheet("QLabel {font: " + str(font_size) + "px; " + bold_str + "qproperty-alignment: '" + alignment + "';}")
        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)
        self.setWordWrap(True)


class UiQLabelColor(QtGui.QLabel):

    def __init__(self, width=None, height=None):
        super(UiQLabelColor, self).__init__()
        self.setStyleSheet("QWidget { background-color: black}")
        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)
        self.mousePressEvent = self.callColorPicker

    def getColor(self, color_format='rgbf'):
        if color_format == 'rgbf':
            _color = self.palette().window().color()
            return _color.redF(), _color.greenF(), _color.blueF()
        elif color_format == 'hex':
            return self.palette().window().color().name()
        elif color_format == 'qcolor':
            return self.palette().window().color()

    def setColor(self, color, color_format='rgbf'):
        if color_format == 'rgbf':
            _color = QtGui.QColor()
            _color.setRgbF(*color)
            self.setStyleSheet("QWidget { background-color: %s}" % _color.name())
        elif color_format == 'hex':
            self.setStyleSheet("QWidget { background-color: %s}" % color)
        elif color_format == 'qcolor':
            self.setStyleSheet("QWidget { background-color: %s}" % color.name())

    def callColorPicker(self, event):
        color = QtGui.QColorDialog.getColor()
        if color.isValid():
            self.setColor(color, color_format='qcolor')

    def convertRgbToHex(self):
        pass

    def convertHexToRgb(self):
        pass


class UiQLabelPic(QtGui.QLabel):

    def __init__(self, img='', width=None, height=None, need_scaled=False, font_size=default_font_size, parent=None):
        super(UiQLabelPic, self).__init__(parent)
        self.need_scaled = need_scaled
        if os.path.isfile(img):
            self.pixmap = QtGui.QPixmap(img)
        else:
            self.pixmap = None
            self.setText('N/A')
            self.setStyleSheet("QLabel {font: " + str(font_size) + "px; qproperty-alignment: 'AlignTop|AlignLeft'; }")
        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)

    def paintEvent(self, event):
        if self.pixmap:
            painter = QtGui.QPainter(self)
            point = QtCore.QPoint(0, 0)
            if self.need_scaled:
                size = self.size()
                scaledPix = self.pixmap.scaled(size, QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
                painter.drawPixmap(point, scaledPix)
            else:
                painter.drawPixmap(point, self.pixmap)
        else:
            QtGui.QLabel.paintEvent(self, event)


class UiQTextEdit(QtGui.QTextEdit):

    editingFinished = QtCore.pyqtSignal()

    def __init__(self, text='', width=None, height=None, font_size=default_font_size, enabled=True):
        super(UiQTextEdit, self).__init__()
        self.append(text)
        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)
        self.setStyleSheet('QTextEdit { font:' + str(font_size) + 'px; color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);}')
        self.setEnabled(enabled)

    def focusOutEvent(self, e):
        self.editingFinished.emit()
        QtGui.QTextEdit.focusOutEvent(self, e)


class UiQLineEditDouble(QtGui.QLineEdit):

    def __init__(self, text='',
                 width=70,
                 height=20,
                 font_size=default_font_size,
                 val_range=None,
                 enabled=True,
                 highlight_nonvalid=False,
                 int_validator=False,
                 read_only=False):

        super(UiQLineEditDouble, self).__init__()
        self.font_size = font_size
        self.highlight_nonvalid = highlight_nonvalid
        if val_range:
            if int_validator:
                validator = QtGui.QIntValidator(val_range[0], val_range[1], self)
                validator.setNotation(QtGui.QIntValidator.StandardNotation)
            else:
                validator = QtGui.QDoubleValidator(val_range[0], val_range[1], 5, self)
                validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        else:
            if int_validator:
                validator = QtGui.QIntValidator()
            else:
                validator = QtGui.QDoubleValidator()
        if read_only:
            self.setReadOnly(True)

        self.setValidator(validator)

        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)

        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.setStyleSheet('QLineEdit { font:' + str(self.font_size) + 'px; color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);}')
        self.setText(text)
        self.setEnabled(enabled)
        if self.highlight_nonvalid:
            self.textChanged.connect(self.highlightNonValid)
            self.highlightNonValid()

    def highlightNonValid(self):
        try:
            float(self.text())
            self.setStyleSheet('QLineEdit { font:' + str(self.font_size) + 'px; color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);}')
        except ValueError:
            if self.isEnabled():
                self.setStyleSheet("QLineEdit{font:" + str(self.font_size) + "px; background-color: rgb(255, 255, 128);} QLineEdit:hover{border: 1px solid gray; background-color rgb(255, 255, 128);}")
            else:
                self.setStyleSheet('QLineEdit { font:' + str(self.font_size) + 'px; color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);}')

    def setEnabled(self, enabled):
        QtGui.QLineEdit.setEnabled(self, enabled)
        if self.highlight_nonvalid:
            self.highlightNonValid()


class UiQLineEditString(QtGui.QLineEdit):

    InvalidPathStyleSheet = "QLineEdit{font:12px; background-color: rgb(255, 255, 128);} QLineEdit:hover{border: 0px solid gray; }"
    TextStyleSheet = "QLineEdit { font:12px; color: rgb(0, 0, 0); }"
    ReadOnlyStyleSheet = "QLineEdit { font:12px; background-color: rgb(240, 240, 240); }"
    DefaultTextStyleSheet = "QLineEdit { font:12px; font-style: italic; color: rgb(80, 80, 80); }"

    def __init__(self, text='', width=None, height=None, enabled=True, default_text=None, read_only=False):
        super(UiQLineEditString, self).__init__()
        self.setFrame(True)
        self.setStyleSheet(self.TextStyleSheet)
        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)
        self.setText(text)
        self.setEnabled(enabled)
        #
        self.default_text = default_text
        if default_text:
            self.default_text_is_current = False
            self.setDefaultText()
        if read_only:
            self.setReadOnly(True)
        self.init_style = self.TextStyleSheet

    def setDefaultText(self):
        if not self.text():
            self.default_text_is_current = True
            self.blockSignals(True)
            self.setText(self.default_text)
            self.blockSignals(False)
            self.init_style = self.DefaultTextStyleSheet
            self.setStyleSheet(self.init_style)
        else:
            self.default_text_is_current = False
            self.init_style = self.TextStyleSheet
            self.setStyleSheet(self.init_style)

    def highlightInvalidPath(self):
        if (not self.text()) and self.isEnabled():
            self.init_style = self.InvalidPathStyleSheet
            self.setStyleSheet(self.init_style)
        else:
            self.init_style = self.TextStyleSheet
            self.setStyleSheet(self.init_style)

    def focusInEvent(self, e):
        if self.default_text:
            if self.default_text_is_current:
                self.default_text_is_current = False
                self.setText('')
                self.init_style = self.TextStyleSheet
                self.setStyleSheet(self.init_style)
        QtGui.QLineEdit.focusInEvent(self, e)

    def focusOutEvent(self, e):
        if self.default_text:
            self.setDefaultText()
        QtGui.QLineEdit.focusOutEvent(self, e)


class UiQPushButton(QtGui.QPushButton):

    def __init__(self, text='', width=80, height=25, font_size=default_font_size, enabled=True):
        super(UiQPushButton, self).__init__(text)
        self.setStyleSheet("QPushButton {font: " + str(font_size) + "px;}")
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.setEnabled(enabled)


class UiQComboBox(QtGui.QComboBox):

    def __init__(self, items=[], width=None, height=25, font_size=default_font_size, parent=None):
        super(UiQComboBox, self).__init__(parent)
        self.setStyleSheet("QComboBox {font: " + str(font_size) + "px;}")
        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)
        for item in items:
            self.addItem(item)

    def wheelEvent(self, *args, **kwargs):
        pass

    def setText(self, text):
        index = self.findText(text, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.setCurrentIndex(index)
        else:
            self.setCurrentIndex(0)

    def setItems(self, items=[]):
        self.blockSignals(True)
        self.clear()
        if items:
            for item in items:
                self.addItem(item)
            self.setCurrentIndex(0)
        self.blockSignals(False)


class UiQTableWidgetItemDouble(QtGui.QLineEdit):

    default_style_sheet = "QLineEdit { font: 12px; background: rgb(255, 255, 255); selection-background-color: rgb(51, 153, 255); }"
    selected_style_sheet = "QLineEdit { font: 12px; font: bold; background: rgb(0, 255, 255); selection-background-color: rgb(233, 99, 0); }"

    def __init__(self, text, parent_table, pos, form=fixed_form):
        self.var_float = float(text)
        self.form = form
        super(UiQTableWidgetItemDouble, self).__init__(self.form(text))
        self.parent_table = parent_table
        self.pos = pos
        self.setValidator(QtGui.QDoubleValidator())
        self.setStyleSheet(UiQTableWidgetItemDouble.default_style_sheet)
        self.setFrame(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

    def focusInEvent(self, e):
        self.setStyleSheet(UiQTableWidgetItemDouble.selected_style_sheet)
        self.setText(str(self.var_float))
        self.parent_table.setCurrentCell(*self.pos)
        QtGui.QLineEdit.focusInEvent(self, e)

    def focusOutEvent(self, e):
        self.var_float = float(self.text())
        self.setText(self.form(self.text()))
        self.setStyleSheet(UiQTableWidgetItemDouble.default_style_sheet)
        QtGui.QLineEdit.focusOutEvent(self, e)


class UiQTableWidgetItemCombox(QtGui.QComboBox):

    style_sheet = '''QComboBox {
        font: 12px;
        border: 1px solid white;
        min-width: 6em;
    }

    QComboBox:editable {
        background: white;
    }

    QComboBox:on {
        padding-top: 3px;
        padding-left: 4px;
    }

    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 15px;
        border-left-width: 0px;
    }

    QComboBox::down-arrow {
        image: url(dir_pics/downarrow.png);
    }'''.replace('dir_pics', config.dir_pics)

    def __init__(self, items=[], font_size=default_font_size, parent=None):
        super(UiQTableWidgetItemCombox, self).__init__(parent)
        self.setStyleSheet(UiQTableWidgetItemCombox.style_sheet)
        for item in items:
            self.addItem(item)

    def wheelEvent(self, *args, **kwargs):
        pass

    def setText(self, text):
        index = self.findText(text, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.setCurrentIndex(index)
        else:
            self.setCurrentIndex(0)


class UiQTabWidget(QtGui.QTabWidget):

    def __init__(self, width=None, height=None, font_size=default_font_size, bold=False, parent=None):
        super(UiQTabWidget, self).__init__(parent)
        bold_str = 'font: bold; ' if bold else ''
        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)
        self.setStyleSheet("QTabWidget {font: " + str(font_size) + "px; " + bold_str + " }")


class UiQRadioButton(QtGui.QRadioButton):

    def __init__(self, text='', width=None, height=None, font_size=default_font_size, bold=False):
        super(UiQRadioButton, self).__init__(text)
        bold_str = 'font: bold; ' if bold else ''
        self.setStyleSheet("QRadioButton {font: " + str(font_size) + "px; " + bold_str + "}")
        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)


class UiTreeWidgetParentItem(QtGui.QTreeWidgetItem):

    def __init__(self, *args):
        super(UiTreeWidgetParentItem, self).__init__(*args)
        self.setFlags(self.flags() ^ QtCore.Qt.ItemIsSelectable)


class UiTreeWidgetItem(QtGui.QTreeWidgetItem):

    def __init__(self, parent, text, data=None):
        self.item_data = data
        super(UiTreeWidgetItem, self).__init__(parent, text)

    def setItemData(self, data):
        self.item_data = data


class UiQGroupBox(QtGui.QGroupBox):

    def __init__(self, text='', width=None, height=None, font_size=default_font_size, bold=False):
        super(UiQGroupBox, self).__init__()
        font = QtGui.QFont()
        font.setPixelSize(font_size)
        font.setBold(bold)
        self.setTitle(text)
        self.setFont(font)
        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)


class UiQCheckBox(QtGui.QCheckBox):

    checked = QtCore.Qt.Checked
    unchecked = QtCore.Qt.Unchecked
    states = {True: checked, False: unchecked}

    def __init__(self, text='', width=None, height=None, font_size=default_font_size, bold=False):
        super(UiQCheckBox, self).__init__(text)
        bold_str = 'font: bold; ' if bold else ''
        self.setStyleSheet("QCheckBox {font: " + str(font_size) + "px; " + bold_str + "}")
        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)

    def setBoolState(self, state):
        self.setCheckState(self.states[state])

    def getBoolState(self):
        if int(self.checkState()) == 2:
            return True
        else:
            return False


class UiLoggerWidget(QtGui.QTextEdit):

    colors = {'error': '#ff0000', 'success': '#006600', 'info': '#000000'}

    def __init__(self, font_size=12, parent=None):
        super(UiLoggerWidget, self).__init__(parent)
        self.font_size = font_size
        self.setMaximumHeight(140)
        self.setFrameShape(self.Box)
        self.setFrameShadow(self.Sunken)
        # self.redirect_outputs()

    def redirect_outputs(self):
        sys.stdout = self
        sys.stderr = self

    def emit(self, text, message_type='info', hide_time=False):
        cur_time = str(datetime.now().strftime('%H:%M:%S'))
        if not hide_time:
            _args = [self.font_size, UiLoggerWidget.colors[message_type], cur_time, text]
            in_text = '<span style=" font-size:{0:d}px; color:{1};" > [{2}] - {3}</span>'.format(*_args)
        else:
            _args = [self.font_size, UiLoggerWidget.colors[message_type], text]
            in_text = '<span style=" font-size:{0:d}px; color:{1};" > {2}</span>'.format(*_args)
        self.append(in_text)

    def write(self, text, message_type='info', hide_time=False):
        _text = text.strip('\n')
        if _text.strip():
            self.emit(text, message_type, hide_time)


class UiContextMenu(QtGui.QMenu):

    def __init__(self, icons, titles, funcs):
        super(UiContextMenu, self).__init__()
        for icon, title, func in zip(icons, titles, funcs):
            action = QtGui.QAction(QtGui.QIcon(icon), title, self)
            action.triggered.connect(func)
            self.addAction(action)


class UiQListWidgetItem(QtGui.QListWidgetItem):

    def __init__(self, text='', double_validation=False):
        super(UiQListWidgetItem, self).__init__(text)
        if double_validation:
            pass


class UiComponentWidget(QtGui.QFrame):

    ScalarComponentsList = ['Scalar', ]

    VectorComponentsList = ['X Component',
                            'Y Component',
                            'Z Component',
                            'Magnitude']

    TensorComponentsList = ['X Component',
                            'Y Component',
                            'Z Component',
                            'XY Component',
                            'YZ Component',
                            'ZX Component',
                            'Von Mises',
                            'Von Mises signe',
                            '1er Invariant',
                            '2em Invariant',
                            '3em Invariant',
                            'Max. Principal',
                            'Mid. Principal',
                            'Min. Principal']

    ComponentsDict = {'scalar': ScalarComponentsList,
                      'vector': VectorComponentsList,
                      'tensor': TensorComponentsList,
                      None: []}

    LayoutIndexDict = {'scalar': 0,
                       'vector': 1,
                       'tensor': 2,
                       None: 3}

    IndexLayoutDict = {v: k for k, v in LayoutIndexDict.items()}

    def __init__(self, main_window, update_callback=None):
        super(UiComponentWidget, self).__init__()
        self.main_window = main_window

        self.layout = QtGui.QStackedLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(25)
        for field_type, components in self.ComponentsDict.items():
            combox_component = UiQComboBox(components, width=188, parent=main_window)
            self.layout.addWidget(combox_component)
            if callable(update_callback):
                combox_component.activated.connect(update_callback)
        self.layout.widget(self.LayoutIndexDict[None]).setEnabled(False)
        self.layout.setCurrentIndex(len(self.LayoutIndexDict) - 1)

    @property
    def current_component(self):
        return self.layout.currentWidget().currentText()

    def setCurrentFieldType(self, field_type):
        self.layout.setCurrentIndex(self.LayoutIndexDict[field_type])
