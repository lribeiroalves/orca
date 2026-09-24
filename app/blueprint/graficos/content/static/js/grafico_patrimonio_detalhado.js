import { exibirMensagem } from "/webui/static/js/flash_messages.js";

function graficoPatrimonioDetalhado() {
    const url = $('#btnPatrimonioDetalhado').data('url');
    const parametros = {};

    $.ajax({
        url: url,
        method: 'GET',
        data: parametros,
        success: function(resposta) {
            
        },
        error: function(resposta) {

        },
        complete: function(r) {
            const resposta = r.responseJSON;
        }
    });
}


$(function() {
    graficoPatrimonioDetalhado();
});