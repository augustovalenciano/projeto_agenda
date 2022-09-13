from PyQt5 import uic,QtWidgets
import mysql.connector

numero_id = 0

banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "agenda"
)

def acessar_login():
    login.label_4.setText("")
    nome_usuario = login.lineEdit.text()
    senha = login.lineEdit_2.text()
    if nome_usuario == "luisaugusto" and senha == "euamoaduda":
        login.close()
        formulario.show()
    else:
        login.label_4.setText("Dados Incorretos")

def editar_dados():
    global numero_id
    linha = segunda_tela.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM fazer")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM fazer WHERE id="+ str(valor_id))
    produto = cursor.fetchall()
    terceira_tela.show()

    terceira_tela.lineEdit.setText(str(produto[0][0]))
    terceira_tela.lineEdit_2.setText(str(produto[0][1]))
    terceira_tela.lineEdit_3.setText(str(produto[0][2]))
    terceira_tela.lineEdit_4.setText(str(produto[0][3]))
    numero_id = valor_id

def salvar():
    global numero_id
    materia = terceira_tela.lineEdit_2.text()
    oqfazer = terceira_tela.lineEdit_3.text()
    status = terceira_tela.lineEdit_4.text()
    cursor = banco.cursor()
    cursor.execute("UPDATE fazer SET materia = '{}', oqfazer = '{}', status = '{}' WHERE id = {}".format(materia,oqfazer,status,numero_id))
    banco.commit()
    terceira_tela.close()
    segunda_tela.close()
    chama_segunda_tela()

def excluir_dados():
    linha =segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM fazer")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM fazer WHERE id="+ str(valor_id))


def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()

    categoria = ""
    
    if formulario.radioButton.isChecked():
        print("Status: Feito")
        categoria = "Feito"
    elif formulario.radioButton_2.isChecked():
        print("Status: Vou Fazer")
        categoria = "Vou Fazer"
    else:
        print("Status: EM ATRASO")
        categoria = "EM ATRASO"

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO fazer (materia,oqfazer,status) VALUES (%s,%s,%s)"
    dados = (str(linha1),str(linha2),categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")

    print("A materia é:", linha1)
    print("oq tenho que fazer é:", linha2)

def chama_segunda_tela():
    segunda_tela.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM fazer"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(4)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 4):
           segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

app=QtWidgets.QApplication([])
formulario=uic.loadUi("primeira_tela.ui")
segunda_tela=uic.loadUi("segunda_tela.ui")
terceira_tela=uic.loadUi("terceira_tela.ui")
login=uic.loadUi("quarta_tela.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(excluir_dados)
segunda_tela.pushButton_2.clicked.connect(editar_dados)
terceira_tela.pushButton.clicked.connect(salvar)
login.pushButton.clicked.connect(acessar_login)
login.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
login.show()
app.exec()