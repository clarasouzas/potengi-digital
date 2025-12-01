let currentUserType = 'aluno';

function setUserType(type) {
    currentUserType = type;
    console.log('Tipo definido:', type);
    
    localStorage.setItem('userType', type);
    
    updateActiveTab(type);
    
    updateGoogleButtons(type);
}

function updateGoogleButtons(type) {
    document.querySelectorAll('.google-login-btn').forEach(btn => {
        btn.setAttribute('data-tipo', type);
    });
}

function loginWithGoogle(type) {
    console.log('Login Google como:', type);
    
    setTypeInSession(type).then(() => {
        const googleUrl = document.querySelector('.google-login-btn').getAttribute('data-google-url');
        console.log('Redirecionando para:', googleUrl);
        window.location.href = googleUrl;
    }).catch(error => {
        console.error('Erro:', error);
        const googleUrl = document.querySelector('.google-login-btn').getAttribute('data-google-url');
        window.location.href = googleUrl;
    });
}

function setTypeInSession(type) {
    return new Promise((resolve, reject) => {
        document.getElementById('form-tipo-input').value = type;
        
        const form = document.getElementById('set-type-form');
        const formData = new FormData(form);
        
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                console.log('Tipo definido na sessão:', data.message);
                resolve();
            } else {
                reject(data.error || 'Erro desconhecido');
            }
        })
        .catch(error => reject(error));
    });
}

function updateActiveTab(type) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    if (type === 'aluno') {
        const alunoBtn = document.querySelector('[data-bs-target="#aba-aluno"]');
        if (alunoBtn) {
            alunoBtn.classList.add('active');
            const tab = new bootstrap.Tab(alunoBtn);
            tab.show();
        }
    } else if (type === 'empresa') {
        const empresaBtn = document.querySelector('[data-bs-target="#aba-empresa"]');
        if (empresaBtn) {
            empresaBtn.classList.add('active');
            const tab = new bootstrap.Tab(empresaBtn);
            tab.show();
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM carregado - inicializando scripts de cadastro');
    
    const savedType = localStorage.getItem('userType');
    if (savedType) {
        currentUserType = savedType;
        updateActiveTab(savedType);
        updateGoogleButtons(savedType);
    }
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const target = this.getAttribute('data-bs-target');
            if (target === '#aba-aluno') {
                setUserType('aluno');
            } else if (target === '#aba-empresa') {
                setUserType('empresa');
            }
        });
    });
    
    document.querySelectorAll('.google-login-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            let tipo = this.getAttribute('data-tipo');
            if (!tipo) {
                tipo = currentUserType;
            }
            
            loginWithGoogle(tipo);
        });
    });
});