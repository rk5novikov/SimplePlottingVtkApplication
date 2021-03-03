'''
Main window module. Here initialisation of gui widgets and construction
of main layout are to be executed.
'''


import sys
import ui_widgets

from ui_chart_widget import UiChartWidget

from PyQt4 import QtGui

from ui_config import config


class UiMainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(UiMainWindow, self).__init__()
        main_frame = QtGui.QFrame()
        #
        self.logger = ui_widgets.UiLoggerWidget()
        #
        self.chart_widget = UiChartWidget(self)
        self.vtk_chart = self.chart_widget.vtk_chart
        #
        main_layout = QtGui.QGridLayout(main_frame)
        main_layout.addWidget(self.chart_widget, 0, 0, 1, 1)
        main_layout.addWidget(self.logger, 1, 0, 1, 1)
        #
        self.setCentralWidget(main_frame)
        self.setWindowTitle('plots')
        self.show()

        self.logger.emit("Lancement de l'application.", 'success')

def main():
    app = QtGui.QApplication(sys.argv)
    main_window = UiMainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
