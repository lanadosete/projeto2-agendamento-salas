let idAgendamentoParaCancelar = null;

document.addEventListener("DOMContentLoaded", () => {

    /* =========================
       MODAL DE SALAS
    ========================= */

    const btnSalas = document.getElementById("btn-salas");
    const modalSalas = document.getElementById("modal-salas");
    const listaSalas = document.getElementById("lista-salas-modal");
    const voltarSalas = document.getElementById("voltar-salas");

    btnSalas.addEventListener("click", async () => {
        modalSalas.style.display = "block";
        listaSalas.innerHTML = "Carregando salas...";

        try {
            const response = await fetch("/salas");
            const salas = await response.json();

            listaSalas.innerHTML = "";

            if (salas.length === 0) {
                listaSalas.innerHTML = "<p>Nenhuma sala disponível.</p>";
                return;
            }

            salas.forEach(sala => {
                listaSalas.innerHTML += `
                    <div class="sala-item">
                        <div class="sala-info">
                            <strong>${sala.nome}</strong>
                            <span>R$ ${sala.valor_hora}/hora</span>
                        </div>
                        <button onclick="window.location.href='/agendar/${sala.id_sala}'">
                            Selecionar
                        </button>
                    </div>
                `;
            });

        } catch {
            mostrarToast("Erro ao carregar salas.", "erro");
        }
    });

    voltarSalas.addEventListener("click", () => {
        modalSalas.style.display = "none";
    });

    /* =========================
       MODAL DE AGENDAMENTOS
    ========================= */

    const btnAgendamentos = document.getElementById("btn-agendamentos");
    const modalAgendamentos = document.getElementById("modal-agendamentos");
    const voltarAgendamentos = document.getElementById("voltar-agendamentos");

    btnAgendamentos.addEventListener("click", () => {
        modalAgendamentos.style.display = "block";
        document.querySelector('input[name="filtro-agendamento"][value="AVULSO"]').checked = true;
        carregarAgendamentos("AVULSO");

        document
            .querySelectorAll("input[name='filtro-agendamento']")
            .forEach(radio => {
                radio.addEventListener("change", () => {
                    carregarAgendamentos(radio.value);
                });
            });
    });

    voltarAgendamentos.addEventListener("click", () => {
        modalAgendamentos.style.display = "none";
    });

    /* =========================
       MODAL VALOR MENSAL
    ========================= */

    const btnValorMensal = document.getElementById("btn-valor-mensal");
    const modalValorMensal = document.getElementById("modal-valor-mensal");
    const btnVoltarValorMensal = document.getElementById("voltar-valor-mensal");
    const inputMes = document.getElementById("mes-selecionado");

    btnValorMensal.addEventListener("click", () => {
        modalValorMensal.style.display = "block";

        const hoje = new Date();
        const mesAtual = hoje.toISOString().slice(0, 7);

        if (!inputMes.value) {
            inputMes.value = mesAtual;
        }

        carregarValorMensal(inputMes.value);

        inputMes.onchange = () => {
            carregarValorMensal(inputMes.value);
        };
    });

    btnVoltarValorMensal.addEventListener("click", () => {
        modalValorMensal.style.display = "none";
    });

    /* =========================
       MODAIS DE CANCELAMENTO
    ========================= */

    const modalConfirmar = document.getElementById("modal-confirmar-cancelamento");
    const modalSucesso = document.getElementById("modal-cancelado-sucesso");

    const btnConfirmar = document.getElementById("btn-confirmar-cancelamento");
    const btnFecharConfirmar = document.getElementById("btn-fechar-cancelamento");
    const btnFecharSucesso = document.getElementById("btn-fechar-cancelado");

    btnConfirmar.addEventListener("click", async () => {
        const response = await fetch("/agendamentos/cancelar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id_horario: idAgendamentoParaCancelar })
        });

        const resultado = await response.json();

        if (!response.ok) {
            mostrarToast(resultado.erro, "erro");
            return;
        }

        modalConfirmar.style.display = "none";
        modalSucesso.style.display = "block";
        carregarAgendamentos("AVULSO");
    });

    btnFecharConfirmar.addEventListener("click", () => {
        modalConfirmar.style.display = "none";
    });

    btnFecharSucesso.addEventListener("click", () => {
        modalSucesso.style.display = "none";
    });
});


/* =========================
   FUNÇÕES AUXILIARES
========================= */

async function carregarAgendamentos(filtro) {
    const listaAgendamentos = document.getElementById("lista-agendamentos");
    listaAgendamentos.innerHTML = "Carregando...";

    try {
        const response = await fetch(`/agendamentos?filtro=${filtro}`);
        const dados = await response.json();

        listaAgendamentos.innerHTML = "";

        if (dados.length === 0) {
            listaAgendamentos.innerHTML = "<p>Nenhum registro encontrado.</p>";
            return;
        }

        dados.forEach(a => {

            let descricao = a.descricao;

            if (descricao.includes("→")) {
                const partes = descricao.split("→");
                descricao = `${formatarDataHoraBR(partes[0])} → ${formatarDataHoraBR(partes[1])}`;
            }

            // 🔹 Layout original restaurado
            listaAgendamentos.innerHTML += `
                <div class="sala-item">
                    <div class="sala-info">
                        <strong>${a.sala}</strong>
                        <span>${descricao}</span>
                        <span>Status: ${a.status}</span>
                    </div>

                    ${
                        a.tipo === "AVULSO" && a.status === "ATIVO"
                        ? `<button onclick="cancelarAgendamento(${a.id})">Cancelar</button>`
                        : ""
                    }
                </div>
            `;
        });

    } catch {
        mostrarToast("Erro ao carregar agendamentos.", "erro");
    }
}

function cancelarAgendamento(idHorario) {
    idAgendamentoParaCancelar = idHorario;
    document.getElementById("modal-confirmar-cancelamento").style.display = "block";
}

async function carregarValorMensal(mes) {
    const lista = document.getElementById("lista-valor-mensal");
    lista.innerHTML = "Carregando...";

    try {
        const response = await fetch(
            `/valor-mensal/detalhado?id_profissional=1&mes=${mes}`
        );

        const dados = await response.json();

        if (dados.total === 0) {
            lista.innerHTML = "<p style='text-align:center;'>Nenhum gasto neste mês.</p>";
            return;
        }

        lista.innerHTML = `
            <div class="valor-secao">
                <div class="valor-item">
                    <div class="valor-linha">
                        <span>Total geral</span>
                        <strong>R$ ${dados.total.toFixed(2)}</strong>
                    </div>
                    <div class="valor-linha">
                        <span>Avulsos</span>
                        <span>R$ ${dados.avulso.toFixed(2)}</span>
                    </div>
                    <div class="valor-linha">
                        <span>Recorrentes</span>
                        <span>R$ ${dados.recorrente.toFixed(2)}</span>
                    </div>
                </div>
            </div>
        `;
    } catch {
        mostrarToast("Erro ao carregar valor mensal.", "erro");
    }
}

function formatarDataHoraBR(dataIso) {
    const data = new Date(dataIso);
    if (isNaN(data)) return dataIso;

    return data.toLocaleString("pt-BR", {
        dateStyle: "short",
        timeStyle: "short"
    });
}

function mostrarToast(mensagem, tipo = "erro") {
    const toast = document.createElement("div");
    toast.className = `toast toast-${tipo}`;
    toast.innerText = mensagem;

    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add("show"), 100);

    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}