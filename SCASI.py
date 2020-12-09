from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import *
import pymysql
import sys
import mysql.connector
import time
import os


class CadastroAluno (QDialog):#Terceira etapa -Criação do Formulário do Aluno
    def __init__(self,*args,**kwargs):
        super(CadastroAluno, self).__init__(*args,**kwargs)

        self.btn_cadastrar = QPushButton()
        self.btn_cadastrar.setText("REGISTRAR")
        font = self.btn_cadastrar.font()
        font.setBold(True)
        self.btn_cadastrar.setFont(font)

        self.setWindowTitle("Add Aluno: ")
        self.setWindowIcon (QIcon('icon/add1.png'))
        self.setStyleSheet("background-color: rgb(230, 242, 255)")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.btn_cadastrar.clicked.connect(self.AddAluno)

        layout = QVBoxLayout()


        #=========CAIIXAS DE TEXTO DOS DADOS==================#

        self.nome_inp = QLineEdit()
        self.nome_inp.setPlaceholderText("Nome: ")
        layout.addWidget(self.nome_inp)

        self.tipo_curso = QComboBox()
        self.tipo_curso.addItem("Licenciatura em Matemática")
        self.tipo_curso.addItem("Licenciatura em Computação")
        self.tipo_curso.addItem("Análise e Desenvolvimento de Sistemas")

        layout.addWidget(self.tipo_curso)

        self.input_semestre = QComboBox()
        self.input_semestre.addItem("Semestre: 1")
        self.input_semestre.addItem("Semestre: 2")
        self.input_semestre.addItem("Semestre: 3")
        self.input_semestre.addItem("Semestre: 4")
        self.input_semestre.addItem("Semestre: 5")
        self.input_semestre.addItem("Semestre: 6")
        self.input_semestre.addItem("Semestre: 7")
        self.input_semestre.addItem("Semestre: 8")

        layout.addWidget(self.input_semestre)


        self.tel_txt = QLineEdit()
        self.tel_txt.setPlaceholderText("Telefone Nº: ")
        self.somente_num = QIntValidator() #Biblioteca que faz o campo aceitar só num inteiro, e não por extenso
        self.tel_txt.setValidator(self.somente_num)
        layout.addWidget(self.tel_txt)

        self.endereco_txt = QLineEdit()
        self.endereco_txt.setPlaceholderText("Endereço: ")
        layout.addWidget(self.endereco_txt)

        layout.addWidget(self.btn_cadastrar)
        self.setLayout(layout)


    def AddAluno(self):
        nome =""
        curso = ''
        sem = -1
        tel = ""
        endereco = ""

        nome = self.nome_inp.text()
        curso = self.tipo_curso.itemText(self.tipo_curso.currentIndex())
        sem = self.input_semestre.itemText(self.input_semestre.currentIndex())
        tel1 = self.tel_txt.text()
        endereco = self.endereco_txt.text()

        if(self.nome_inp.text()=='' or self.tel_txt.text()== '' or self.endereco_txt.text()==''):
            QMessageBox.warning(self,"AVISO!", 'Por favor, preencha todos os campos \npara efetuar o cadastro.')

        else:
            try:
                conn = pymysql.connect("localhost","root","","registroalunos")
                cur= conn.cursor()
                cur.execute("INSERT INTO estudantes(nome,nomecurso,semestre,tel,endereco)VALUES(%s,%s,%s,%s,%s)",(nome,curso,sem,tel1,endereco))
                conn.commit()
                cur.close()
                conn.close()

                QMessageBox.information(self,'Cadastro','Cadastro do aluno realizado com sucesso!')
                self.close()

            except Exception:
                QMessageBox.warning(self,'br07louise@hotmail.com','Não foi possível realizar o cadastro, verifique se os campos foram preenchidos corretamente.')


