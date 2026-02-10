/* ===================== SPINNER ===================== */
const spinner = `
<div class="d-flex justify-content-center align-items-center" style="height: 200px;">
    <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
    </div>
</div>`;

/* ===================== MODAL ===================== */
const meuModal = new bootstrap.Modal(document.querySelector("#modalPadrao"));
const modalTitle = document.querySelector(".modal-title");
const modalBody = document.querySelector(".modal-body");
const btnSalvar = document.querySelector(".btn-salvar");

/* ===================== CONTROLE ===================== */
let modoAtual = null;
let urlAtual = null;

/* ===================== MENSAGENS ===================== */
function buscarMensagens() {
    fetch(mensagensUrl, { cache: "no-store" })
        .then(r => r.text())
        .then(html => {
            const div = document.querySelector("#div-mensagens");
            if (div) div.innerHTML = html;
        });
}

/* ===================== FORM HELPER ===================== */
function configurarForm(url) {
    const form = modalBody.querySelector(".form-vaga");
    if (!form) return;

    form.action = url;
    form.addEventListener("submit", e => e.preventDefault());
}

/* ===================== RESET BOTÃO ===================== */
function resetarBotaoSalvar() {
    btnSalvar.innerText = "Salvar";
    btnSalvar.classList.remove("btn-danger");
    btnSalvar.classList.add("btn-primary");
}

/* ===================== CREATE ===================== */
document.querySelector(".btn-criar")?.addEventListener("click", e => {
    e.preventDefault();

    modoAtual = "criar";
    urlAtual = e.currentTarget.href;

    resetarBotaoSalvar();
    btnSalvar.classList.remove("d-none");

    modalTitle.innerText = "Nova vaga";
    modalBody.innerHTML = spinner;
    meuModal.show();

    fetch(urlAtual)
        .then(r => r.text())
        .then(html => {
            modalBody.innerHTML = html;
            configurarForm(urlAtual);
        });
});

/* ===================== SALVAR ===================== */
btnSalvar.onclick = async function () {

    /* ===== REMOVER (AJUSTADO) ===== */
    if (modoAtual === "remover") {
        const formRemover = modalBody.querySelector(".form-remover");
        if (!formRemover) return;

        modalBody.innerHTML = spinner;

        const response = await fetch(urlAtual, {
            method: "POST",
            body: new FormData(formRemover),
        });

        // 🔥 ESSENCIAL: força o Django a finalizar o ciclo
        await response.text();

        meuModal.hide();
        atualizarLista();
        buscarMensagens();
        resetarBotaoSalvar();
        return;
    }

    /* ===== CREATE / EDIT ===== */
    const form = modalBody.querySelector(".form-vaga");
    if (!form) return;

    modalBody.innerHTML = spinner;

    try {
        const response = await fetch(form.action, {
            method: "POST",
            body: new FormData(form),
        });

        const contentType = response.headers.get("content-type") || "";

        if (response.ok && contentType.includes("application/json")) {
            await response.json();
            meuModal.hide();
            atualizarLista();
            buscarMensagens();
            resetarBotaoSalvar();
            return;
        }

        if (contentType.includes("text/html")) {
            modalBody.innerHTML = await response.text();
            configurarForm(form.action);
            buscarMensagens();
        }

    } catch (err) {
        console.error("Erro ao salvar:", err);
    }
};

/* ===================== LISTA ===================== */
function atualizarLista() {
    const lista = document.querySelector("#lista");
    lista.innerHTML = spinner;

    fetch(listaUrl)
        .then(r => r.text())
        .then(html => {
            lista.innerHTML = html;
            criarEventos();
        });
}

/* ===================== EVENTOS ===================== */
function criarEventos() {

    /* DETALHAR */
    document.querySelectorAll(".btn-detalhar").forEach(btn => {
        btn.onclick = e => {
            e.preventDefault();
            modoAtual = "detalhar";

            btnSalvar.classList.add("d-none");

            modalTitle.innerText = "Detalhar vaga";
            modalBody.innerHTML = spinner;
            meuModal.show();

            fetch(btn.href)
                .then(r => r.text())
                .then(html => modalBody.innerHTML = html);
        };
    });

    /* EDITAR */
    document.querySelectorAll(".btn-editar").forEach(btn => {
        btn.onclick = e => {
            e.preventDefault();

            modoAtual = "editar";
            urlAtual = btn.href;

            resetarBotaoSalvar();
            btnSalvar.classList.remove("d-none");

            modalTitle.innerText = "Editar vaga";
            modalBody.innerHTML = spinner;
            meuModal.show();

            fetch(urlAtual)
                .then(r => r.text())
                .then(html => {
                    modalBody.innerHTML = html;
                    configurarForm(urlAtual);
                });
        };
    });

    /* REMOVER */
    document.querySelectorAll(".btn-remover").forEach(btn => {
        btn.onclick = e => {
            e.preventDefault();

            modoAtual = "remover";
            urlAtual = btn.href;

            btnSalvar.innerText = "Excluir";
            btnSalvar.classList.remove("btn-primary");
            btnSalvar.classList.add("btn-danger");
            btnSalvar.classList.remove("d-none");

            modalTitle.innerText = "Excluir vaga";
            modalBody.innerHTML = spinner;
            meuModal.show();

            fetch(urlAtual)
                .then(r => r.text())
                .then(html => modalBody.innerHTML = html);
        };
    });
}


/* ===================== INIT ===================== */
criarEventos();
