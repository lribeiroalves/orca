import { exibirMensagem } from "/webui/static/js/flash_messages.js";

let graficoCriado;
let options = null;

function graficoPatrimonio(ano=0, user=0) {
    const url = $('#btnPatrimonio').data('url');
    const parametros = {
        ano: ano,
        user: user
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

            const datasetsConstruidos = resposta.series.map((item, index) => {
                const cor = resposta.cores[index];

                return {
                label: item.label,
                data: item.valores,
                backgroundColor: cor,
                borderColor: cor.replace('0.7', '1'), // Remove a transparência para a borda
                borderWidth: 1
                };
            });

            if (graficoCriado) {
                graficoCriado.destroy();
            }

            // Calcula a largura ideal (ex: 50 pixels por cada mês no eixo X)
            const quantidadeMeses = resposta.meses.length;
            const larguraIdealMobile = quantidadeMeses * 50; 

            // Se a tela for pequena (< 1057px), aplica a largura dinâmica forçando o scroll
            if (window.innerWidth < 1057) {

                $('#containerGraf').parent().removeClass('p-3');
                $('#chartWrapper').css('min-width', `${larguraIdealMobile}px`);
            } else {
                // No desktop, volta ao comportamento padrão preenchendo a tela
                $('#chartWrapper').css('min-width', '100%');
            }

            graficoCriado = new Chart($('#graf'), {
                type: 'bar',
                data: {
                    labels: resposta.meses,
                    datasets: datasetsConstruidos
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            grid: {display: false}
                        },
                        xAnos: {
                            type: 'category',
                            position: 'bottom',
                            labels: resposta.meses,
                            grid: { drawOnChartArea: false, drawTicks: false },
                            ticks: {
                                font: { weight: 'bold', size: 14 },
                                padding: 5,
                                color: '#666',
                                callback: function(value, index) {
                                    if (index % 12 === 6) {
                                        return resposta.anos[index];
                                    }
                                    return '';
                                }
                            }
                        },
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
            $('#tituloGrafico').text('Patrimônio Líquido');
            const anos_unicos = [...new Set(resposta.anos)];
            if (!options) {
                options = '';
                for (ano of anos_unicos) {
                    options += `<li><a class="dropdown-item" href="#" data-value=${ano}>${ano}</a></li>`
                }
                options += `<li><a class="dropdown-item" href="#" data-value="0">Todo o período</a></li>`;
                $('#dropDownPatrimonio').html(options);
            }
            $('#divPatrimonio').removeClass('d-none');
        },
        error: function(resposta) {
            console.log(resposta);
        },
        complete: function(r) {
            const resposta = r.responseJSON;
            $('#placeholder').addClass('d-none');
            $('#chartWrapper').removeClass('d-none');
            $('#offcanvas').offcanvas('hide');
        }
    });
}

$(function() {
    $('#btnPatrimonio').on('click', function(event) {
        event.preventDefault();
        graficoPatrimonio();
    })
    $('#dropDownPatrimonio').on('click', '.dropdown-item', function(event) {
        event.preventDefault();
        const ano = $(this).data('value');
        graficoPatrimonio(ano);
    });
})