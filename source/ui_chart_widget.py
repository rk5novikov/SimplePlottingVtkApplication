'''
Module with classes needed for chart widget gui
'''


import os
import vtk

from PyQt4 import QtGui, QtCore

from vtk_chart import VTKChartWidget

from ui_config import config

import ui_widgets


## Small widget needed for selection of the color, style and thickness
# of plot lines
class UiPlotLineOptionsGroupBox(ui_widgets.UiQGroupBox):

    LineTypes = ['SOLID_LINE',
                 'DASH_LINE',
                 'DOT_LINE',
                 'DASH_DOT_LINE',
                 'DASH_DOT_DOT_LINE',
                 'DENSE_DOT_LINE']

    def __init__(self, serie_id=1):
        title = 'Serie {0:d}'.format(serie_id)
        super(UiPlotLineOptionsGroupBox, self).__init__(title, bold=True, height=100, width=360)

        label_color = ui_widgets.UiQLabel('Coleur', width=150, font_size=12, alignment='AlignVCenter|AlignRight')
        label_epaiseur = ui_widgets.UiQLabel('Epaisseur', width=150, font_size=12, alignment='AlignVCenter|AlignRight')
        label_style = ui_widgets.UiQLabel('Type de ligne', width=150, font_size=12, alignment='AlignVCenter|AlignRight')

        self.label_color = ui_widgets.UiQLabelColor(width=20, height=20)
        self.label_line_ep = ui_widgets.UiQLineEditDouble('', height=20, width=170)
        self.combox_line_types = ui_widgets.UiQComboBox(self.LineTypes, height=20, width=170)

        layout = QtGui.QGridLayout(self)
        layout.addWidget(label_color, 0, 0, 1, 1)
        layout.addWidget(label_epaiseur, 1, 0, 1, 1)
        layout.addWidget(label_style, 2, 0, 1, 1)
        layout.addWidget(self.label_color, 0, 1, 1, 1)
        layout.addWidget(self.label_line_ep, 1, 1, 1, 1)
        layout.addWidget(self.combox_line_types, 2, 1, 1, 1)

    def set_color(self, rgb):
        if rgb:
            self.label_color.setColor(rgb)

    def set_width(self, ep):
        self.label_line_ep.setText('{0:.3f}'.format(ep))

    def set_line_type(self, line_type):
        self.combox_line_types.setCurrentIndex(line_type - 1)

    def get_color(self):
        return self.label_color.getColor()

    def get_width(self):
        return float(self.label_line_ep.text())

    def get_line_type(self):
        return self.combox_line_types.currentIndex() + 1


