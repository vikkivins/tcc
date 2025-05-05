document.addEventListener('DOMContentLoaded', function() {
    // Função para truncar texto
    function truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength - 3) + '...';
    }
    
    // Edição de comentário
    document.addEventListener('click', function(e) {
        // Botão de editar comentário
        if (e.target.classList.contains('btn-editar')) {
            const comentarioDiv = e.target.closest('.comentario');
            const conteudo = comentarioDiv.querySelector('.comentario-conteudo');
            const formEdicao = comentarioDiv.querySelector('.form-editar-comentario');
            
            conteudo.style.display = 'none';
            formEdicao.style.display = 'block';
            e.target.style.display = 'none';
        }
        
        // Botão de cancelar edição
        if (e.target.classList.contains('btn-cancelar-edicao')) {
            const form = e.target.closest('.form-editar-comentario');
            const comentarioDiv = form.closest('.comentario');
            
            form.style.display = 'none';
            comentarioDiv.querySelector('.comentario-conteudo').style.display = 'block';
            comentarioDiv.querySelector('.btn-editar').style.display = 'inline';
        }
        
        // Botão de responder comentário
        if (e.target.classList.contains('btn-resposta')) {
            const comentario = e.target.closest('.comentario');
            const form = comentario.querySelector('.form-resposta');
            const conteudoComentario = comentario.querySelector('.comentario-conteudo').textContent;
            
            // Verificar se este comentário já é uma resposta aninhada
            const isReply = comentario.getAttribute('data-is-reply') === 'true';
            const comentarioId = comentario.getAttribute('data-comentario-id');
            const paiId = comentario.getAttribute('data-pai-id');
            
            // Se for uma resposta aninhada, vamos redirecionar a resposta para o comentário pai
            if (isReply && paiId) {
                // Vamos procurar o formulário do comentário pai para responder a ele
                const comentarioPai = document.querySelector(`.comentario[data-comentario-id="${paiId}"]`);
                if (comentarioPai) {
                    // Pegar o formulário do comentário pai
                    const formPai = comentarioPai.querySelector('.form-resposta');
                    // Incluir citação do comentário atual
                    const inputCitacao = formPai.querySelector('.comentario-citado');
                    inputCitacao.value = truncateText(conteudoComentario, 150); // Limitar a 150 caracteres
                    
                    const inputAutorCitacao = formPai.querySelector('.comentario-citado-autor');
                    if (inputAutorCitacao) {
                        const autorOriginal = comentario.querySelector('.comentario-cabecalho strong').textContent;
                        inputAutorCitacao.value = autorOriginal;
                    }
                    
                    // Mostrar o formulário pai e esconder o botão resposta do pai
                    formPai.style.display = 'block';
                    comentarioPai.querySelector('.btn-resposta').style.display = 'none';
                    
                    // Rolar até o formulário
                    formPai.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    formPai.querySelector('textarea').focus();
                    
                    // Não mostrar o formulário deste comentário
                    return;
                }
            }
            
            // Comportamento normal para comentários de primeiro nível
            const inputCitacao = form.querySelector('.comentario-citado');
            if (inputCitacao) {
                inputCitacao.value = truncateText(conteudoComentario, 150);
            }
            
            form.style.display = 'block';
            e.target.style.display = 'none';
            form.querySelector('textarea').focus();
        }
        
        // Botão de cancelar resposta
        if (e.target.classList.contains('btn-cancelar')) {
            const form = e.target.closest('.form-resposta');
            const inputCitacao = form.querySelector('.comentario-citado');
            if (inputCitacao) {
                inputCitacao.value = '';
            }
            
            form.style.display = 'none';
            form.closest('.comentario').querySelector('.btn-resposta').style.display = 'inline';
        }
    });
    
    // Envio do formulário de edição
    document.addEventListener('submit', function(e) {
        // Formulário de edição
        if (e.target.classList.contains('form-editar-comentario')) {
            e.preventDefault();
            
            const form = e.target;
            const formData = new FormData(form);
            const comentarioDiv = form.closest('.comentario');
            const btnEditar = comentarioDiv.querySelector('.btn-editar');
            const conteudo = comentarioDiv.querySelector('.comentario-conteudo');
            
            // Mostrar indicador de carregamento
            const btnSalvar = form.querySelector('.btn-salvar');
            btnSalvar.disabled = true;
            btnSalvar.textContent = 'Salvando...';
            
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    conteudo.textContent = data.conteudo;
                    form.style.display = 'none';
                    conteudo.style.display = 'block';
                    btnEditar.style.display = 'inline';
                } else {
                    alert('Erro ao atualizar comentário: ' + (data.error || ''));
                    console.error('Server error:', data);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Erro ao atualizar comentário');
            })
            .finally(() => {
                btnSalvar.disabled = false;
                btnSalvar.textContent = 'Salvar';
            });
        }
        
        // Formulário de resposta
        if (e.target.classList.contains('form-resposta')) {
            e.preventDefault();
            const form = e.target;
            const formData = new FormData(form);
            const btnEnviar = form.querySelector('.btn-enviar');
            
            // Verificar se há citação
            const citacao = form.querySelector('.comentario-citado').value;
            const autorCitacao = form.querySelector('.comentario-citado-autor').value;
            
            // Se há citação, adicionar ao conteúdo da resposta
            if (citacao && citacao.trim() !== '') {
                const textoOriginal = formData.get('conteudo');
                formData.set('conteudo_original', textoOriginal);
                formData.set('citacao', citacao);
                formData.set('citacao_autor', autorCitacao);
            }
            
            // Mostrar indicador de carregamento
            btnEnviar.disabled = true;
            btnEnviar.textContent = 'Enviando...';
            
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                    return;
                }
                return response.json();
            })
            .then(data => {
                if (data && data.success) {
                    // Recarregar a página para mostrar o novo comentário
                    window.location.reload();
                } else if (data) {
                    alert('Erro ao adicionar resposta: ' + (data.error || ''));
                    console.error('Server error:', data);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Erro ao adicionar resposta');
            })
            .finally(() => {
                btnEnviar.disabled = false;
                btnEnviar.textContent = 'Enviar resposta';
            });
        }
    });
});