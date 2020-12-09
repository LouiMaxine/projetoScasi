from PyQt5 import QtGui
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QFileDialog
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.QtCore import QFileInfo


class janela(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Registro de alunos: "
        self.top = 100
        self.left = 100
        self.width = 800
        self.height = 500
        self.setWindowIcon (QtGui.QIcon('icon/g2.png'))

        self.iniciar_janela()

    def iniciar_janela(self):
        botao = QPushButton("Imprimir",self)
        botao.setGeometry(200,100,100,50)
        botao.clicked.connect(self.criardialogo)

        botaoV = QPushButton("Visualizar",self)
        botaoV.setGeometry(100,100,100,50)
        botaoV.clicked.connect(self.visualizar_impressao)

        botaoP = QPushButton("Salvar em PDF",self)
        botaoP.setGeometry(300,100,100,50)
        botaoP.clicked.connect(self.pdf)

        self.editar_text = QTextEdit(self)
        self.editar_text.setGeometry(100,150,200,200)

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()


    def pdf(self):
        salvar, _ = QFileDialog.getSaveFileName(self, 'salvarpdf', None, 'Arquivo PDF (.pdf);; All files()')

        if salvar != '':
            if QFileInfo(salvar).suffix() == "": salvar += '.pdf'

            imprimir = QPrinter(QPrinter.HighResolution)
            imprimir.setOutputFormat(QPrinter.PdfFormat)
            imprimir.setOutputFileName(salvar)
            self.editar_text.document().print_(imprimir)


    def visualizar_impressao(self):
        imprimir = QPrinter(QPrinter.HighResolution)
        visualizar = QPrintPreviewDialog(imprimir, self)
        visualizar.paintRequested.connect(self.printVisual)
        visualizar.exec_()

    def printVisual(self, imprimir):
            self.editar_text.print_(imprimir)

    def criardialogo(self):
        imprimir = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(imprimir)

        if dialog.exec_() == QPrintDialog.Accepted:
            self.editar_text.print_(imprimir)

app = QApplication(sys.argv)
janela = janela()
sys.exit(app.exec_())
