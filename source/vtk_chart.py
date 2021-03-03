'''
Module that contains VTKChartWidget class and values of its default
attributes. This class is used for vizuaisation and customizing of 2D plots
'''


import vtk

from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


default_line_colors = [(1, 0, 0),
                       (0, 1, 0),
                       (0, 0, 1),
                       (1, 0, 1),
                       (0, 0.498, 0),
                       (0, 0, 0.667),
                       (1, 0.4, 1),
                       (1, 0.8, 0),
                       (0, 0.749, 0),
                       (1, 0.749, 1),
                       (1, 0.467, 0),
                       (0, 0.6, 1)]

default_line_width = [1.0,
                      1.0,
                      1.0,
                      4.0,
                      4.0,
                      4.0,
                      4.0,
                      2.0,
                      2.0,
                      2.0,
                      2.0,
                      2.0]

default_line_types = [1,
                      1,
                      1,
                      1,
                      1,
                      1,
                      2,
                      2,
                      2,
                      2,
                      2,
                      2]


## Wrapper class on vtkChartXY. Its used for vizualisation
# and customizing of 2D plots
class VTKChartWidget(object):

    def __init__(self, chart_frame):
        super(VTKChartWidget, self).__init__()
        vtk.vtkObject.GlobalWarningDisplayOff()

        self.line_colors = default_line_colors
        self.line_width = default_line_width
        self.line_types = default_line_types

        self._gui_callbacks = []

        self.chart_frame = chart_frame

        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(1.0, 1.0, 1.0)

        self.table = vtk.vtkTable()
        self.chart = vtk.vtkChartXY()
        self.chart_scene = vtk.vtkContextScene()
        self.chart_actor = vtk.vtkContextActor()
        self.chart_view = vtk.vtkContextView()

        self.chart_scene.AddItem(self.chart)
        self.chart_actor.SetScene(self.chart_scene)
        self.chart_view.SetScene(self.chart_scene)

        self.renderer.AddActor(self.chart_actor)
        self.chart_scene.SetRenderer(self.renderer)

        self.chart.SetShowLegend(True)
        legend = self.chart.GetLegend()
        legend.SetInline(False)
        legend.SetHorizontalAlignment(vtk.vtkChartLegend.RIGHT)
        legend.SetVerticalAlignment(vtk.vtkChartLegend.TOP)
        legend.SetLabelSize(20)
        title_prop = self.chart.GetTitleProperties()
        title_prop.SetFontSize(20)

        self.init_xy_data()
        self.set_up_view()

    @property
    def options_dict(self):
        options_dict = {}
        options_dict['x_min'] = self.chart.GetAxis(0).GetMinimum()
        options_dict['x_max'] = self.chart.GetAxis(0).GetMaximum()
        options_dict['y_min'] = self.chart.GetAxis(1).GetMinimum()
        options_dict['y_max'] = self.chart.GetAxis(1).GetMaximum()

        lines_options = []
        for i in range(self.chart.GetNumberOfPlots()):
            line = self.chart.GetPlot(i)
            rgb = [0.0, 0.0, 0.0]
            line.GetColor(rgb)
            width = line.GetWidth()
            line_type = line.GetPen().GetLineType()
            lines_options.append((rgb, width, line_type))
        options_dict['lines_options'] =  lines_options

        return options_dict

    def apply_options(self, options_dict):
        self.chart.GetAxis(0).SetMinimum(options_dict['x_min'])
        self.chart.GetAxis(0).SetMaximum(options_dict['x_max'])
        self.chart.GetAxis(1).SetMinimum(options_dict['y_min'])
        self.chart.GetAxis(1).SetMaximum(options_dict['y_max'])

        lines_options = options_dict['lines_options']
        for i in range(self.chart.GetNumberOfPlots()):
            rgb = lines_options[i][0]
            width = lines_options[i][1]
            line_type = lines_options[i][2]

            _index1 = i % len(self.line_colors)
            _index2 = i % len(self.line_width)
            _index3 = i % len(self.line_types)

            self.line_colors[_index1] = rgb
            self.line_width[_index2] = width
            self.line_types[_index3] = line_type

            line = self.chart.GetPlot(i)
            line.SetColor(*rgb)
            width = line.SetWidth(width)
            line_type = line.GetPen().SetLineType(line_type)
            lines_options.append((rgb, width, line_type))
            self.render()

    def add_callback(self, callback):
        if callable(callback):
            self._gui_callbacks.append(callback)

    def refresh_gui(method):
        def wrapper(self, *args):
            method(self, *args)
            for i in range(len(self._gui_callbacks)):
                self._gui_callbacks[i]()
        return wrapper

    def init_xy_data(self):
        self.chart.SetTitle('N/A')
        self.chart.ClearPlots()
        self.chart.AddPlot(vtk.vtkChart.LINE)

    def set_up_view(self):
        self.interactor = QVTKRenderWindowInteractor(self.chart_frame)
        self.interactor.GetRenderWindow().AddRenderer(self.renderer)
        self.chart_frame.layout().addWidget(self.interactor, 1, 0, 1, 1)
        self.iren = self.interactor.GetRenderWindow().GetInteractor()

    @refresh_gui
    def set_xy_data(self, x_array, y_array, title):
        if not title:
            title = 'N/A'
        self.chart.SetTitle(title)
        self.chart.ClearPlots()

        self.table = vtk.vtkTable()

        self.table.AddColumn(x_array)
        self.table.AddColumn(y_array)

        line = self.chart.AddPlot(vtk.vtkChart.LINE)

        self.chart.GetAxis(1).SetTitle(x_array.GetName())
        self.chart.GetAxis(0).SetTitle(y_array.GetName())

        line.SetInputData(self.table, 0, 1)

        line.SetColor(*self.line_colors[0])
        line.SetWidth(self.line_width[0])
        line.GetPen().SetLineType(self.line_types[0])

        self.set_active()

        self.render()

    @refresh_gui
    def set_multiple_xy_data(self, x_array, y_arrays_list, title):
        if not title:
            title = 'N/A'
        self.chart.SetTitle(title)
        self.chart.ClearPlots()
        self.chart.GetAxis(0).SetTitle('')
        self.chart.GetAxis(1).SetTitle(x_array.GetName())

        self.table = vtk.vtkTable()

        self.table.AddColumn(x_array)
        for var_index, y_array in enumerate(y_arrays_list):
            self.table.AddColumn(y_array)
            line = self.chart.AddPlot(vtk.vtkChart.LINE)
            line.SetInputData(self.table, 0, var_index + 1)

            _index = var_index % len(self.line_colors)
            color_rgb = self.line_colors[_index]

            line.SetColor(*color_rgb)
            line.GetPen().SetLineType(self.line_types[_index])
            line.SetWidth(self.line_width[_index])

        self.set_active()
        self.render()

    def get_values_as_table(self):
        n_columns = self.table.GetNumberOfColumns()
        if not n_columns:
            return []

        n_rows = self.table.GetColumn(0).GetNumberOfTuples()
        if not n_rows:
            return []

        column_names = []
        for i in range(n_columns):
            column_names.append(self.table.GetColumn(i).GetName())

        table_values = [column_names, ]
        for i in range(n_rows):
            cur_row = []
            for j in range(n_columns):
                column = self.table.GetColumn(j)
                cur_row.append(column.GetValue(i))
            table_values.append(cur_row)
        return table_values

    @property
    def is_visible(self):
        return self.chart_frame.isVisible()

    def show(self):
        self.chart_frame.show()

    def hide(self):
        self.chart_frame.hide()

    def set_active(self):
        self.chart_frame.set_active()

    def render(self):
        self.interactor.GetRenderWindow().Render()
