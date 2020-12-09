'''
upgrade do pip
NUMA MÁQUINA SEM PERMISSÃO DE ADM
python -m pip install -- upgrade pip --user
COM PERMISSÃO DE ADM
python -m pip install -- upgrade pip
instalar o PySide2
pip install PySide2 --user(para nós)
'''
import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QMainWindow
from PySide2.QtCore import QFile
from PySide2 import QtGui
from PySide2 import QtCore
window = None
class carrega_janela():#função chamada para carregar a outra janela(segunda janela); outra janela
    #é outro arquivo, precisa criar uma classe
    janela = None
    def __init__(self):#a classe precisa que vc chame para rodar; metodo construtor
        global janela
        self.jan = QtGui.qApp#janelas que dependem de outro para existir
        self.arquivo = QFile('SegundaJanelaDoBotaoAbreOutraJanela.ui')
        self.arquivo.open(QFile.ReadOnly)
        self.carrega = QUiLoader()
        janela = self.carrega.load(self.arquivo)
        self.arquivo.close()
        janela.show()


def carregar_janela02():#para transformar classe em instância (da segunda janela)
    j = carrega_janela()#cria um objeto/instância
if __name__=='__main__':
    app = QApplication(sys.argv)#o sys vai capturar qualquer linha do seu sistema
    ui_file=QFile('BtnAbreOutraJanela.ui')#trazer para dentro do código o arquivo .ui
    ui_file.open(QFile.ReadOnly)
    loader = QUiLoader()#carregar meu arquivo, gravar o arquivo dentro da variável window
    window = loader.load(ui_file)#classe é o meu arquivo original e instância é uma cópia dela que
        #vai rodar na memória RAM.

    window.btn_carregar.clicked.connect(carregar_janela02) #aqui está acessando o botão que está
        #dentro do window; e coloca o gatilho pra carregar janela02
    ui_file.close()#fecha a classe

    window.show()#pede para aparecer a janela
        #precisa fazer entrar num loop, para o python não encerrer aqui e, cima
    sys.exit(app.exec_())#Sempre acontece primeiro o que tá denro dos parênteses. #Enquanto o app
        #estver executando, o sistema não pode sair
