function formExcluir(id='', tipo='', ano='', mes='', user='') {
    $('#idExcluir').val(id);
    $('#tipoExcluir').val(tipo);
    $('#anoExcluir').val(ano);
    $('#mesExcluir').val(mes);
    $('#userExcluir').val(user);

    $('#formExcluir').submit();
}