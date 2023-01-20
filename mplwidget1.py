# coding=utf-8
from PyQt5.QtWidgets import*

from matplotlib import cm

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure

    
class MplWidget1(QWidget):
    
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        
        self.canvas = FigureCanvas(Figure())
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        
        self.canvas.ax  = self.canvas.figure.add_subplot(1,3,1)
        self.canvas.ax.set_autoscaley_on(True)
        self.canvas.ax.set_xlim(0, 320) #establecer limites
        self.canvas.ax.set_ylim(0, 240)
        self.canvas.ax.axis("off")
        
        # grafica 2
        self.canvas.ax1  = self.canvas.figure.add_subplot(1,3,2)
        self.canvas.ax1.set_autoscaley_on(True)
        self.canvas.ax1.set_xlim(0, 320) #establecer limites
        self.canvas.ax1.set_ylim(0, 240)
        self.canvas.ax1.axis("off")
        
        self.canvas.ax2  = self.canvas.figure.add_subplot(1,3,3)
        self.canvas.ax2.set_autoscaley_on(True)
        self.canvas.ax2.set_xlim(0, 320) #establecer limites
        self.canvas.ax2.set_ylim(0, 240)
        self.canvas.ax2.axis("off")
        
        self.setLayout(vertical_layout)