## Dialog window where user can adjust chart vizualisation
# attributes
class UiChartOptionsDialog(QtGui.QScrollArea):

    def __init__(self, parent_widget):
        super(UiChartOptionsDialog, self).__init__(parent=parent_widget)

        self.parent_widget = parent_widget

        scroll_area = QtGui.QScrollArea()
        scroll_area.setMinimumHeight(280)
        scroll_area.setFixedWidth(400)

        self.frame_data = QtGui.QFrame(scroll_area)
        self.layout = QtGui.QGridLayout(self.frame_data)

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowTitle("Options du graph")

        gb_limits = ui_widgets.UiQGroupBox("Limites", bold=True, height=100, width=360)
        gb_limits_layout = QtGui.QGridLayout(gb_limits)

        label_x_min = ui_widgets.UiQLabel('Y mini', width=80, font_size=12, alignment='AlignVCenter|AlignRight')
        label_x_max = ui_widgets.UiQLabel('Y maxi', width=80, font_size=12, alignment='AlignVCenter|AlignRight')
        label_y_min = ui_widgets.UiQLabel('X mini', width=80, font_size=12, alignment='AlignVCenter|AlignRight')
        label_y_max = ui_widgets.UiQLabel('X maxi', width=80, font_size=12, alignment='AlignVCenter|AlignRight')

        self.line_x_min = ui_widgets.UiQLineEditDouble('', height=20, width=80)
        self.line_x_max = ui_widgets.UiQLineEditDouble('', height=20, width=80)
        self.line_y_min = ui_widgets.UiQLineEditDouble('', height=20, width=80)
        self.line_y_max = ui_widgets.UiQLineEditDouble('', height=20, width=80)

        gb_limits_layout.addWidget(label_x_min, 0, 0, 1, 1)
        gb_limits_layout.addWidget(self.line_x_min, 0, 1, 1, 1)
        gb_limits_layout.addWidget(label_x_max, 0, 2, 1, 1)
        gb_limits_layout.addWidget(self.line_x_max, 0, 3, 1, 1)
        gb_limits_layout.addWidget(label_y_min, 1, 0, 1, 1)
        gb_limits_layout.addWidget(self.line_y_min, 1, 1, 1, 1)
        gb_limits_layout.addWidget(label_y_max, 1, 2, 1, 1)
        gb_limits_layout.addWidget(self.line_y_max, 1, 3, 1, 1)

        self.layout.addWidget(gb_limits, 0, 0, 1, 1)
        scroll_area.setWidget(self.frame_data)

        button_annuler = ui_widgets.UiQPushButton("Annuler", width=80, height=25, font_size=12)
        button_appliquer = ui_widgets.UiQPushButton("Appliquer", width=80, height=25, font_size=12)

        main_layout = QtGui.QGridLayout(self)
        main_layout.addWidget(scroll_area, 0, 0, 1, 4)
        main_layout.addWidget(button_appliquer, 1, 2, 1, 1)
        main_layout.addWidget(button_annuler, 1, 3, 1, 1)

        button_appliquer.clicked.connect(self.on_button_appliquer_clicked)
        button_annuler.clicked.connect(self.on_button_annuler_clicked)

        self.line_opt_widgets = []

    @property
    def options_dict(self):
        options_dict = {}
        try:
            options_dict['x_min'] = float(self.line_x_min.text())
            options_dict['x_max'] = float(self.line_x_max.text())
            options_dict['y_min'] = float(self.line_y_min.text())
            options_dict['y_max'] = float(self.line_y_max.text())
        except ValueError:
            return {}
        lines_options = []
        for opt_widget in self.line_opt_widgets:
            rgb = opt_widget.get_color()
            width = opt_widget.get_width()
            line_type = opt_widget.get_line_type()
            lines_options.append([rgb, width, line_type])
        options_dict['lines_options'] = lines_options
        return options_dict

    def on_button_appliquer_clicked(self):
        vtk_chart = self.parent_widget.vtk_chart
        options_dict = self.options_dict
        if options_dict:
            vtk_chart.apply_options(options_dict)

    def on_button_annuler_clicked(self):
        self.close()
        self.update()

    def update(self):
        vtk_chart = self.parent_widget.vtk_chart
        options_dict = vtk_chart.options_dict
        self.line_x_min.setText('{0:.3f}'.format(options_dict['x_min']))
        self.line_x_max.setText('{0:.3f}'.format(options_dict['x_max']))
        self.line_y_min.setText('{0:.3f}'.format(options_dict['y_min']))
        self.line_y_max.setText('{0:.3f}'.format(options_dict['y_max']))

        for opt_widget in self.line_opt_widgets:
            opt_widget.setParent(None)
        self.line_opt_widgets = []

        for ind, options in enumerate(options_dict['lines_options']):
            opt_widget = UiPlotLineOptionsGroupBox(ind + 1)
            opt_widget.set_color(options[0])
            opt_widget.set_width(options[1])
            opt_widget.set_line_type(options[2])
            self.layout.addWidget(opt_widget, ind + 1, 0, 1, 1)
            self.line_opt_widgets.append(opt_widget)
        n_lines = len(options_dict['lines_options'])
        self.frame_data.setFixedHeight(105 * (n_lines + 1))


