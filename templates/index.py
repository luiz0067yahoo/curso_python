
import json
from flask import Flask,request,render_template,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/calculadora')
def calculadora():
    return render_template('./calculadora.html')

@app.route('/')
def home():
    resultado=""
    i = 1
    while i < 6:
        print(i)
        resultado+=str(i)+"<br>\n"
        i += 1        
    return resultado

@app.route('/teste')
def teste():
    resultado=""
    for x in range(1,6):
        resultado+=str(x)+"<br>\n"
    return resultado

@app.route('/soma')
def soma():
    resultado=""
    v1=request.args.get('v1')
    v2=request.args.get('v2')
    try:
        resultado=float(v1)+float(v2)
    except:
        print("Erro ao somar")
    finally:
        print("Soma realizada com sucesso")
    return str(resultado)


@app.route('/subtracao',methods=['POST'])
def subtracao():
    resultado=""
    data = request.get_json()
    v1 = data.get('v1')
    v2 = data.get('v2')
    try:
        resultado=float(v1)-float(v2)
    except:
        print("Erro ao somar")
    finally:
        print("Subtracao realizada com sucesso")
    return str(resultado)



@app.route('/divisao',methods=['PUT'])
def divisao():
    resultado=""
    data = request.get_json()
    v1 = data.get('v1')
    v2 = data.get('v2')
    try:
        resultado=float(v1)/float(v2)
    except:
        print("Erro ao somar")
    finally:
        print("Subtracao realizada com sucesso")
    return str(resultado)

@app.route('/multiplicacao/<int:v1>/<int:v2>', methods=['DELETE'])
def multiplicacao(v1, v2):
    resultado=""
    try:
        resultado=float(v1)*float(v2)
    except:
        print("Erro ao somar")
    finally:
        print("Subtracao realizada com sucesso")
    return str(resultado)








if __name__ == '__main__':
    app.run(debug=True)