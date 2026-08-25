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

function capitalizar(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
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
        mes: 1,
        tipo: 'mes'
    };

    $('#dropItemsAno').text(year);
    $('#dropItemsMes').text(mes_nome);
    $('#identificadorFatura').text(`${mes_nome} / ${year}`)


    $.get(url, parametros, function(resposta) {
        console.log(resposta);
        construirDropdown(resposta['anos'], resposta['meses']);

        let valTotalFatura = 'R$ ' + parseFloat(resposta['total_fatura']).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
        $('#cardTotalGeral').text(valTotalFatura);

        let user_html = ''
        for (let [index, user] of Object.entries(resposta['users'])) {
            console.log(resposta['total_por_usuario'][index-1]);
            let valorUsuario = 'R$ ' + parseFloat(resposta['total_por_usuario'][index-1]).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
            user_html += `
            <div>
                <span class="d-block text-muted small"><i class="bi bi-person-fill me-1"></i>${capitalizar(user[0])}</span>
                <span class="d-block fw-bold fs-5 text-dark">${valorUsuario}</span>
            </div>
            `
        }
        $('#containerTotaisUsuarios').html(user_html);

        let tableContent = '';
        
        for (let item of resposta['dados']) {
            let dataFormatada = new Date(item['data']).toLocaleDateString('pt-BR', { timeZone: 'UTC' });
            let valTotalFormatado = parseFloat(item['valor_total']).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
            let valParcelaFormatado = parseFloat(item['valor_parcela']).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
            let userName = item['user_name'].charAt(0).toUpperCase() + item['user_name'].slice(1);

            tableContent += `
            <tr>
                <td class="text-start">
                    <span id=user-tabela class="badge" style="background-color: ${resposta['users'][item['user_id']][1]}">${userName}</span>
                </td>
                <td class="text-start text-muted text-nowrap">
                    ${dataFormatada}
                </td>
                <td class="text-start text-capitalize">
                    ${item['categoria']}
                </td>
                <td class="text-start text-truncate" style="max-width: 150px;" title="${item['descricao']}">
                    ${item['descricao']}
                </td>
                <!-- text-nowrap impede que o 'R$' se separe do número em telas pequenas -->
                <td class="text-end fw-medium text-nowrap">
                    R$ ${valTotalFormatado}
                </td>
                <td class="text-end fw-medium text-nowrap">
                    R$ ${valParcelaFormatado}
                </td>
                <td class="text-center text-muted">
                    <small>${`${item['parcelas']}`.slice(0, -2)} / ${Number(`${item['parcelas']}`.slice(-2))}</small>
                </td>
            </tr>`;
        };
        $('#tableBodyFaturas').html(tableContent);
    });

});
