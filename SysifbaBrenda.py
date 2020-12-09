import mysql.connector
import time
import os

meu_db = ('sysfba',)#podem ser adicionados mais bancos de dados, contando que especifique durante o programa a posição [0]zero

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
    status = False #isso só serve para dizer se tá conectado ou não
    try:
        db = conecta_db()
        cursor = db.cursor() #ele conecta o bd com o python

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
    print("Configurando o sistema. Aguarde!")
    time.sleep(5)
    os.system("cls")
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

        sql = "CREATE TABLE usuarios (id INT AUTO_INCREMENT PRIMARY KEY, usuario VARCHAR(20), passwd VARCHAR(10))"
        cursor.execute(sql)

        sql = "CREATE TABLE clientes (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), endereco VARCHAR(255))"
        cursor.execute(sql)

        sql= "INSERT INTO usuarios(usuario,passwd) VALUES(%s,%s)"
        val=("admin", "admin")
        cursor.execute(sql,val)

        db.commit()
        db.close
        cursor.close()
        print("Tabela criada com sucesso!")

    except BaseException as erro:
        print("Erro na criação de tabela" + str(erro))

def valida_usuario(us=None,pw=None):#para criar o primeiro usuario, valida o administrados e depois ele permite a entrada de qualquer usuario
    if us ==None:#quando não tiver valor, vou logar para entrar no sistema
        try:
            db = conecta_db(meu_db[0])
            cursor = db.cursor()

            cursor.execute('SELECT count(*) FROM usuarios')#ESSE COMANDO CONTA TDS OS REGISTROS QUE EU TENHO DO USUARIO

            resultado = cursor.fetchone()#pega a tabela resposta do banco e armazena em resultado

            if resultado[0] == 1:#Caso o n sei o q seja só uma
                print('Esse é o primeiro acesso!')
                print('Insira os dados do Administrador')
                user = input('Login: ')
                pswd = input('Senha: ')

                sql = 'SELECT * FROM usuarios WHERE usuario LIKE %s'#selecione tudo na tabela usuario quando o usuario se parecer com user
                 #só vai retornar qualquer resp se o usuario acertar qualquer valor dentro do banco
                val = (user,)

                cursor.execute(sql,val)

                usuarios = cursor.fetchone()

                if usuarios is not None and usuarios[2]==pswd:#posição dois é onde está a informação da senha dentro de usuarios
                    print('Acesso Liberado!')
                    user = input('Novo usuário: ')
                    pswd = input('Senha: ')

                    sql = 'INSERT INTO usuarios (usuario, passwd) VALUES (%s,%s)'
                    val = (user, pswd)

                    cursor.execute(sql, val)

                    db.commit()#salvar as alterações do INSERT
                else:#caso haja mais de um usuário
                    print('Aceso negado!')
                    return False#não vai fazer sentido, mas no futuro a gente já pegar e ...

            else:
                user = input('Login: ')
                pswd = input('Senha: ')

                sql = 'SELECT * FROM usuarios WHERE usuario LIKE %s'
                val = (user,)

                cursor.execute(sql,val)

                usuarios = cursor.fetchone()

                if usuarios is not None and usuarios[2]==pswd:
                    return True
                else:
                    print('Usuário ou senha inválidos')

        except BaseException as erro:
            print('Erro validando usuario: '+ str(erro))
        finally: # comando que vai sempre vai executar independente de except ou try
            cursor.close()
            db.close()
    else:
        pass

def cadastrar_cliente(n = None, e = None):#a função pega o nome e coloca em n, e o endereço em e. Joga no banco de dados
        try:
            db = conecta_db(meu_db[0])
            cursor = db.cursor()

            sql = 'INSERT INTO clientes(nome, endereco) VALUES(%s,%s)'#pode chamar a variavel do q quiser(comando de alteração do banco tem que dar commit)#CONECTA - cria o cursor
            val = (n,e)

            cursor.execute(sql,val)

            db.commit()#salva os dados do banco
            input('Cliente cadastrado com sucesso! [ENTER] para continuar')#O programa para aqui, e o enter é somente para guiar o usuário a continuar o programa
        except BaseException as erro:#tudo que pode dar errado no program pode ser adicionado ao exception; Para saber, consultar a doc oficial da linguagem
            print('Erro no cadastro do cliente. ', str(erro))
            input('[ENTER] para continuar')
        finally:
            cursor.close()
            db.close()

def editar_cliente(n = None):
    try:
        db = conecta_db(meu_db[0])
        cursor = db.cursor()

        sql = 'SELECT * FROM clientes WHERE nome = %s'
        val = (n,)

        cursor.execute(sql,val)
        resultado = cursor.fetchall()

        if len(resultado) > 0:
            for r in resultado:
                print(r)
                print("_"*40)
            print('Para manter os valores atuais, apenas pressione [ENTER]')
            n = input('Novo nome: ')
            e = input('Novo endereço: ')

            if len(n) > 0 and len(e)>0:#Quando o usuário apertar enter, o espaço que ele nao digitar vai ser igual a nada
                sql = 'UPDATE clientes SET nome = %s, endereco = %s WHERE clientes.id = ' + str(r[0]) #r na posição zero, é o id do banco de dados. mas preciso mostrar o dado da tupla, sem aspas. Por isso usa a string na posição
                val = (n,e)
                cursor.execute(sql, val)
                db.commit()
            elif len(n)>0 and len(e)==0:
                sql = 'UPDATE clientes SET nome = %s WHERE clientes.id = ' + str(r[0])
                val = (n,)
                cursor.execute(sql, val)
                db.commit()
            elif len(n)==0 and len(e)>0:
                sql = 'UPDATE clientes SET endereco = %s WHERE clientes.id = ' + str(r[0])
                val = (e,)
                cursor.execute(sql, val)
                db.commit()
            else:
                print('Nenhum dado foi alterado')
        else:
            print('Nenhum dado foi encontrado')
        input('Pressione [Enter] para continuar...')
    except BaseException as erro:
        print('Erro ao editar\n',str(erro))
        input('Pressione [ENTER] para continuar...')
    finally:
        cursor.close()
        db.close()


