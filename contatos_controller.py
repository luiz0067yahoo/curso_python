
from flask import Flask,request,render_template,jsonify,session
from flask_cors import CORS
import json
import mysql.connector
from flask.sessions import SecureCookieSessionInterface



app = Flask(__name__)
app.secret_key = 'Senac$2023'
app.session_interface = SecureCookieSessionInterface()

CORS(app)


# Configuração do banco de dados MySQL
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='usbw',
    database='agenda'
)
db_cursor = db_connection.cursor()

@app.route('/create_table')
def create_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS contatos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        telefone VARCHAR(255) NOT NULL
    )
    """
    db_cursor.execute(create_table_query)
    db_connection.commit()
    return "Tabela de contatos criada com sucesso"

@app.route('/')
def formulario():
    return render_template('./FormularioContatosMysql.html')

@app.route('/contatos', methods=['GET'])
def listar():
    select_query = "SELECT * FROM contatos"
    db_cursor.execute(select_query)
    contatos = db_cursor.fetchall()
    contatos_list = []
    for contato in contatos:
        contato_dict = {
            "id": contato[0],
            "nome": contato[1],
            "telefone": contato[2]
        }
        contatos_list.append(contato_dict)
    return jsonify(contatos_list)




@app.route('/contatos/<int:id>')
def listarPorId(id):
    resultado=""
    return str(resultado)




@app.route('/contatos', methods=['POST'])
def criar():
    data = request.get_json()
    if data:
        nome = data.get('nome')
        telefone = data.get('telefone')
        insert_query = "INSERT INTO contatos (nome, telefone) VALUES (%s, %s)"
        db_cursor.execute(insert_query, (nome, telefone))
        db_connection.commit()
        return jsonify({"success": "Contato criado com sucesso"})
    else:
        return jsonify({"error": "Dados inválidos"}), 400
    


@app.route('/contatos/<int:id>', methods=['PUT'])
def alterar(id):
    data = request.get_json()
    if data:
        nome = data.get('nome')
        telefone = data.get('telefone')
        update_query = "UPDATE contatos SET nome = %s, telefone = %s WHERE id = %s"
        db_cursor.execute(update_query, (nome, telefone, id))
        db_connection.commit()
        if db_cursor.rowcount > 0:
            return jsonify({"success": "Contato atualizado com sucesso"})
        else:
            return jsonify({"error": "Contato não encontrado"}), 404
    else:
        return jsonify({"error": "Dados inválidos"}), 400

    
    

@app.route('/contatos/<int:id>', methods=['DELETE'])
def deletar(id):
    delete_query = "DELETE FROM contatos WHERE id = %s"
    db_cursor.execute(delete_query, (id,))
    db_connection.commit()

    if db_cursor.rowcount > 0:
        return jsonify({"success": f"Contato com ID {id} excluído com sucesso"})
    else:
        return jsonify({"error": "Contato não encontrado"}), 404




if __name__ == '__main__':
    app.run(debug=True)