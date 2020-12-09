from PyQt5 import QtGui
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QPushButton, QToolTip, QMessageBox, QStatusBar
from PyQt5.QtCore import QCoreApplication

class janela(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Registro de alunos: "
        self.top = 100
        self.left = 100
        self.width = 800
        self.height = 500
        self.setWindowIcon (QtGui.QIcon('icon/g2.png'))
        botao = QPushButton("Sair",self)
        botao.move(200,100)
        botao.clicked.connect(self.fechar_Aplicacao)
        self.iniciar_janela()

    def iniciar_janela(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def fechar_Aplicacao(self):
        resposta = QMessageBox.question(self,"BrendaLouise", "Deseja realmente fechar o sistema?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resposta == QMessageBox.Yes:
            self.close()

app = QApplication(sys.argv)
janela = janela()
sys.exit(app.exec_())
