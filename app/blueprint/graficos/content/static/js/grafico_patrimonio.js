import { exibirMensagem } from "/webui/static/js/flash_messages.js";

let graficoCriado;

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

            const paletaCores = [
                'rgba(54, 162, 235, 0.7)', // Azul
                'rgba(255, 99, 132, 0.7)', // Vermelho
                'rgba(255, 206, 86, 0.7)', // Amarelo
                'rgba(153, 102, 255, 0.7)' // Roxo
            ];

            const datasetsConstruidos = resposta.series.map((item, index) => {
                // Usa o resto da divisão (%) para recomeçar as cores se houverem mais barras que cores na paleta
                const cor = paletaCores[index % paletaCores.length]; 
                
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
            $('#tituloGrafico').text('Patrimônio');
            const anos_unicos = [...new Set(resposta.anos)];
            let options = ``;
            for (ano of anos_unicos) {
                options += `<li><a class="dropdown-item" href="#" data-value=${ano}>${ano}</a></li>`
            }
            options += `<li><a class="dropdown-item" href="#" data-value="0">Todo o período</a></li>`;
            $('#dropDownPatrimonio').html(options);
            $('#divPatrimonio').removeClass('d-none');
        },
        error: function(resposta) {
            console.log(resposta);
        },
        complete: function(r) {
            const resposta = r.responseJSON;
            $('#offcanvas').offcanvas('hide');
        }
    });
}

$(function() {
    $('#btnPatrimonio').on('click', function(event) {
        event.preventDefault();
        graficoPatrimonio();
    })
})