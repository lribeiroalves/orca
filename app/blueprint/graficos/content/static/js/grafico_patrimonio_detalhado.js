import { exibirMensagem } from "/webui/static/js/flash_messages.js";

function graficoPatrimonioDetalhado() {
    const url = $('#btnPatrimonioDetalhado').data('url');
    const parametros = {};

    $.ajax({
        url: url,
        method: 'GET',
        data: parametros,
        success: function(resposta) {
            if (resposta.status !== 'ok') {
                exibirMensagem('Houve um erro na criação do gráfico!');
                return;
            }

            const graficoCriado = Chart.getChart('graf');
            if (graficoCriado) {
                graficoCriado.destroy();
            }
        },
        error: function(resposta) {

        },
        complete: function(r) {
            const resposta = r.responseJSON;
            $('#tituloGrafico').text('Patrimônio Detalhado');
            $('#placeholder').addClass('d-none');
            $('#chartWrapper').removeClass('d-none');
            $('#offcanvas').offcanvas('hide');
            $('#divPatrimonio').addClass('d-none');
            $('#divPatrimonioDetalhado').removeClass('d-none');
        }
    });
}


$(function() {
    $('#btnPatrimonioDetalhado').on('click', function(event) {
        event.preventDefault();
        graficoPatrimonioDetalhado();
    });
});