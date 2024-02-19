import chatbot as pc
from tkinter import *

def roda_Chatbot():
    global entrada_sugestao
    global entrada_nome_usuario
    global historico_conversa
    global nome_usuario

    if entrada_nome_usuario:
        nome_usuario = e_mensagem.get()
        saudacao = pc.saudacao_GUI(nome_maquina)
        historico_conversa = nome_maquina + ": " + saudacao + "\n"
        v.set(historico_conversa)
        entrada_nome_usuario = False

    else:
        texto = e_mensagem.get()
        historico_conversa += "\n " + nome_usuario + ": " + texto
        v.set(historico_conversa)

        if entrada_sugestao:
            pc.salva_sugestao(texto)
            entrada_sugestao = False
            historico_conversa += "\n Agora aprendi! Vamos continuar nossa conversa... \n"
            v.set(historico_conversa)
        else:
            resposta = pc.buscaResposta_GUI(nome_usuario, texto)


            if resposta == "Me desculpe, não sei o que falar":
                historico_conversa += "\n Me desculpe, não sei o que falar. O que você esperava? \n"
                v.set(historico_conversa)
                entrada_sugestao = True
            else:
                historico_conversa += "\n" + pc.exibeResposta_GUI(texto, resposta, nome_maquina)
                v.set(historico_conversa)

main_window = Tk()

main_window.title("Lucas")
main_window.geometry("1080x720")

frame = Frame(main_window)
frame.grid()

l_identif = Label(frame, text="Insira uma mensagem aqui: ")
l_identif.grid(row=0, column=0)

e_mensagem = Entry(frame)
e_mensagem.grid(row=0, column=1)

frame2 = Frame(main_window)
frame2.grid(row=0, column=1)
v = StringVar()
Label(frame2, textvariable=v).grid()

nome_maquina = "CTRL+PLAY"
v.set("Qual é o seu nome?")
entrada_sugestao = False
entrada_nome_usuario = True
nome_usuario = ""
historico_conversa = ""

Button(frame, text="Clique Aqui", command=roda_Chatbot).grid(row=0, column=2)

main_window.mainloop()
