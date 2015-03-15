from PyQt4 import QtCore, QtGui, uic
import sys

class MyWidget(QtGui.QMainWindow):
    def __init__(self):
        #somewhere in constructor:
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('MainWindow.ui', self)

def main():

    app = QtGui.QApplication(sys.argv)

    w = MyWidget()
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()