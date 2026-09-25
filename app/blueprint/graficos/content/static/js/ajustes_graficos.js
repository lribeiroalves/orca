export function ajuste_tamanho(largura) {
    // Calcula a largura ideal (ex: 50 pixels por cada mês no eixo X)
    const larguraIdealMobile = largura * 50; 

    // Se a tela for pequena (< 1057px), aplica a largura dinâmica forçando o scroll
    if (window.innerWidth < 1057) {

        $('#containerGraf').parent().removeClass('p-3');
        $('#chartWrapper').css('min-width', `${larguraIdealMobile}px`);
    } else {
        // No desktop, volta ao comportamento padrão preenchendo a tela
        $('#chartWrapper').css('min-width', '100%');
    }
}