class PesquisarAluno(QDialog):#Quarta etapa
    def __init__(self,*args,**kwargs):
        super(PesquisarAluno, self).__init__(*args,**kwargs)

        self.btn_pesquisa_aln = QPushButton()
        self.btn_pesquisa_aln.setText("PESQUISAR")
        font = self.btn_pesquisa_aln.font()
        font.setBold(True)
        self.btn_pesquisa_aln.setFont(font)

        self.setWindowTitle("Pesquisar Aluno ")
        self.setWindowIcon (QIcon('icon/s3.png'))
        self.setStyleSheet("background-color: rgb(179, 255, 179)")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        self.btn_pesquisa_aln.clicked.connect(self.pesquisandoAluno)

        layout = QVBoxLayout()

        #=========CAIIXAS DE TEXTO DOS DADOS==================#

        self.pesquisando_txt = QLineEdit()
        self.somente_num = QIntValidator()
        self.pesquisando_txt.setValidator(self.somente_num)
        self.pesquisando_txt.setPlaceholderText("Inscrição Nº: ")
        layout.addWidget(self.pesquisando_txt)

        layout.addWidget(self.btn_pesquisa_aln)
        self.setLayout(layout)

    def pesquisandoAluno(self):
        pesq = ""
        pesq = self.pesquisando_txt.text()

        try:
            conn = pymysql.connect("localhost","root","","registroalunos")
            cur= conn.cursor()
            cur.execute("SELECT * FROM estudantes WHERE id = "+str(pesq))
            row = cur.fetchone() #trazer o pacote de informação(algumas info, por isso one); O row é para distribuir as info em linhas
            result_pesq = "Inscrição Nº: "+str(row[0])+'\n'+"Nome: " +str(row[1])+'\n'+"Curso: "+str(row[2])+'\n'+"Semestre: "+str(row[3])+'\n'+"Telefone: "+str(row[4])+'\n'+"Endereço: "+str(row[5])#distribuir a info na tabela
            QMessageBox.information(self,'Pesquisa realizada com sucesso!',result_pesq)
            conn.commit()
            cur.close()
            conn.close()

        except Exception:
            QMessageBox.warning(self,'br07louise@hotmail.com','Não foi possível realizar a pesquisa, verifique se o número da inscrição está correto')


class Deletar(QDialog):#Quinta etapa
    def __init__(self,*args,**kwargs):
        super(Deletar, self).__init__(*args,**kwargs)

        self.btn_del_aln = QPushButton()
        self.btn_del_aln.setText("DELETAR")
        font = self.btn_del_aln.font()
        font.setBold(True)
        self.btn_del_aln.setFont(font)

        self.setWindowTitle("Deletar Inscrição:")
        self.setWindowIcon (QIcon('icon/d1.png'))
        self.setStyleSheet("background-color: rgb(255, 255, 179)")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        self.btn_del_aln.clicked.connect(self.deletando)

        layout = QVBoxLayout()

        #=========CAIIXAS DE TEXTO DOS DADOS==================#

        self.deleta_txt = QLineEdit()
        self.del_somente_num = QIntValidator()
        self.deleta_txt.setValidator(self.del_somente_num)
        self.deleta_txt.setPlaceholderText("Inscrição Nº: ")
        layout.addWidget(self.deleta_txt)

        layout.addWidget(self.btn_del_aln)
        self.setLayout(layout)

    def deletando(self):
        del1 = ""
        del1 = self.deleta_txt.text()

        try:
            conn = pymysql.connect("localhost","root","","registroalunos")
            cur= conn.cursor()
            cur.execute("DELETE FROM estudantes WHERE id = "+str(del1))
            conn.commit()
            cur.close()
            conn.close()

            QMessageBox.information(self,'br07louise@hotmail.com', 'Inscrição deletada com sucesso!')
            self.close()
        except Exception:
            QMessageBox.warning(self,'br07louise@hotmail.com','Não foi possível deletar, verifique se o número da inscrição está correto')


