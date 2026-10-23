// Oculta os dados de devolução enquanto o status não representar retorno ou perda.
// Validações reais permanecem no formulário Django do servidor.
(() => {
  const status = document.querySelector('[data-status-emprestimo]');
  if (!status) return;
  const campos = document.querySelectorAll('[data-campo-devolucao]');
  const atualizar = () => {
    const mostrar = ['devolvido', 'danificado', 'perdido'].includes(status.value);
    campos.forEach((campo) => {
      campo.hidden = !mostrar;
      campo.style.display = mostrar ? '' : 'none';
      campo.querySelectorAll('input, textarea').forEach((entrada) => { entrada.disabled = !mostrar; });
    });
  };
  status.addEventListener('change', atualizar);
  atualizar();
})();
