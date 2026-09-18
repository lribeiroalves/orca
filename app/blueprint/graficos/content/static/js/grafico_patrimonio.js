$(function() {
    $('#btnPatrimonio').on('click', function(event) {
        event.preventDefault();

        const url = $(this).data('url');

        $.ajax({
            url: url,
            method: 'GET',
            data: {},
            success: function(resposta) {
                console.log(resposta);
            },
            error: function(resposta) {
                console.log(resposta);
            },
            complete: function(r) {
                const resposta = r.responseJSON;
            }
        });
    })
})