class SobreAjuda (QDialog):#Segunda etapa
    def __init__(self,*args,**kwargs):
        super(SobreAjuda, self).__init__(*args,**kwargs)#Config da janela de Desenvolvedor

        self.setFixedWidth(300)#fixa largura da janela
        self.setFixedHeight(400)#fixa altura da janela

        #==========#CRIANDO A CAIXA DAS INFO#==============#
        btn_defi_desenv = QDialogButtonBox.Ok #botão tipo caixa
        self.buttonBox = QDialogButtonBox(btn_defi_desenv)
        self.buttonBox.accepted.connect (self.accept)#Quando clicar no botão ele vai aceitar e abrir
        self.buttonBox.rejected.connect (self.reject)#Para/Fecha

        layout = QVBoxLayout()

        self.setWindowTitle("Sobre - SCASI")
        self.setWindowIcon (QIcon('icon/i1.png'))
        title = QLabel('''  Sistema de Cadastro
   Alunos do Superior
 IFBA Campus Valença''')
        font = title.font()#Recebendo a fonte do título
        font.setPointSize(20)
        title.setFont(font)#Recendo o subtítulo


        #================#Colocando imagem no layout#========================#
        lbl_imagem = QLabel()#Uma variável, atribuida a um label#Precisa especificar uma altura pro label
        pixmap = QPixmap('icon/san.png')#Uma variável recebendo o campo pixmap
        pixmap = pixmap.scaledToWidth(150)#Recebendo a largura
        lbl_imagem.setPixmap(pixmap)#Especifica que vai receber a mesma altura da foto
        lbl_imagem.setFixedHeight(150)

        layout.addWidget(title)
        layout.addWidget(QLabel("v2.O"))
        layout.addWidget(QLabel("Copyright Louise Cerqueira 2019"))
        layout.addWidget(lbl_imagem)
        layout.addWidget(self.buttonBox)#Fechar o formulário chamando-o
        self.setLayout(layout)


