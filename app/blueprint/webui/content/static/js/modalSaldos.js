function inputAnoSaldo(event) {
    let valorAtual = $(this).val();

    valorAtual = valorAtual.replace(/[^0-9]/g, '');

    if (valorAtual.length > 4) {
        valorAtual = valorAtual.substring(0, 4);
    }

    $(this).val(valorAtual);

    // Validações
    if (valorAtual.length === 0) {
        this.setCustomValidity("O campo precisa ser preenchido.");
    } else if (valorAtual.length > 0 && valorAtual.length < 4) {
        this.setCustomValidity("O ano deve conter exatamente 4 dígitos.");
    } else if (valorAtual.length === 4 && parseInt(valorAtual) < 2026) {
        this.setCustomValidity("O ano não pode ser menor que 2026.");
    } else {
        this.setCustomValidity("");
    }
};

function inputValorSaldo(event) {
    let valorAtual = $(this).val();

    // Deixa apenas numeros, pontos e virgulas
    valorAtual = valorAtual.replace(/[^0-9.,]/g, '');

    // Troca pontos por virgulas
    valorAtual = valorAtual.replace(/\./g, ',');

    const partes = valorAtual.split(',');

    // Nao aceita que o primeiro char seja virgula
    if (partes[0].length === 0) {
        $(this).val('');
        return;
    }

    // Nao aceita que tenha mais de uma virgula
    if (partes.length > 2) {
        valorAtual = partes[0] + ',' + partes.slice(1).join('').replace(/,/g, '');
    }

    // aceita apenas 2 digitos apos a virgula
    const partesFinais = valorAtual.split(',');
    if (partesFinais.length === 2) {
        let decimais = partesFinais[1].substring(0, 2);
        valorAtual = partesFinais[0] + ',' + decimais;
    }

    $(this).val(valorAtual);
};

function abrirModalSaldos(titulo="Inicialização Incorreta", id="", user="", mes="", ano="", valor="", banco="") {
    $('#modalSaldosLabel').text(titulo);

    // Campos do Form
    $('#idSaldo').val(id);
    $('#mesSaldo').val(mes);
    $('#anoSaldo').val(ano);
    $('#userSaldo').val(user);
    $('#bancoSaldo').val(banco);
    $('#valorSaldo').val(valor);

    // binds
    $('#anoSaldo').on('input', inputAnoSaldo);
    $('#valorSaldo').on('input', inputValorSaldo);
    $('#valorSaldo').trigger('input');

    // Abrir modal
    $('#modalSaldos').modal('show');
}