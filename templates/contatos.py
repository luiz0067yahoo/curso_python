
from flask import Flask,request,render_template,jsonify,session
from flask_cors import CORS
import json
import random

app = Flask(__name__)
app.secret_key = 'Senac$2023'
CORS(app)

contatos=[]

@app.route('/')
def calculadora():
    return render_template('./FormularioContatos.html')

@app.route('/contatos')
def listar():
    global contatos
    contatos = session.get('contatos', [])
    return json.dumps(contatos)

@app.route('/contatos/<int:id>')
def listarPorId(id):
    resultado=""
    return str(resultado)

@app.route('/contatos',methods=['POST'])
def criar():
    global contatos
    contatos = session.get('contatos', [])
    data = request.get_json()  # Obtém os dados do corpo da requisição como um objeto JSON
    if data:
        # Cria um objeto JSON com os dados fornecidos
        contato = {
            "id": random.randint(1, 1000),
            "nome": data.get('nome'),
            "telefone": data.get('telefone')
        }
        contatos.append(contato)
        session["contatos"]=contatos
        return jsonify(contato)  # Retorna o objeto JSON como resposta
    else:
        return jsonify({"error": "Dados inválidos"}), 400  # Retorna um erro se os dados estiverem ausentes ou inválidos


@app.route('/contatos',methods=['PUT'])
def alterar():
    encontrado=False
    contatos = session.get('contatos', [])
    data = request.get_json()  # Obtém os dados do corpo da requisição como um objeto JSON
    if data:        
        for i in range(len(contatos)):
            resultado=str(len(contatos))
            contato=contatos[i]
            #resultado="\n"+str(contato.get('id'))+"\t"+str(data.get('id'))
            if contato.get('id') == data.get('id'):                
                contato = {
                    "id": data.get('id'),
                    "nome": data.get('nome'),
                    "telefone": data.get('telefone')
                }
                contatos[i]=contato
                session['contatos']=contatos
                encontrado=True
        if not(encontrado):
            return jsonify({"error": resultado+"Contato não encontrado"})
        else:
            return jsonify(contato)  # Retorna o objeto JSON como resposta
    else:
        return jsonify({"error": "Dados inválidos"}), 400  # Retorna u
    
    


@app.route('/contatos/<int:id>',methods=['DELETE'])
def deletar(id):
    contatos = session.get('contatos', [])
    nome_contato_removido = None
    contatos_atualizados = []
    for contato in contatos:
        if contato.get('id') == id:
            nome_contato_removido = contato.get('nome')
        else:
            contatos_atualizados.append(contato)
    session['contatos'] = contatos_atualizados
    return jsonify({"success": "O contato "+nome_contato_removido+" excluído com sucesso"})



if __name__ == '__main__':
    app.run(debug=True)