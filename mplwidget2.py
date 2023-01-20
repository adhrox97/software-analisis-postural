# coding=utf-8
from PyQt5.QtWidgets import*

from matplotlib import cm

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure

    
class MplWidget2(QWidget):
    
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        
        self.canvas = FigureCanvas(Figure())
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        
        self.canvas.ax  = self.canvas.figure.add_subplot(1,1,1)
        
        self.setLayout(vertical_layout)