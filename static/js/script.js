// SPINNER
const spinner = `
<div class="d-flex justify-content-center align-items-center" style="height:200px;">
    <div class="spinner-border text-primary"></div>
</div>`;

// ABRIR MODAL
function abrirModal(modalId, html) {
    const modal = document.getElementById(modalId);
    modal.querySelector(".modal-content-vaga").innerHTML = html;
    modal.classList.add("ativo");
}

// FECHAR MODAL
function fecharModal() {
    document.querySelectorAll(".modal-vaga").forEach(m => m.classList.remove("ativo"));
}

// EVENTOS GLOBAIS
document.addEventListener("click", (e) => {
    // FECHAR MODAL
    if (e.target.matches(".modal-vaga, .modal-close, [data-modal-close]")) {
        e.preventDefault();
        fecharModal();
    }

    // VER VAGA (AJAX)
    if (e.target.matches("[data-vaga-detalhe]")) {
        e.preventDefault();
        const url = e.target.dataset.vagaDetalhe;
        const modalId = e.target.dataset.modal;
        abrirModal(modalId, spinner);

        fetch(url)
            .then(r => r.json())
            .then(data => abrirModal(modalId, data.html))
            .catch(() => abrirModal(modalId, "<p>Erro ao carregar dados.</p>"));
    }

    // EDITAR VAGA (AJAX)
    if (e.target.matches("[data-vaga-form]")) {
        e.preventDefault();
        const url = e.target.dataset.vagaForm;
        const modalId = e.target.dataset.modal;
        abrirModal(modalId, spinner);

        fetch(url)
            .then(r => r.json())
            .then(data => {
                abrirModal(modalId, data.html);
                bindFormVaga(modalId);
            })
            .catch(() => abrirModal(modalId, "<p>Erro ao abrir formulário.</p>"));
    }

    // EXCLUIR VAGA (AJAX)
    if (e.target.matches("[data-vaga-excluir]")) {
        e.preventDefault();
        const url = e.target.dataset.vagaExcluir;
        const modalId = e.target.dataset.modal;

        // Abrir o modal com o spinner
        abrirModal(modalId, spinner);

        // Fazer a requisição para obter o conteúdo do modal de exclusão
        fetch(url)
            .then(r => r.json())
            .then(data => {
                // Atualiza o modal com o HTML recebido
                abrirModal(modalId, data.html);
                // Vincula o formulário de exclusão (caso necessário)
                bindFormExcluir(modalId);
            })
            .catch(() => {
                alert("Erro de conexão.");
                fecharModal(); // Fecha o modal em caso de erro de conexão
            });
    }

    // GERENCIAR VAGA (AJAX) - Agora incluímos o botão "Gerenciar"
    if (e.target.matches("[data-vaga-gerenciar]")) {
        e.preventDefault();
        const url = e.target.dataset.vagaGerenciar;
        const modalId = e.target.dataset.modal;
        abrirModal(modalId, spinner);

        // Fazer a requisição para obter o conteúdo do modal de gerenciar
        fetch(url)
            .then(r => r.json())
            .then(data => {
                abrirModal(modalId, data.html);
                // Vincula o formulário de gerenciar (caso necessário)
                bindFormGerenciar(modalId);
            })
            .catch(() => {
                alert("Erro de conexão.");
                fecharModal(); // Fecha o modal em caso de erro de conexão
            });
    }

    // Aprovar Vaga (AJAX)
    if (e.target.matches("[data-vaga-aprovar]")) {
        e.preventDefault();
        const url = e.target.dataset.vagaAprovar;
        const modalId = e.target.dataset.modal;
        abrirModal(modalId, spinner);

        // Fazer a requisição para aprovar a vaga via AJAX
        fetch(url)
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    alert("Vaga aprovada com sucesso!");
                    location.reload(); // Atualiza a página
                } else {
                    alert("Erro ao aprovar a vaga.");
                }
                fecharModal(); // Fecha o modal após a aprovação
            })
            .catch(() => {
                alert("Erro de conexão.");
                fecharModal(); // Fecha o modal em caso de erro de conexão
            });
    }

    // Reprovar Vaga (AJAX)
    if (e.target.matches("[data-vaga-reprovar]")) {
        e.preventDefault();
        const url = e.target.dataset.vagaReprovar;
        const modalId = e.target.dataset.modal;
        abrirModal(modalId, spinner);

        // Fazer a requisição para reprovar a vaga via AJAX
        fetch(url)
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    alert("Vaga reprovada com sucesso!");
                    location.reload(); // Atualiza a página
                } else {
                    alert("Erro ao reprovar a vaga.");
                }
                fecharModal(); // Fecha o modal após a reprovação
            })
            .catch(() => {
                alert("Erro de conexão.");
                fecharModal(); // Fecha o modal em caso de erro de conexão
            });
    }
});

// SUBMIT FORM VAGA
function bindFormVaga(modalId) {
    const form = document.querySelector(`#${modalId} form`);
    if (!form) return;

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": getCSRFToken() }
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                fecharModal();
                location.reload();
            } else {
                document.querySelector(`#${modalId} .modal-content-vaga`).innerHTML = data.html;
                bindFormVaga(modalId);
            }
        })
        .catch(() => alert("Erro ao salvar.")); 
    });
}

// SUBMIT FORM EXCLUIR
function bindFormExcluir(modalId) {
    const form = document.querySelector(`#${modalId} form`);
    if (!form) return;

    form.addEventListener("submit", (e) => {
        e.preventDefault();  // Impede o envio normal do formulário

        fetch(form.action, {
            method: "POST",  // Envia uma requisição POST
            headers: { "X-CSRFToken": getCSRFToken() }  // CSRF token para segurança
        })
        .then((r) => r.json())  // Espera a resposta como JSON
        .then((data) => {
            if (data.success) {
                fecharModal();  // Fecha o modal se a exclusão for bem-sucedida
                location.reload();  // Recarrega a página
            } else {
                alert("Erro ao excluir.");
            }
        })
        .catch(() => alert("Erro ao excluir."));  // Caso haja erro de conexão
    });
}

// SUBMIT FORM GERENCIAR (para as vagas)
function bindFormGerenciar(modalId) {
    const form = document.querySelector(`#${modalId} form`);
    if (!form) return;

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": getCSRFToken() }
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                fecharModal();
                location.reload();
            } else {
                alert("Erro ao gerenciar a vaga.");
            }
        })
        .catch(() => alert("Erro ao gerenciar a vaga.")); 
    });
}

// CSRF
function getCSRFToken() {
    return document.cookie.split("; ").find(row => row.startsWith("csrftoken="))?.split("=")[1];
}  
