/**
 * Baile55 Video Platform - Chat Widget
 * Controla a funcionalidade do widget de chat
 */

document.addEventListener('DOMContentLoaded', function () {
    // Elementos do chat
    const chatButton = document.getElementById('chat-widget-button');
    const chatPopup = document.getElementById('chat-widget-popup');
    const chatClose = document.getElementById('chat-widget-close');
    const chatExpand = document.getElementById('chat-widget-expand');
    const chatForm = document.getElementById('chat-widget-form');
    const chatInput = document.getElementById('chat-widget-input');
    const chatMessages = document.getElementById('chat-widget-messages');

    let isExpanded = false;

    // Função para alternar a visibilidade do popup
    function toggleChatPopup() {
        if (chatPopup.classList.contains('show')) {
            chatPopup.classList.remove('show');
            chatPopup.classList.add('hide');
            setTimeout(() => {
                chatPopup.style.display = 'none';
                chatPopup.classList.remove('hide');
            }, 300);
        } else {
            chatPopup.style.display = 'flex';
            chatPopup.classList.add('show');
            chatInput.focus();
        }
    }

    // Função para expandir/contrair o chat
    function toggleExpandChat() {
        if (isExpanded) {
            chatPopup.style.width = '320px';
            chatPopup.style.height = '400px';
            isExpanded = false;
            chatExpand.innerHTML = '<i class="fas fa-expand-alt"></i>';
        } else {
            chatPopup.style.width = '400px';
            chatPopup.style.height = '500px';
            isExpanded = true;
            chatExpand.innerHTML = '<i class="fas fa-compress-alt"></i>';
        }
    }

    // Função para adicionar mensagem ao chat
    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message');
        messageDiv.classList.add(isUser ? 'chat-message-user' : 'chat-message-assistant');
        messageDiv.textContent = content;

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Função para processar o envio de mensagem
    function handleMessageSubmit(e) {
        e.preventDefault();
        const message = chatInput.value.trim();

        if (message) {
            // Adiciona a mensagem do usuário ao chat
            addMessage(message, true);
            chatInput.value = '';

            // Simula uma resposta do assistente (em produção, aqui você faria uma chamada de API)
            setTimeout(() => {
                addMessage('Obrigado por sua mensagem! Sou o assistente virtual do Baile55 Video Platform. Como posso ajudar?');
            }, 1000);
        }
    }

    // Event listeners
    if (chatButton) {
        chatButton.addEventListener('click', toggleChatPopup);
    }

    if (chatClose) {
        chatClose.addEventListener('click', toggleChatPopup);
    }

    if (chatExpand) {
        chatExpand.addEventListener('click', toggleExpandChat);
    }

    if (chatForm) {
        chatForm.addEventListener('submit', handleMessageSubmit);
    }

    // Detectar clique fora do chat para fechá-lo
    document.addEventListener('click', function (e) {
        const isClickInsideChat = chatPopup.contains(e.target);
        const isClickOnButton = chatButton.contains(e.target);

        if (chatPopup.classList.contains('show') && !isClickInsideChat && !isClickOnButton) {
            toggleChatPopup();
        }
    });

    // Impedir que o clique dentro do popup feche o chat
    chatPopup.addEventListener('click', function (e) {
        e.stopPropagation();
    });
}); 