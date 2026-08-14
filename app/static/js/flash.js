setTimeout(function () {
    // Seleciona todos os elementos com a classe 'alert' dentro do container de flash
    let alerts = document.querySelectorAll('#flash-messages .alert');
    
    alerts.forEach(function (alert) {
        // Usa a API nativa do Bootstrap 5 para fechar o alerta com animação
        let bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    });
}, 3000);