# Chart widget gui class
class UiChartWidget(QtGui.QFrame):

    OpenIcon = os.path.join(config.dir_pics, 'open.png')
    ChartIcon = os.path.join(config.dir_pics, 'chart.png')
    OptionsIcon = os.path.join(config.dir_pics, 'custom_view_options.png')
    ExportIcon = os.path.join(config.dir_pics, 'write.png')

    def __init__(self, main_window=None):
        super(UiChartWidget, self).__init__(parent=main_window)

        self.main_window = main_window
        self.logger = main_window.logger

        self.options_dialog = UiChartOptionsDialog(self)

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowMinimizeButtonHint)

        icon = QtGui.QIcon(QtGui.QPixmap(self.ChartIcon))
        self.setWindowTitle('xy-chart')
        self.setWindowIcon(icon)

        options_toolbar = QtGui.QToolBar()
        options_toolbar.setWindowTitle('Options...')

        action_open = QtGui.QAction(QtGui.QIcon(self.OpenIcon), 'Ouvrir xy csv', self)
        action_open.triggered.connect(self.read_csv)

        action_options = QtGui.QAction(QtGui.QIcon(self.OptionsIcon), 'Options du graph', self)
        action_options.triggered.connect(self.options_dialog.show)

        action_export = QtGui.QAction(QtGui.QIcon(self.ExportIcon), 'Exporter les valeurs', self)
        action_export.triggered.connect(self.export_values)

        options_toolbar.addAction(action_open)
        options_toolbar.addAction(action_options)
        options_toolbar.addAction(action_export)

        chart_layout = QtGui.QGridLayout(self)
        chart_layout.setContentsMargins(0, 0, 0, 0)
        chart_layout.setSpacing(0)

        chart_layout.addWidget(options_toolbar, 0, 0, 1, 1)

        self.vtk_chart = VTKChartWidget(self)
        self.vtk_chart.add_callback(self.options_dialog.update)

        self.vtk_chart.interactor.Initialize()
        self.vtk_chart.interactor.Start()

    def export_values(self):
        table = self.vtk_chart.get_values_as_table()
        if not table:
            return
        filename = QtGui.QFileDialog.getSaveFileName(self, "Nom du fichier de text", '', "Text File (*.txt)")
        if filename:
            with open(filename, 'w') as f0:
                titles = '\t'.join(table[0])
                f0.write(titles + '\n')
                for row in table[1:]:
                    vals = [str(v) for v in row]
                    f0.write('\t'.join(vals) + '\n')
            self.logger.emit('Fichier {0} a ete cree avec succes'.format(filename))

    def read_csv(self):
        file_path = QtGui.QFileDialog.getOpenFileName(self, "Nom du fichier csv", '', "Csv File (*.csv)")
        if not file_path:
            return

        plot_name = os.path.basename(file_path)
        x_vals = []
        y_vals = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    x, y = map(float, [s.strip() for s in line.split(',')[:2]])
                    x_vals.append(x)
                    y_vals.append(y)
            x_array = vtk.vtkDoubleArray()
            y_array = vtk.vtkDoubleArray()
            x_array.SetNumberOfComponents(1)
            y_array.SetNumberOfComponents(1)
            x_array.SetName("x")
            y_array.SetName("y")
            for x_val, y_val in zip(x_vals, y_vals):
                x_array.InsertNextValue(x_val)
                y_array.InsertNextValue(y_val)
            self.vtk_chart.set_xy_data(x_array, y_array, plot_name)
        except Exception as e:
            self.logger.emit('Erreur en cours de lecture {}: '.format(file_path), 'error')
            self.logger.emit(str(e), 'error', hide_time=True)


    def init_position(self):
        self.resize(780, 250)
        pos = self.main_window.pos()
        x = pos.x() + 250
        y = pos.y() + 350
        self.move(x, y)

    def set_active(self):
        QtGui.QApplication.setActiveWindow(self)
