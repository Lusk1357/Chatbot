// script.js
document.addEventListener("DOMContentLoaded", function () {
    const historicoConversa = document.getElementById("historico-conversa");

    function atualizarHistorico(novoHistorico) {
        historicoConversa.innerText = novoHistorico;
        historicoConversa.scrollTop = historicoConversa.scrollHeight;
    }

    // Exibindo mensagem de saudação e solicitando nome do usuário
    const saudacaoInicial = "Olá! Eu sou o {{ nome_maquina }}. Qual é o seu nome?";
    atualizarHistorico(saudacaoInicial);

    const inputMensagem = document.getElementById("mensagem");
    const botaoEnviar = document.getElementById("botao-enviar");

    botaoEnviar.addEventListener("click", function () {
        enviarMensagem(inputMensagem.value);
    });

    inputMensagem.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            enviarMensagem(inputMensagem.value);
        }
    });

    function enviarMensagem(mensagem) {
        if (mensagem.trim() === "") {
            return;
        }

        const dados = { mensagem: mensagem };
        fetch("/processar_mensagem", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(dados),
        })
            .then((response) => response.json())
            .then((data) => {
                atualizarHistorico(data.historico_conversa);
                inputMensagem.value = "";
            })
            .catch((error) => {
                console.error("Erro ao enviar mensagem:", error);
            });
    }

    // Função para exibir respostas do chatbot
    function exibirRespostaChatbot(resposta) {
        const mensagemChatbot = `CTRL+PLAY: ${resposta}`;
        atualizarHistorico(mensagemChatbot);
    }

    // Exibir resposta inicial do chatbot, se houver
    const respostaInicial = "Olá, para começarmos, digite seu nome";
    if (respostaInicial.trim() !== "") {
        exibirRespostaChatbot(respostaInicial);
    }

    // Resetar a página (Flask) quando a página é carregada
    fetch("/resetar", {
        method: "POST",
    })
        .then((response) => response.json())
        .then((data) => {
            console.log("Estado resetado", data);
        })
        .catch((error) => {
            console.error("Erro ao resetar o estado:", error);
        });
});