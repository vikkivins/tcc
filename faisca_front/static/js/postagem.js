function toggleEditMode(postId) {
    const postCard = document.getElementById(`post-${postId}`);
    const viewMode = postCard.querySelector('.view-mode');
    const editMode = postCard.querySelector('.edit-mode');
    
    if (viewMode.style.display === 'none') {
        // Voltando para o modo de visualização
        viewMode.style.display = 'block';
        editMode.style.display = 'none';
    } else {
        // Mudando para o modo de edição
        viewMode.style.display = 'none';
        editMode.style.display = 'block';
        
        // Foca no textarea
        const textarea = editMode.querySelector('textarea');
        textarea.focus();
        // Posiciona o cursor no final do texto
        textarea.selectionStart = textarea.selectionEnd = textarea.value.length;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Formatar todas as datas
    document.querySelectorAll('.datetime').forEach(function(element) {
        const timestamp = element.getAttribute('data-timestamp');
        const date = new Date(timestamp);
        date.setHours(date.getHours() - 3);
        
        // Formatar a data no formato local (DD/MM/YYYY HH:MM)
        element.textContent = date.toLocaleString('pt-BR');
    });
    
    // Adicionar listeners para os formulários de edição
    document.querySelectorAll('.edit-mode form').forEach(function(form) {
        form.addEventListener('submit', function(event) {
            console.log('Formulário de edição enviado:', form.action);
        });
    });
    
    // Adicionar listeners para os formulários de exclusão
    document.querySelectorAll('.delete-form').forEach(function(form) {
        form.addEventListener('submit', function(event) {
            console.log('Formulário de exclusão enviado:', form.action);
        });
    });
});