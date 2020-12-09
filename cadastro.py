import mysql.connector

nome = input("Digite o nome: ")
idade = input("Digite a idade: ")



#================PERSISTÊNCIA========================

def conectarAoBanco():
    banco = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="testecli"
        )
    return banco

def gravarDadosDoCliente(nm,id):
    try:
        db = conectarAoBanco()
        cursor = db.cursor()

        sql = "INSERT INTO dadospessoais (nome, idade) VALUES (%s, %s)"
        val= (nm, id)

        cursor.execute(sql, val)
        db.commit()

        db.close
        cursor.close()
        print("Cadastro efetuado com sucesso!")
    except BaseException as erro:
        print("Deu erro: " + str(erro))

gravarDadosDoCliente(nome,idade)
