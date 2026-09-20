$(function() {
    $('#btnPatrimonio').on('click', function(event) {
        event.preventDefault();

        const url = $(this).data('url');

        $.ajax({
            url: url,
            method: 'GET',
            data: {},
            success: function(resposta) {
                const paletaCores = [
                    'rgba(75, 192, 192, 0.7)', // Verde
                    'rgba(255, 99, 132, 0.7)', // Vermelho
                    'rgba(54, 162, 235, 0.7)', // Azul
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

                new Chart($('#graf'), {
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
            },
            error: function(resposta) {
                console.log(resposta);
            },
            complete: function(r) {
                const resposta = r.responseJSON;
                $('#offcanvas').offcanvas('hide');
            }
        });
    })
})