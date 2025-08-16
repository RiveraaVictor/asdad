/**
 * Flask Monolith Template - JavaScript Principal
 * Funcionalidades interativas da aplicação
 */

// Aguardar carregamento do DOM
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades
    initializeApp();
    initializeSearch();
    initializeLikes();
    initializeTooltips();
    initializeAlerts();
    initializeScrollToTop();
    initializeImageLazyLoading();
    initializeFormValidation();
});

/**
 * Inicializar aplicação
 */
function initializeApp() {
    console.log('Flask Monolith Template carregado');
    
    // Adicionar classe para indicar que JS está ativo
    document.body.classList.add('js-enabled');
    
    // Configurar CSRF token para requisições AJAX
    const csrfToken = document.querySelector('meta[name="csrf-token"]');
    if (csrfToken) {
        window.csrfToken = csrfToken.getAttribute('content');
    }
}

/**
 * Inicializar funcionalidade de busca
 */
function initializeSearch() {
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('input[name="q"]');
    
    if (!searchInput) return;
    
    let searchTimeout;
    
    // Busca em tempo real (opcional)
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length < 3) {
            hideSearchResults();
            return;
        }
        
        searchTimeout = setTimeout(() => {
            performLiveSearch(query);
        }, 300);
    });
    
    // Esconder resultados ao clicar fora
    document.addEventListener('click', function(e) {
        if (!searchForm || !searchForm.contains(e.target)) {
            hideSearchResults();
        }
    });
}

/**
 * Realizar busca em tempo real
 */
function performLiveSearch(query) {
    fetch(`/api/search?q=${encodeURIComponent(query)}&limit=5`)
        .then(response => response.json())
        .then(data => {
            if (data.success && data.data.length > 0) {
                showSearchResults(data.data);
            } else {
                hideSearchResults();
            }
        })
        .catch(error => {
            console.error('Erro na busca:', error);
            hideSearchResults();
        });
}

/**
 * Mostrar resultados da busca
 */
function showSearchResults(results) {
    let resultsContainer = document.querySelector('.search-results');
    
    if (!resultsContainer) {
        resultsContainer = document.createElement('div');
        resultsContainer.className = 'search-results';
        document.querySelector('.search-form').appendChild(resultsContainer);
    }
    
    resultsContainer.innerHTML = results.map(post => `
        <div class="search-result-item">
            <a href="${post.url}" class="text-decoration-none">
                <div class="fw-medium">${post.title}</div>
                <div class="text-muted small">${post.excerpt}</div>
            </a>
        </div>
    `).join('');
    
    resultsContainer.style.display = 'block';
}

/**
 * Esconder resultados da busca
 */
function hideSearchResults() {
    const resultsContainer = document.querySelector('.search-results');
    if (resultsContainer) {
        resultsContainer.style.display = 'none';
    }
}

/**
 * Inicializar sistema de likes
 */
function initializeLikes() {
    const likeButtons = document.querySelectorAll('.like-button');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const postId = this.dataset.postId;
            if (!postId) return;
            
            // Verificar se usuário está logado
            if (!isUserAuthenticated()) {
                showLoginModal();
                return;
            }
            
            likePost(postId, this);
        });
    });
}

/**
 * Curtir post
 */
function likePost(postId, button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    button.disabled = true;
    
    fetch(`/api/posts/${postId}/like`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.csrfToken || ''
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Atualizar contador de likes
            const counter = button.querySelector('.like-count');
            if (counter) {
                counter.textContent = data.likes_count;
            }
            
            // Adicionar animação
            button.classList.add('liked');
            setTimeout(() => button.classList.remove('liked'), 300);
            
            showToast('Post curtido!', 'success');
        } else {
            showToast('Erro ao curtir post', 'error');
        }
    })
    .catch(error => {
        console.error('Erro ao curtir post:', error);
        showToast('Erro ao curtir post', 'error');
    })
    .finally(() => {
        button.innerHTML = originalText;
        button.disabled = false;
    });
}

/**
 * Verificar se usuário está autenticado
 */
function isUserAuthenticated() {
    return document.body.classList.contains('authenticated') || 
           document.querySelector('.navbar .dropdown-toggle');
}

/**
 * Mostrar modal de login
 */
function showLoginModal() {
    // Implementar modal de login ou redirecionar
    if (confirm('Você precisa estar logado para curtir posts. Deseja fazer login?')) {
        window.location.href = '/auth/login';
    }
}

/**
 * Inicializar tooltips do Bootstrap
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Inicializar auto-dismiss de alertas
 */
function initializeAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    
    alerts.forEach(alert => {
        // Auto-dismiss após 5 segundos
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Inicializar botão "Voltar ao topo"
 */
function initializeScrollToTop() {
    // Criar botão se não existir
    let scrollButton = document.querySelector('.scroll-to-top');
    if (!scrollButton) {
        scrollButton = document.createElement('button');
        scrollButton.className = 'btn btn-primary scroll-to-top';
        scrollButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
        scrollButton.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: none;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        `;
        document.body.appendChild(scrollButton);
    }
    
    // Mostrar/esconder baseado no scroll
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollButton.style.display = 'block';
        } else {
            scrollButton.style.display = 'none';
        }
    });
    
    // Ação do clique
    scrollButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/**
 * Inicializar lazy loading de imagens
 */
function initializeImageLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback para navegadores sem suporte
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

/**
 * Inicializar validação de formulários
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        });
    });
    
    // Validação em tempo real
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.checkValidity()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            }
        });
    });
}

/**
 * Mostrar toast notification
 */
function showToast(message, type = 'info', duration = 3000) {
    // Criar container de toasts se não existir
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1055';
        document.body.appendChild(toastContainer);
    }
    
    // Criar toast
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type === 'error' ? 'danger' : type}" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    // Mostrar toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: duration
    });
    
    toast.show();
    
    // Remover do DOM após esconder
    toastElement.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

/**
 * Confirmar ação
 */
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

/**
 * Copiar texto para clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copiado para a área de transferência!', 'success');
        }).catch(() => {
            showToast('Erro ao copiar', 'error');
        });
    } else {
        // Fallback para navegadores sem suporte
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            document.execCommand('copy');
            showToast('Copiado para a área de transferência!', 'success');
        } catch (err) {
            showToast('Erro ao copiar', 'error');
        }
        
        document.body.removeChild(textArea);
    }
}

/**
 * Formatar data para exibição
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Formatar data relativa (ex: "há 2 horas")
 */
function formatRelativeDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    const intervals = {
        ano: 31536000,
        mês: 2592000,
        semana: 604800,
        dia: 86400,
        hora: 3600,
        minuto: 60
    };
    
    for (const [unit, seconds] of Object.entries(intervals)) {
        const interval = Math.floor(diffInSeconds / seconds);
        if (interval >= 1) {
            return `há ${interval} ${unit}${interval > 1 ? 's' : ''}`;
        }
    }
    
    return 'agora mesmo';
}

/**
 * Debounce function
 */
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
}

/**
 * Throttle function
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Exportar funções para uso global
window.FlaskApp = {
    showToast,
    confirmAction,
    copyToClipboard,
    formatDate,
    formatRelativeDate,
    debounce,
    throttle
};

// Adicionar estilos CSS dinâmicos
const dynamicStyles = `
    .liked {
        animation: likeAnimation 0.3s ease;
    }
    
    @keyframes likeAnimation {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    
    .lazy {
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .scroll-to-top {
        transition: all 0.3s ease;
    }
    
    .scroll-to-top:hover {
        transform: translateY(-2px);
    }
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = dynamicStyles;
document.head.appendChild(styleSheet);