class Login(QDialog):
    def __init__(self, parent = None):
        super(Login,self).__init__(parent)

        self.setFixedWidth(405)
        self.setFixedHeight(300)

        self.lbl_nome_usu =QLabel("Usuário:")
        self.lbl_senha = QLabel("Senha:")

        self.nome_txt = QLineEdit(self)
        self.senha_txt = QLineEdit(self)
        self.senha_txt.setEchoMode(QLineEdit.Password)

        self.btn_Login = QPushButton("Login",self)
        self.btn_CadUsuario = QPushButton("Primeiro Acesso? Cadastre-se! ",self)
        self.btn_Login.clicked.connect(self.valida_usuario)
        self.btn_CadUsuario.clicked.connect(self.cadastrodeusuario)


        font = QFont()
        font.setPointSize(100)
        font.setBold(True)
        font.setWeight(75)

        layout = QGridLayout(self)
        layout.addWidget(self.lbl_nome_usu,2,1)
        font4 = self.lbl_nome_usu.font()
        font4.setPointSize(14)
        self.lbl_nome_usu.setFont(font4)
        layout.addWidget(self.lbl_senha,3,1)
        font5 = self.lbl_senha.font()
        font5.setPointSize(14)
        self.lbl_senha.setFont(font5)

        self.lbl_boas = QLabel('''Bem Vindo
        ao
        SCASI!''')
        layout.addWidget(self.lbl_boas,1,1)
        font = self.lbl_boas.font()
        font.setPointSize(15)
        self.lbl_boas.setFont(font)


        layout.addWidget(self.nome_txt,2,2)
        font2 = self.nome_txt.font()
        font2.setPointSize(12)
        self.nome_txt.setFont(font2)
        layout.addWidget(self.senha_txt,3,2)
        font3 = self.senha_txt.font()
        font3.setPointSize(12)
        self.senha_txt.setFont(font3)
        layout.addWidget(self.btn_Login,7, 2)#localizar o botão
        font6 = self.btn_Login.font()
        font6.setBold(True)
        font6.setPointSize(11)
        self.btn_Login.setFont(font6)
        layout.addWidget(self.btn_CadUsuario,8, 2)
        font9 = self.btn_CadUsuario.font()
        font9.setBold(True)
        font9.setPointSize(11)
        self.btn_CadUsuario.setFont(font9)


        self.setWindowTitle('Sistema de Cadastro de Alunos Superior IFBA - SCASI')
        self.setWindowIcon (QIcon('icon/panda_login.png'))


        self.lbl_vindas = QLabel(self)
        self.lbl_vindas.resize(150,150)
        self.lbl_vindas.move(210,20)
        self.lbl_vindas.setScaledContents(True)
        self.lbl_vindas.setPixmap(QPixmap('icon/panda_login.png'))

    def cadastrodeusuario(self):
        us =""
        pswd = ''

        us = self.nome_txt.text()
        pswd = self.senha_txt.text()
        try:
            if(self.nome_txt.text()=='' or self.senha_txt.text()== ''):
                QMessageBox.warning(self,"AVISO!", 'Preencha os campos usuário e senha com os caracteres \nde sua preferência, para efetuar o cadastro.')
            else:
                conn = pymysql.connect("localhost","root","","registroalunos")#Vai no banco de dados
                cur= conn.cursor()#Pesquisa
                cur.execute("SELECT count(*) FROM usuarios")
                resultado = cur.fetchone()

                if resultado[0] !=1:
                    cur.execute("INSERT INTO usuarios(usuario,passwd)VALUES(%s,%s)",(us,pswd))
                    conn.commit()
                    cur.close()
                    conn.close()
                    self.nome_txt.clear()
                    self.senha_txt.clear()

                    QMessageBox.information(self,'Cadastro','Cadastro de usuário realizado com sucesso!')
                else:
                    QMessageBox.warning(self,'br07louise@hotmail.com','Você já foi cadastrado, preencha os campos \ncom usuário e senha válidos e aperte em Login.')


        except Exception:
            QMessageBox.warning(self,'br07louise@hotmail.com','Não foi possível realizar o cadastro, verifique se os campos foram preenchidos.')


    def valida_usuario(self):
        user = self.nome_txt.text()
        pswd = self.senha_txt.text()

        try:
            conn = pymysql.connect("localhost", "root", "", "registroalunos")

            with conn:
                cur = conn.cursor()
                cur.execute('SELECT count(*) FROM usuarios')

                resultado = cur.fetchone()
                tst1 = False
                tst2 = False

                if resultado[0] == 1:
                    sql = 'SELECT * FROM usuarios'
                    cur.execute(sql)
                    usuarios = cur.fetchone()

                    if user == usuarios[1]:
                        tst1 = True

                    if pswd == usuarios[2]:
                        tst2 = True

                if tst1 and tst2 == True:
                    self.accept()
                else:
                    QMessageBox.warning(self,'br07louise@hotmail.com:',
                                        'Usuário não cadastrado \n ou erro ao inserir os dados.')

        except BaseException as erro:
                MessageBox.warning(self,'br07louise@hotmail.com:',
                                    'Erro ao validar' + str(erro))
        finally:
                cur.close()


