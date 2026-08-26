let bancoSelected = null;
let userSelected = null;
let dados_global;
let users_global;

function construirDropdown(anos, meses) {
    meses_nomes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
    
    // Dropdown Anos
    let anosContent = '';
    for (let i = 0; i < anos.length; i++) {
        anosContent += `<li>
                            <a id="ano${anos[i]}" href="#" class="dropdown-item" data-ano="${anos[i]}">${anos[i]}</a>
                        </li>`
    }
    $('#anosDropdownMenu').html(anosContent);

    // Dropdown Meses
    let mesesContent = '';
    meses.sort((a, b) => meses_nomes.indexOf(a) - meses_nomes.indexOf(b));
    for (let i = 0; i < meses.length; i++) {
        mesesContent += `<li>
                            <a id="mes${meses[i]}" href="#" class="dropdown-item" data-mes="${meses_nomes.indexOf(`${meses[i]}`)+1}">${meses[i]}</a>
                        </li>`
    }
    $('#mesesDropdownMenu').html(mesesContent);
}


function construirTabela() {
    let tableContent = '';
    let contagem_linhas = 0;
        
    for (let item of dados_global) {
        if ((userSelected === null || userSelected === item['user_id']) && (bancoSelected === null || bancoSelected === item['banco_id'])) {
            contagem_linhas ++;
            let dataFormatada = new Date(item['data']).toLocaleDateString('pt-BR', { timeZone: 'UTC' });
            let valTotalFormatado = parseFloat(item['valor_total']).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
            let valParcelaFormatado = parseFloat(item['valor_parcela']).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
            let userName = item['user_name'].charAt(0).toUpperCase() + item['user_name'].slice(1);
    
            tableContent += `
            <tr>
                <td class="text-start">
                    <span id=user-tabela class="badge" style="background-color: ${users_global[item['user_id']][1]}; color: ${users_global[item['user_id']][2]}">${userName}</span>
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
                <td class="text-center text-capitalize">
                    ${item['banco']}
                </td>
            </tr>`;
        }
    }
    if (contagem_linhas === 0) {
        $('#div-table').hide()
        $('#div-noTable').show()
    } else {
        $('#div-table').show()
        $('#div-noTable').hide()
    }
    $('#tableBodyFaturas').html(tableContent);
}


function construirDashboard(resposta) {
    if (resposta['dados']){
        $('#contentCompras').show();
        $('#no-contentCompras').hide();
        let valTotalFatura = 'R$ ' + parseFloat(resposta['total_fatura']).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
        $('#cardTotalGeral').text(valTotalFatura);
    
        let user_html = ''
        for (let [index, user] of Object.entries(resposta['users'])) {
            let valorUsuario = 'R$ ' + parseFloat(resposta['total_por_usuario'][index-1]).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
            user_html += `
            <div class="card-dash rounded p-2" data-user="${index}">
                <span class="d-block text-muted small"><i class="bi bi-person-fill me-1"></i>${capitalizar(user[0])}</span>
                <span class="d-block fw-bold  text-dark">${valorUsuario}</span>
            </div>
            `
        }
        $('#containerTotaisUsuarios').html(user_html);

        let banco_html = ''
        for (let [index, banco] of Object.entries(resposta['bancos'])) {
            let valorBanco = 'R$ ' + parseFloat(banco[1]).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
            banco_html += `
            <div class="card-dash rounded p-2" data-banco="${index}">
                <span class="d-block text-muted small"><i class="bi bi-bank me-1"></i>${capitalizar(banco[0])}</span>
                <span class="d-block fw-bold  text-dark">${valorBanco}</span>
            </div>
            `
        }
        $('#containerTotaisBancos').html(banco_html);

        dados_global = resposta['dados'];
        users_global = resposta['users'];
        construirTabela();
    } else {
        $('#contentCompras').hide();
        $('#no-contentCompras').show();
    }
}

function capitalizar(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}


function atualizarFatura(ano, mes, tipo) {
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    parametros = {
        ano: ano,
        mes: mes,
        tipo: tipo
    };

    url = $('#dropItemsMes').data('url');
    return $.get(url, parametros, function(resposta) {
        construirDropdown(resposta['anos'], resposta['meses']);
        if (tipo === "mes"){
            construirDashboard(resposta);
        }

        $('#dropItemsAno').text(ano);
        $('#dropItemsMes').text('Selecione...');
        if (tipo === "mes") {
            $('#dropItemsMes').text(resposta['meses'][0]);
            $('#identificadorFatura').text(`${meses[mes-1]} / ${ano}`);
        }
    });    
}


// Execução assim que a página é carregada
$(function() {
    now = new Date();
    year = now.getFullYear();
    month = now.getMonth() + 1;

    $('#mesesDropdownMenu').on('click', '.dropdown-item', function(evento) {
        evento.preventDefault();

        const mes = $(this).data("mes");
        const ano = $('#dropItemsAno').text();
        userSelected = null;
        bancoSelected = null;
        atualizarFatura(ano, mes, 'mes');

    });

    $('#anosDropdownMenu').on('click', '.dropdown-item', function(evento) {
        evento.preventDefault();

        const mes = month;
        const ano = $(this).data("ano");
        atualizarFatura(ano, mes, 'ano');
    });

    $('#containerTotaisUsuarios').on('click', ' .card-dash', function(event) {
        let possui_classe = $(this).hasClass('ativo');
        $('#containerTotaisUsuarios .card-dash').removeClass('ativo');
        userSelected = null;
        if (!possui_classe) {
            $(this).addClass('ativo');
            userSelected = $(this).data('user');
        }
        construirTabela();
    });

    $('#containerTotaisBancos').on('click', ' .card-dash', function(event) {
        let possui_classe = $(this).hasClass('ativo');
        $('#containerTotaisBancos .card-dash').removeClass('ativo');
        bancoSelected = null;
        if (!possui_classe) {
            $(this).addClass('ativo');
            bancoSelected = $(this).data('banco');
        }
        construirTabela();
    });

    atualizarFatura(year, month, 'mes').done(function() {
        $('#dropItemsAno').text('Selecione...');
        $('#dropItemsMes').text('Selecione...');
        $('#mesesDropdownMenu').html("");
    });
});
