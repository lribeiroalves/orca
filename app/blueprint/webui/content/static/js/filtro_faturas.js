function construirDropdown(anos, meses) {

    // Dropdown Anos
    let anosContent = '';
    for (let i = 0; i < anos.length; i++) {
        anosContent += `<li>
                            <a id="ano${anos[i]}" href="#" class="dropdown-item">${anos[i]}</a>
                        </li>`
    }
    $('#anosDropdownMenu').html(anosContent);

    // Dropdown Meses
    let mesesContent = '';
    for (let i = 0; i < meses.length; i++) {
        mesesContent += `<li>
                            <a id="mes${meses[i]}" href="#" class="dropdown-item">${meses[i]}</a>
                        </li>`
    }
    $('#mesesDropdownMenu').html(mesesContent);
}


// Execução assim que a página é carregada
$(function() {
    url = $('#dropItemsMes').data('url');
    now = new Date();
    year = now.getFullYear();
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    month = now.getMonth() + 1;
    mes_nome = meses[month - 1]
    

    parametros = {
        ano: year,
        mes: month,
        tipo: 'mes'
    };

    $('#dropItemsAno').text(year);
    $('#dropItemsMes').text(mes_nome);


    $.get(url, parametros, function(resposta) {
        construirDropdown(resposta[0]['anos'], resposta[1]['meses']);

        // CONSTRUIR TABELA
    });

});
