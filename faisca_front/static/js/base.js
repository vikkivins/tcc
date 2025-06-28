document.addEventListener('DOMContentLoaded', function() {
    const dropdownToggle = document.querySelector('.dropdown-toggle');
    const dropdownMenu = document.querySelector('.dropdown-menu');
    
    if (dropdownToggle && dropdownMenu) {
        dropdownToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            dropdownMenu.classList.toggle('show');
        });

        // Fechar ao clicar fora
        document.addEventListener('click', function(e) {
            if (!dropdownToggle.contains(e.target) && !dropdownMenu.contains(e.target)) {
                dropdownMenu.classList.remove('show');
            }
        });

        // Fechar ao pressionar ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                dropdownMenu.classList.remove('show');
            }
        });
    }
    // Adicione o código da sidebar
    const menuIcon = document.querySelector('.menu-icon');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    menuIcon.addEventListener('click', function() {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    });

    overlay.addEventListener('click', function() {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    });

    // Fechar ao pressionar ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        }
    });

    // Notificações
    const notificationBell = document.getElementById('notification-bell');
    const notificationModal = document.getElementById('notification-modal');
    const notificationDot = document.getElementById('notification-dot');
    const notificationList = document.getElementById('notification-list');
    const closeNotificationModal = document.getElementById('close-notification-modal');

    function fetchNotifications() {
        fetch('/api/notificacoes/nao_visualizadas')
            .then(response => response.json())
            .then(data => {
                // Se não houver notificações não lidas, buscar as 5 mais recentes
                if (data.length === 0) {
                    fetch('/api/notificacoes/recentes')
                        .then(response => response.json())
                        .then(dataRecentes => renderNotificationList(dataRecentes));
                } else {
                    renderNotificationList(data);
                }
            });
    }

    function renderNotificationList(data) {
        if (data.length > 0) {
            notificationDot.style.display = 'inline-block';
        } else {
            notificationDot.style.display = 'none';
        }
        notificationList.innerHTML = '';
        if (data.length === 0) {
            notificationList.innerHTML = '<li>Nenhuma notificação encontrada.</li>';
        } else {
            data.forEach(n => {
                const li = document.createElement('li');
                li.className = n.visualizada ? '' : 'nao-visualizada';
                li.innerHTML = `<span class="mensagem">${n.mensagem}</span> <span class="data">${(n.data_criacao||'').slice(0,16).replace('T',' ')}</span>`;
                notificationList.appendChild(li);
            });
        }
    }

    if (notificationBell) {
        notificationBell.addEventListener('click', function(e) {
            e.stopPropagation();
            if (notificationModal.style.display === 'block') {
                notificationModal.style.display = 'none';
            } else {
                notificationModal.style.display = 'block';
            }
        });
    }
    if (closeNotificationModal) {
        closeNotificationModal.addEventListener('click', function() {
            notificationModal.style.display = 'none';
        });
    }
    // Fechar modal ao clicar fora
    window.addEventListener('click', function(event) {
        if (event.target === notificationModal) {
            notificationModal.style.display = 'none';
        }
    });
    // Atualizar dot periodicamente
    setInterval(fetchNotifications, 20000);
});