class MainWindow (QMainWindow):#Primeira etapa
    def __init__(self,*args,**kwargs):
        super(MainWindow, self).__init__(*args,**kwargs)
        self.setWindowIcon (QIcon('icon/g2.png'))

        #==========#INSERIR SUBTÍTULOS#==============#
        file_menu = self.menuBar().addMenu("&File")
        ajuda_menu = self.menuBar().addMenu("&Ajuda")
        self.setWindowTitle ("SCASI - Campus Valença:")
        self.setMinimumSize(800,600)#ajuste do tamanho da tela; ADD título e subtítulo
        self.setStyleSheet("background-color: rgb(230, 204, 255)")

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
        self.setStatusBar(barra_status)#inserindo barra de status abaixo da tela

        btn_addaluno = QAction(QIcon("icon/add1.png"),"Add Aluno",self) #botão para adicionar os alunos
        btn_addaluno.triggered.connect(self.cadastrar_alunos)#Para ativar o botão
        btn_addaluno.setStatusTip("Add Aluno")#Para não ficar o título, mas só o botão com a imagem
        toolbar.addAction(btn_addaluno)#Pede para ser inserido na variável
        file_menu.addAction(btn_addaluno)#Adiciona o botão dentro da opção file

        btn_atualizar = QAction(QIcon("icon/r3.png"),"Atualizar",self)
        btn_atualizar.triggered.connect(self.carregar_dados)
        btn_atualizar.setStatusTip("Atualizar Dados na Tabela")
        toolbar.addAction(btn_atualizar)

        btn_pesquisar = QAction(QIcon("icon/s3.png"),"Pesquisar",self)
        btn_pesquisar.triggered.connect(self.pesquisa)
        btn_pesquisar.setStatusTip("Pesquisar aluno")
        toolbar.addAction(btn_pesquisar)
        file_menu.addAction(btn_pesquisar)

        btn_deletar = QAction(QIcon("icon/d1.png"),"Deletar",self)
        btn_deletar.triggered.connect(self.delete)
        btn_deletar.setStatusTip("Deletar cadastro do aluno")
        toolbar.addAction(btn_deletar)
        file_menu.addAction(btn_deletar)

        sobre_desenv = QAction(QIcon("icon/i1.png"),"Desenvolvedor",self)#Para criar o menu de ajuda
        sobre_desenv.triggered.connect(self.sobre)
        ajuda_menu.addAction(sobre_desenv)


    def carregar_dados(self):#nem sei como deu certo (uma semana de depressão e tentativas)
        conn = pymysql.connect("localhost", "root", "", "registroalunos")

        with conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM estudantes')

        self.tableWidget.setRowCount(0)
        for row_number,row_data in enumerate(cur):#Para percorrer as linhas
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):#percorrer as colunas
                self.tableWidget.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        conn.close()


    def pesquisa(self):
        dlg = PesquisarAluno()
        dlg.exec_()


    def delete(self):
        dlg = Deletar()
        dlg.exec_()


    def cadastrar_alunos(self):#Cadastrar alunos
        dlg = CadastroAluno()
        dlg.exec_()


    def sobre(self):#função paraabrir aba de info sobre desenvolvedor
        desenv = SobreAjuda()
        desenv.exec_()


meu_db = ('registroalunos',)
def conecta_db(db=None):
    if db == None:
        banco = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd=""
                )
        return banco
    else:
        banco = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database=db
                )
        return banco


def existe_db():
    status = False
    try:
        db = conecta_db()
        cursor = db.cursor()

        cursor.execute("SHOW DATABASES")

        for banco in cursor:
            if banco == meu_db:
                status = True
        cursor.close()
        db.close()
    except BaseException as erro:
        print("Erro ao testar Banco: " + str(erro))
    return status


def criar_db():
    try:
        db = conecta_db()
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE " + meu_db[0])
        cursor.close()
        db.close()
        criar_tabelas()
    except BaseException as erro:
        print("Erro na criação do banco" + str(erro))


def criar_tabelas():
    try:
        db = conecta_db(meu_db[0])
        cursor = db.cursor()

        sql = "CREATE TABLE usuarios (id INT AUTO_INCREMENT PRIMARY KEY, usuario VARCHAR(20), passwd VARCHAR(10))DEFAULT CHARACTER SET utf8"
        cursor.execute(sql)

        sql = "CREATE TABLE estudantes (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255) NOT NULL, nomecurso VARCHAR(100),semestre VARCHAR(25),tel BIGINT(14),endereco VARCHAR(255) NOT NULL)DEFAULT CHARACTER SET utf8"
        cursor.execute(sql)
        db.commit()
        db.close
        cursor.close()

    except BaseException as erro:
        print("Erro na criação de tabela" + str(erro))


##########CRIAÇÃO DE DB MYSQL#####################
if not existe_db():
    criar_db()

app = QApplication(sys.argv)
if (QDialog.Accepted == True):
    login = Login()
    login.show()

    if login.exec_() == QDialog.Accepted:
        window = MainWindow()
        window.show()
        window.carregar_dados()
    sys.exit(app.exec_())