def pesquisar_cliente(n = None):
    try:
        db = conecta_db(meu_db[0])
        cursor = db.cursor()

        sql = "SELECT * FROM clientes WHERE nome LIKE '%"+ n+ "%'"  #ASTERISCO significa tudo no sistema operacional;
        #% a porcentagem faz parte da quare; Tem que usar a concatenação, pq nesse caso não funciona;
        #Nesse código de sql, não pode usar aspas simples para escrever o código, somente antes e dps das porcentagens
        cursor.execute(sql)
        resultado = cursor.fetchall()
        for r in resultado:
            print(r)
            print('_'*50)
        input('Pressione [Enter] para continuar...')#Todo o código é o mesmo só muda o sql dentro das funções
    except BaseException as erro:#os erros são gravados em logs de sistema em txt
        print('Erro na pesquisa do Cliente', str(erro))
        input('[ENTER] para continuar.')
    finally:
        cursor.close()
        db.close()

def excluir_cliente(n = None):
    try:
        db = conecta_db(meu_db[0])
        cursor = db. cursor()

        sql = "SELECT * FROM clientes WHERE  nome = %s"
        val = (n,) #precisa da vírgula, senão não cria tupla

        cursor.execute(sql,val)
        resultado = cursor.fetchall()#tem que ser ftchal, pois pode ter mais de uma pessoa com o mesmo Nome

        if len(resultado) > 0:#se o tamanho do resultado for maior do q zer, eu EXCLUO
            for r in resultado:
                print(r)
                print('-'*50)
            print('Atenção, os dados excluídos, não podem ser recuperados!')
            op = input('Tem certeza que deseja excluir o cliente? [S/N]')
            if op.lower() == 's':
                sql = 'DELETE FROM clientes WHERE clientes.id = ' + str(r[0]) #precisa de um dado específico, e quanto menor, melhor, por isso vamos usar o id como referência. O id está na posição 0
                cursor.execute(sql)
                db.commit()
                input('Cliente excluído com sucesso. [ENTER] para continuar.')
            else:
                print('Nenhuma alteração foi realizada!')
        else:#se o contrário, mensagem
            print('Cliente não encontrado!')
    except BaseException as erro:
        print('Erro excluindo cliente.' , str(erro))
        input('[ENTER] para continuar')
    finally:
        cursor.close()
        db.close()
def exibir_cliente(n = None):#CONECTA - cria o cursor; Faz o específico; Fecha a conexão (padrão para tds as funções)
    try:
        db = conecta_db(meu_db[0])#para exibir todos os dados do banco
        cursor = db. cursor()

        sql = 'SELECT * FROM clientes'
        cursor. execute(sql)#EXISTEM TRÊS FeT- precisa usar ele para converter a resp do sql para o python

        resultado = cursor.fetchall()

        for r in resultado: #laço com o interator
            print(r)
            print('_'*40)
        input('Pressione [ENTER] para continuar')
    except BaseException as erro:
        print('Erro exibindo cliente.',str(erro))#Lembrar de especificar o Erro
        input('Pressione [Enter] para continuar...')
    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    op = -1
    valida = False

    while op != 0: #zero pq eu define q é o q o usuario digita para sair do sistema
        if not existe_db():
            criar_db()
        else:
            valida = valida_usuario()
            while valida == True:
                os.system('cls')
                print('|================== SYSFBA 0.1===================== |')
                print('|  [1]-CADASTRAR CLIENTE                            |')
                print('|  [2]-EDITAR DADOS DO CLIENTE                      |')
                print('|  [3]-PESQUISAR CLIENTE                            |')
                print('|  [4]-EXCLUIR CLIENTE                              |')
                print('|  [5]-RELATÓRIO DE CLIENTES                        |')
                print('|  [0]-SAIR                                         |')
                op = int(input('> '))

                if op ==1:
                    os.system('cls')
                    print('===========> CADASTRANDO CLIENTE')
                    nome = input('Nome: ') #porque precisa dessas informações dentro do banco de dados que fizemos
                    endereco = input('Endereço: ')
                    cadastrar_cliente(nome,endereco)
                elif op ==2:
                    os.system('cls')
                    print('===========> EDITANDO CLIENTE')
                    nome = input('Nome: ')
                    editar_cliente(nome)
                elif op == 3:
                    os.system('cls')
                    print('===========> PESQUISANDO CLIENTE')
                    n = input('Nome: ')
                    pesquisar_cliente(n)
                elif op == 4:
                    os.system('cls')
                    print('===========> EXCLUINDO CLIENTE')
                    n = input('Nome:') #prefcisa saber qual é o cliente
                    excluir_cliente(n)
                elif op ==5:
                    os.system('cls')
                    print('===========> EXIBINDO CLIENTE')
                    exibir_cliente()
                elif op == 0:
                    os.system('cls')
                    print('SYSFBA finalizado com sucesso')
                    valida = False
                else:
                    print('Opção Inválida')
                    c = input('[Enter] para continuar')
