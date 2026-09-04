export function exibirMensagem(mensagem, time=3000, tipo="warning") {
    let $alerta = $(`
        <div class="alert alert-${tipo} alert-dismissible fade show text-center mx-5" role="alert">
            ${mensagem}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `);

    $('#flash-messages').append($alerta);

    setTimeout(function () {
        if ($.contains(document, $alerta[0])) {
            
            let bsAlert = new bootstrap.Alert($alerta[0]);
            bsAlert.close();
        }
    }, time);
}
