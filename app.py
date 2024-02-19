from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

class Config:
    NOME_MAQUINA = "CTRL+PLAY"
    BANCO_DE_CONHECIMENTO = "BancoDeConhecimento.txt"

entrada_sugestao = False
entrada_nome_usuario = True
nome_usuario = ""
historico_conversa = ""

def saudacao_GUI(nome):
    frases = ["Olá, meu nome é " + nome + ". Como vai você?", "Oi!", "Oi, tudo bem?"]
    return random.choice(frases)

def busca_resposta_GUI(nome, texto):
    with open(Config.BANCO_DE_CONHECIMENTO, "a+", encoding="utf-8") as conhecimento:
        conhecimento.seek(0)
        while True:
            viu = conhecimento.readline()
            if viu != '':
                if jaccard(nome + ": " + texto, viu) >= 0.8:
                    proxima_linha = conhecimento.readline()
                    if "chatbot: " in proxima_linha: 
                        return proxima_linha
            else:
                conhecimento.write("\ncliente: " + texto)
                return "Me desculpe, não sei o que falar"

def exibe_resposta_GUI(texto, resposta, nome):
    return resposta.replace("chatbot", nome)

def salva_sugestao(sugestao):
    with open(Config.BANCO_DE_CONHECIMENTO, "a+", encoding="utf-8") as conhecimento:
        conhecimento.write("\nchatbot: " + sugestao + "\n")

def jaccard(texto_usuario, texto_base):
    texto_usuario = limpa_frase(texto_usuario)
    texto_base = limpa_frase(texto_base)
    if len(texto_base) < 1:
        return 0
    else:
        palavras_em_comum = sum(palavra in texto_base.split() for palavra in texto_usuario.split())
        return palavras_em_comum / len(texto_base.split())

def limpa_frase(frase):
    tirar = ["?", "!", "...", ".", ",", "cliente: ", "\n", "Cliente: "]
    for t in tirar:
        frase = frase.replace(t, "")
    return frase.lower()

def saudacao_inicial():
    return f"Olá! Eu sou o {Config.NOME_MAQUINA}. Qual é o seu nome?"

@app.route('/')
def index():
    return render_template('index.html', historico_conversa=historico_conversa, saudacao_inicial=saudacao_inicial())

@app.route('/processar_mensagem', methods=['POST'])
def processar_mensagem():
    global nome_usuario, historico_conversa, entrada_sugestao, entrada_nome_usuario

    try:
        if entrada_nome_usuario:
            nome_usuario = request.json['mensagem']
            saudacao = saudacao_GUI(Config.NOME_MAQUINA)
            historico_conversa = f"{Config.NOME_MAQUINA}: {saudacao}\n"
            entrada_nome_usuario = False
        else:
            texto = request.json['mensagem']
            historico_conversa += f"\n{nome_usuario}: {texto}\n"

            if entrada_sugestao:
                salva_sugestao(texto)
                entrada_sugestao = False
                historico_conversa += "\nAgora aprendi! Vamos continuar nossa conversa...\n"
            else:
                resposta = busca_resposta_GUI(nome_usuario, texto)

                if resposta == "Me desculpe, não sei o que falar":
                    historico_conversa += "\nMe desculpe, não sei o que falar. O que você esperava?\n"
                    pergunta = limpa_frase(f"{nome_usuario}: {texto}")
                    entrada_sugestao = True
                else:
                    historico_conversa += f"\n{exibe_resposta_GUI(texto, resposta, Config.NOME_MAQUINA)}\n"

        return jsonify({'historico_conversa': historico_conversa})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/resetar', methods=['POST'])
def resetar():
    global entrada_nome_usuario, entrada_sugestao, nome_usuario, historico_conversa
    entrada_sugestao = False
    entrada_nome_usuario = True
    nome_usuario = ""
    historico_conversa = ""
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
