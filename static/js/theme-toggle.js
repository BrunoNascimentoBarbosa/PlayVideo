/**
 * Baile55 Video Platform - Sistema de temas
 * Implementação com botão de alternância direta entre temas:
 * - Clique alterna entre Modo Claro e Modo Escuro
 */

// Aplicar o tema imediatamente para evitar flash de tema incorreto
(function () {
    // Obtém o tema salvo ou padrão
    const savedTheme = localStorage.getItem('theme') || 'light';

    // Aplica imediatamente para evitar flash
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
})();

// Função para obter o tema atual
function getCurrentTheme() {
    return localStorage.getItem('theme') || 'light';
}

// Função para alternar entre temas claro e escuro
function toggleTheme() {
    const currentTheme = getCurrentTheme();
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    // Salva a preferência do usuário
    localStorage.setItem('theme', newTheme);
    console.log('Tema alterado para:', newTheme);

    // Aplica o tema e atualiza a interface
    applyTheme(newTheme);
    updateThemeIcon(newTheme);
}

// Função para aplicar estilo do tema a elementos específicos que podem não seguir o tema global
function applyThemeToSpecificElements(theme) {
    // 1. Forçar cores em inputs e formulários que podem não respeitar o tema
    const isDark = (theme === 'dark');

    // Estilo personalizado para garantir que tudo siga o tema
    const styleEl = document.getElementById('theme-override-styles') || document.createElement('style');
    if (!styleEl.id) {
        styleEl.id = 'theme-override-styles';
        document.head.appendChild(styleEl);
    }

    // Regras CSS específicas para corrigir elementos que não seguem o tema
    if (isDark) {
        styleEl.textContent = `
            /* Override para elementos de formulário em modo escuro */
            [data-bs-theme="dark"] input, 
            [data-bs-theme="dark"] textarea, 
            [data-bs-theme="dark"] select,
            [data-bs-theme="dark"] .form-control,
            [data-bs-theme="dark"] .form-select,
            [data-bs-theme="dark"] .btn-outline-secondary,
            [data-bs-theme="dark"] .card,
            [data-bs-theme="dark"] .modal-content {
                background-color: #2b2b2b !important;
                color: #e0e0e0 !important;
                border-color: #444 !important;
            }
            
            [data-bs-theme="dark"] .btn-secondary,
            [data-bs-theme="dark"] .btn-light,
            [data-bs-theme="dark"] .btn-outline-secondary {
                background-color: #3a3a3a !important;
                color: #e0e0e0 !important;
                border-color: #555 !important;
            }
            
            [data-bs-theme="dark"] .form-label,
            [data-bs-theme="dark"] label {
                color: #e0e0e0 !important;
            }
            
            [data-bs-theme="dark"] .table-hover tbody tr:hover {
                background-color: rgba(255, 255, 255, 0.1) !important;
            }
            
            /* Corrige itens específicos que podem não mudar de cor */
            [data-bs-theme="dark"] .dropdown-menu {
                background-color: #333 !important;
                border-color: #555 !important;
            }
            
            [data-bs-theme="dark"] .dropdown-item {
                color: #e0e0e0 !important;
            }
            
            [data-bs-theme="dark"] .dropdown-item:hover {
                background-color: #444 !important;
            }
        `;
    } else {
        styleEl.textContent = '';
    }
}

// Função para aplicar tema específico ao documento HTML
function applyThemeToDocument(theme) {
    // Define o atributo data-bs-theme no elemento HTML
    document.documentElement.setAttribute('data-bs-theme', theme);

    // Força a aplicação das classes de tema em elementos específicos
    document.body.classList.remove('theme-light', 'theme-dark');
    document.body.classList.add('theme-' + theme);

    // Aplica estilos específicos para elementos que não respeitam o tema global
    applyThemeToSpecificElements(theme);

    console.log('Tema aplicado com sucesso:', theme);
}

// Função principal para aplicar o tema
function applyTheme(theme) {
    // Aplica o tema
    applyThemeToDocument(theme);
    return theme;
}

// Função para atualizar o ícone do botão conforme o tema atual
function updateThemeIcon(theme) {
    // Obtém referência ao ícone atual
    const sunIcon = document.getElementById('theme-icon-sun');
    const moonIcon = document.getElementById('theme-icon-moon');

    if (!sunIcon || !moonIcon) {
        console.error('Erro: Ícones de tema não encontrados!');
        return;
    }

    // Mostra o ícone adequado para o tema atual
    if (theme === 'light') {
        sunIcon.style.display = 'inline-block';
        moonIcon.style.display = 'none';
    } else { // dark
        sunIcon.style.display = 'none';
        moonIcon.style.display = 'inline-block';
    }

    console.log('Ícone atualizado para o tema:', theme);
}

// Função de inicialização imediata
(function () {
    const initialTheme = getCurrentTheme();
    applyTheme(initialTheme);
    console.log('Sistema de temas inicializado - Tema aplicado:', initialTheme);
})();

// Configuração final quando o DOM estiver completamente carregado
document.addEventListener('DOMContentLoaded', function () {
    // Atualiza o ícone para corresponder ao tema atual
    updateThemeIcon(getCurrentTheme());

    // Configura o evento de clique no botão de tema
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function (e) {
            e.preventDefault();
            toggleTheme();
        });
    }

    console.log('Sistema de temas configurado e pronto para uso.');
}); 