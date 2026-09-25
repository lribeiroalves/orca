import { exibirMensagem } from "/webui/static/js/flash_messages.js";
import { ajuste_tamanho } from "./ajustes_graficos.js";

function graficoPatrimonioDetalhado(tipo='users', ano=0, mes=0, user=0) {
    const url = $('#btnPatrimonioDetalhado').data('url');
    const parametros = {
        ano: ano,
        mes: mes,
        user: user,
        tipo: tipo
    };

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

            ajuste_tamanho(12);

            switch (resposta.tipo) {
                case 'users':
                    let options = '';
                    for (user of resposta.dados.users) {
                        options += `<li><a class="dropdown-item" href="#" data-id=${user.id} data-nome=${user.nome}>${user.nome}</a></li>`
                    }
                    $('#dropPatDetUsers').html(options);
                    break;
                case 'anos':
                    //
                    break;
                case 'meses':
                    //
                    break;
                case 'grafico':
                    //
                    break;
                default:
                    //
            }
        },
        error: function(resposta) {
            console.error(resposta);
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
    $('#dropPatDetUsers').on('click', '.dropdown-item', function(event) {
        event.preventDefault();
        const id = $(this).data('id');
        const user = $(this).data('nome');
        $('#btnDropPatDetUsers').text(`Usuário: ${user}  `);
        graficoPatrimonioDetalhado('anos', 0, 0, id);
    })
});