const formatarReais = (valor) => {
    return 'R$ ' + valor.toLocaleString('pt-BR', { 
        minimumFractionDigits: 2, 
        maximumFractionDigits: 2 
    });
};


$(function() {
    const labels_es = $('#graf-es').data('label');
    const values_es = $('#graf-es').data('values');
    const labels_p = $('#graf-p').data('label');
    const values_p = $('#graf-p').data('values');

    new Chart($('#graf-es'), {
        type: 'bar',
        plugins: [ChartDataLabels],
        data: {
            labels: labels_es,
            datasets: [{
                label: '',
                data: values_es,
                backgroundColor: ['rgba(255, 255, 224, 0.6)', 'rgba(255, 182, 193, 0.6)'],
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    grace: '15%',
                    ticks: {
                        callback: function(value) {
                            return 'R$ ' + value.toLocaleString('pt-BR');
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },

                // 1. Configuração do Tooltip (Hover)
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                // Pegamos o valor exato do eixo Y
                                let valor = context.parsed.y;
                                return formatarReais(valor);
                            }
                        }
                    },
                    
                    // 2. Configuração do DataLabels (Texto no topo da barra)
                    datalabels: {
                        anchor: 'end',  // Ancora o texto no final da barra (topo)
                        align: 'end',   // Alinha para fora/cima da barra
                        formatter: function(value) {
                            return formatarReais(value);
                        },
                        font: {
                            weight: 'bold'
                        },
                        color: '#333' // Cor do texto
                    }
            }
        }
    });

});