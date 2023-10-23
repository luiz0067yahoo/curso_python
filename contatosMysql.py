from flask import Flask,request,render_template,jsonify,session#biblioteca flash
from flask_cors import CORS#liberar acesso as requisições por metodos put post get e delete
import json#manipulação de formato json
import random#reliza sorteios de números
from flask.sessions import SecureCookieSessionInterface#manipular sessão
import mysql.connector#conecta ao banco de dados

app = Flask(__name__)#criar o objeto da aplicação Flask
app.secret_key = 'Senac$2023'#atribui o senha da sessão
app.session_interface = SecureCookieSessionInterface()# configura a sessão

CORS(app)#libera acesso as requisições por metodos put post get e delete

db = mysql.connector.connect(#conecta ao banco de dados
    host="localhost",#endereço do servidor de banco de dados
    user="root",#usuario
    passwd="usbw",#senha
    database="agenda"#nome do banco de dados
)

cursor = db.cursor(dictionary=True)#é o classe responsavel por manipular os dados 
#em SQL

@app.route('/')#Rota inicial front end
def formulario():#funcao da rota
    return render_template('./FormularioContatosMysql.html')#exibe o template

@app.route('/formulario_grupo')#Rota inicial front end
def formulario_grupo():#funcao da rota
    return render_template('./FormularioGruposMysql.html')#exibe o template
#backend
@app.route('/contatos')
def listar():
    global cursor#variavel global do cursor
    cursor.execute("SELECT distinct c.id,c.id_grupo,c.nome,c.telefone,g.nome as grupo FROM contatos c left join grupos_contatos g on(g.id=c.id_grupo) ")# seleção de todos os dados
    contatos = cursor.fetchall()#listagem dos dados
    return jsonify(contatos)#resposta dos dados

@app.route('/contatos/<int:id>')
def listarPorId(id):
    global cursor
    cursor.execute("SELECT distinct c.id,c.id_grupo,c.nome,c.telefone,g.nome as grupo FROM contatos c left join grupos_contatos g on(g.id=c.id_grupo) WHERE id = %s", (id,))#seleção de apenas um contato
    contato = cursor.fetchone()
    return jsonify(contato)

@app.route('/contatos',methods=['POST'])
def criar():
    global db, cursor
    data = request.get_json()
    if data:
        cursor.execute("INSERT INTO contatos (id_grupo,nome, telefone) VALUES (%s, %s, %s)", (data.get('id_grupo'),data.get('nome'), data.get('telefone')))
        #cria um novo contato
        db.commit()
        return jsonify({"success": "Contato criado com sucesso"})
    else:
        return jsonify({"error": "Dados inválidos"}), 400

    
@app.route('/contatos/<int:id>',methods=['PUT'])
def alterar(id):
    global db, cursor
    data = request.get_json()
    if data:
        cursor.execute("UPDATE contatos SET id_grupo=%s,nome=%s, telefone=%s WHERE id=%s", (data.get('id_grupo'),data.get('nome'), data.get('telefone'), id))
        #atualizar um novo contato
        db.commit()
        return jsonify({"success": "Contato alterado com sucesso"})
    else:
        return jsonify({"error": "Dados inválidos"}), 400

'''
    ALTER TABLE contatos
    ADD CONSTRAINT fk_grupo_id
    FOREIGN KEY (id_grupo)
    REFERENCES grupos_contatos(id_grupo);
'''

@app.route('/contatos/<int:id>',methods=['DELETE'])
def deletar(id):
    global db, cursor
    cursor.execute("DELETE FROM contatos WHERE id = %s", (id,))
    #excluir um novo contato
    db.commit()
    return jsonify({"success": "Contato excluído com sucesso"})

#backend grupos
#backend
@app.route('/grupos')
def listar_grupo():
    global cursor#variavel global do cursor
    cursor.execute("SELECT g.id,g.nome,(select count(c.id) from contatos c where (c.id_grupo=g.id)) as filhos  FROM grupos_contatos g")# seleção de todos os dados
    grupos = cursor.fetchall()#listagem dos dados
    return jsonify(grupos)#resposta dos dados

@app.route('/grupos/<int:id>')
def listar_grupoPorId(id):
    global cursor
    cursor.execute("SELECT * FROM grupos_contatos WHERE id = %s", (id,))#seleção de apenas um contato
    grupo = cursor.fetchone()
    return jsonify(grupo)

@app.route('/grupos',methods=['POST'])
def criar_grupo():
    global db, cursor
    data = request.get_json()
    if data:
        cursor.execute("INSERT INTO grupos_contatos (nome) VALUES (%s)", (data.get('nome'),))
        #cria um novo contato
        db.commit()
        return jsonify({"success": "Grupo criado com sucesso"})
    else:
        return jsonify({"error": "Dados inválidos"}), 400

    
@app.route('/grupos/<int:id>',methods=['PUT'])
def alterar_grupo(id):
    global db, cursor
    data = request.get_json()
    if data:
        cursor.execute("UPDATE grupos_contatos SET nome=%s WHERE id=%s", (data.get('nome'), id))
        #atualizar um novo contato
        db.commit()
        return jsonify({"success": "Grupo alterado com sucesso"})
    else:
        return jsonify({"error": "Dados inválidos"}), 400

def count_contatos_grupo(id_grupo):
    global cursor  # variavel global do cursor
    cursor.execute("SELECT g.id, g.nome, (SELECT COUNT(c.id) FROM contatos c WHERE c.id_grupo=g.id) AS filhos FROM grupos_contatos g WHERE g.id = %s", (id_grupo,))
    grupo = cursor.fetchone()
    return grupo["filhos"]

@app.route('/grupos/<int:id>',methods=['DELETE'])
def deletar_grupo(id):
    global db, cursor
    if(count_contatos_grupo(id)>0):
        cursor.execute("DELETE FROM grupos_contatos WHERE id = %s", (id,))
        #excluir um novo contato
        db.commit()
        return jsonify({"success": "Grupo excluído com sucesso"})
    else:
        return jsonify({"success": "Grupo não pode excluído por que possui contatos"})

if __name__ == '__main__':
    app.run(debug=True)