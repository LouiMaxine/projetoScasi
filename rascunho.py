if(self.nome_txt.text()=='' and self.senha_txt.text()== ''):
    QMessageBox.warning(QMessageBox(),"AVISO!", 'Os campos usuário e cadastro devem ser preenchidos para prosseguir.')
else:



if(self.nome_txt.text()=='' or self.senha_txt.text()== ''):
    QMessageBox.warning(QMessageBox(),"AVISO!", 'Os campos usuário e cadastro devem ser preenchidos para prosseguir.')
    conn = pymysql.connect("localhost","root","","registroalunos")#Vai no banco de dados
    cur= conn.cursor()#Pesquisa
    cur.execute("SELECT count(*) FROM usuarios")
    resultado = cursor.fetchone()

    if resultado[0] !=1:
        cur.execute("INSERT INTO usuarios(usuario,passwd)VALUES(%s,%s)",(us,pswd))
        conn.commit()
        cur.close()
        conn.close()
        self.nome_txt.clear()
        self.senha_txt.clear()

        QMessageBox.information(QMessageBox(),'Cadastro','Cadastro de usuário realizado com sucesso!')
    else:
        QMessageBox.warning(QMessageBox(),'br07louise@hotmail.com','O Cadastro já foi realizado, preencha os campos corretamente e aperte em Login.')
