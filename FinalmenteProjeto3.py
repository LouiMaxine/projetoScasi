from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
import pymysql
import sys
import mysql.connector
import time

class Login(QDialog):
    def __init__(self, parent = None):
        super(Login,self).__init__(parent)

        lbl_imagem = QLabel()#Uma variável, atribuida a um label#Precisa especificar uma altura pro label
        pixmap = QPixmap('icon/san.png')#Uma variável recebendo o campo pixmap
        pixmap = pixmap.scaledToWidth(150)#Recebendo a largura
        lbl_imagem.setPixmap(pixmap)#Especifica que vai receber a mesma altura da foto
        lbl_imagem.setFixedHeight(150)

        self.lbl_nome_usu =QLabel("Usuário:")
        self.lbl_senha = QLabel("Senha:")
        self.nome_txt = QLineEdit(self)
        self.senha_txt = QLineEdit(self)

        self.btn_Login = QPushButton("Entrar",self)
        self.btn_Login.clicked.connect(self.gerar_login)

        layout = QGridLayout(self)
        layout.addWidget(self.lbl_nome_usu,1,1)#daqui
        layout.addWidget(self.lbl_senha,2,1)#até aqui layout do label

        layout.addWidget(self.nome_txt,1,2)
        layout.addWidget(self.senha_txt,2,2)
        layout.addWidget(self.btn_Login,3, 1, 1, 2)#localizar o botão

        self.setWindowTitle('Login!')

    def gerar_login(self):
            if(self.senha_txt.text()=="" or self.nome_txt.text()==""):
                aviso("Inválido", "Usuário ou Senha não pode ficar em branco")
            else:
                try:
                    db = conecta_db(meu_db[0])
                    cursor = db.cursor()
                    cursor.execute("SELECT count(*) FROM usuarios")
                    resultado = cursor.fetchone()

                    if resultado[0]==1:
                        aviso("Acesso", "Primeiro Acesso")
                        aviso("Acesso", "usuário: admin \n senha: admin")
                        user=self.nome_txt.text()
                        pswd=self.senha_txt.text()
                        sql = "SELECT * FROM usuarios WHERE usuario LIKE %s"
                        val = (user,)
                        cursor.execute(sql,val)
                        usuarios = cursor.fetchone()
                        if usuarios is not None and pswd == usuarios[2]:
                            aviso("LIBERADO","ACESSO LIBERADO")
                            aviso("AVISO","É RECOMENDADO CRIAR OUTRO USUÁRIO !")
                            aviso("Boas Vindas","Seja Bem vindo!")
                            '''window.close()
                            j_valida.close()
                            self.arquivo.close()
                            telainicial()'''

                        else:
                            aviso("AVISO","Acesso Negado !")
                    else:
                        user=self.nome_txt.text()
                        pswd=self.senha_txt.text()
                        sql="SELECT * FROM usuarios WHERE usuario LIKE %s"
                        val=(user,)
                        cursor.execute(sql, val)
                        usuarios = cursor.fetchone()
                        if (usuarios is not None and usuarios[2] == pswd):
                            aviso("Boas Vindas","Seja Bem vindo ao ProdSale !")
                            '''window.close()
                            j_valida.close()
                            self.arquivo.close()
                            telainicial()'''

                            return True
                        else:
                            aviso("AVISO","USUÁRIO OU SENHA INVÁLIDOS")

                except BaseException as erro:
                    aviso("AVISO","ERRO AO VALIDAR USUÁRIO:"+str(erro)+"!")
                finally:
                    cursor.close()
                    db.close()


class MainWindow (QMainWindow):#Primeira etapa
    def __init__(self,*args,**kwargs):
        super(MainWindow, self).__init__(*args,**kwargs)
        self.setWindowIcon (QIcon('icon/g2.png'))

        file_menu = self.menuBar().addMenu("&File")
        ajuda_menu = self.menuBar().addMenu("&Ajuda")
        self.setWindowTitle ("CADASTRO DE ALUNOS DE PYQT5:")
        self.setMinimumSize(800,600)#ajuste do tamanho da tela; ADD título e subtítulo

        #==========#INSERIR TABELA#==============#
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)#Seleciona com mudança de cor
        self.tableWidget.setColumnCount(6)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)#Para o usuário não modificar as colunas
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)#Quando o texto estiver entrando na coluna ele vai esticar de acordo com o tamanho do nome

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("Inscrição Nº","Nome","Curso","Semestre","Telefone","Endereço"))

        #==========#BOTÕES E ÍCONES#==============#
        toolbar = QToolBar()#variável
        toolbar.setMovable(False)#Para que seja fixa, e o usuário não mexa
        self.addToolBar(toolbar)#Self adiciona a tabela no meu formulário

        barra_status = QStatusBar()
        self.setStatusBar(barra_status)#inserido barra de status abaixo da tela



app = QApplication(sys.argv)#Daqui
if (QDialog.Accepted == True):
    window = Login()
    window.show()
    #window.carregar_dados()
sys.exit(app.exec_())
