#Neste arquivo aprendemos como abrir uma janela e configurar tamanho e ícones
#No vídeo 4 dessa série é possível aprender como formatar um botão
from PyQt5 import QtGui
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

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
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

app = QApplication(sys.argv)
janela = janela()
sys.exit(app.exec_())
