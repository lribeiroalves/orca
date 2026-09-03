import { atualizarFatura } from "./filtro_faturas.js";
import { exibirMensagem } from "./flash_messages.js";

function inputValorCompra(event) {
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


function inputParcelaCompra(event) {
    let valorAtual = $(this).val();

    valorAtual = valorAtual.replace(/[^0-9]/g, '');

    if (valorAtual.length > 2) {
        valorAtual = valorAtual.substring(0, 2);
    }

    $(this).val(valorAtual);

    // Validações
    let msg = 'O número de parcelas deve ser entre 1 e 99.';
    let valorInt = parseInt(valorAtual, 10);
    if (valorInt < 1 || valorInt > 99) {
        this.setCustomValidity(msg);
    } else {
        this.setCustomValidity("");
    }
};

function inputDescCompra(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
    }
};


function alterarMes(dataOriginal, mesesParaAdicionar) {
    // 1. Cria uma cópia da data para não modificar a original
    const novaData = new Date(dataOriginal.getTime());
    
    // 2. Trava o dia no dia 1 usando UTC para evitar problemas de fuso horário
    novaData.setUTCDate(1);
    
    // 3. Altera o mês usando UTC (o JS corrige o ano automaticamente aqui)
    novaData.setUTCMonth(novaData.getUTCMonth() + mesesParaAdicionar);
    
    return novaData;
}


function inputDataCompra(event) {
    let valorAtual = $(this).val();

    if (event.type == 'keydown') {
        if (event.key === '/') {
            event.preventDefault();
        } else if (event.key == 'Backspace') {
            if (valorAtual.slice(-1) === '/') {
                valorAtual = valorAtual.slice(0, -1);
            }
        }
    } else if (event.type == 'input') {
        // Deixa apenas numeros e barras
        valorAtual = valorAtual.replace(/[^0-9/]/g, '');
    
        // separa por barras quando dia e mes tem 2 caracteres
        if (valorAtual.length === 2 || valorAtual.length === 5){
            valorAtual += '/';
        }
        
        // garante que o ano tenha no maximo 4 caracteres
        const partes = valorAtual.split('/');
        if (partes.length === 3 && partes[2].length > 3) {
            valorAtual = valorAtual.substring(0, 10);
        }
        
        if (valorAtual.length === 10) {
            try {
                // 1. Divide a string "dd/mm/yyyy" pelas barras
                const partes = valorAtual.split('/'); // Ex: ["25", "10", "2026"]
                
                // 2. Garante que a string tinha o formato esperado com 3 partes
                if (partes.length !== 3) {
                    throw new Error('Formato incorreto. Use DD/MM/YYYY.');
                }

                // 3. Monta no formato ISO: "YYYY-MM-DD"
                const stringFormatada = `${partes[2]}-${partes[1]}-${partes[0]}`;
                
                // 4. Cria a data com a string corrigida
                const data = new Date(stringFormatada);

                // 5. Verifica se o JavaScript aceitou a data
                if (isNaN(data.getTime())) {
                    throw new Error('Data inválida.');
                }

                // O código abaixo garante que o dia/mês digitados são exatamente os reais.
                const diaDigitado = parseInt(partes[0], 10);
                const mesDigitado = parseInt(partes[1], 10);
                // data.getUTCDate evita problemas de fuso horário na validação
                if (data.getUTCDate() !== diaDigitado || (data.getUTCMonth() + 1) !== mesDigitado) {
                    throw new Error('Data não existe no calendário.');
                }

                // Se passou em tudo, limpa o erro de validação
                this.setCustomValidity("");

                // Construção dos choices de faturas
                const faturaAnterior = alterarMes(data, -1);
                const faturaSeguinte = alterarMes(data, 1);
                const mesAtual = data.getUTCMonth() + 1;
                const anoAtual = data.getUTCFullYear();
                const mesAnterior = faturaAnterior.getUTCMonth() + 1;
                const anoAnterior = faturaAnterior.getUTCFullYear();
                const mesSeguinte = faturaSeguinte.getUTCMonth() + 1;
                const anoSeguinte = faturaSeguinte.getUTCFullYear();
                const meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
                const options = `
                                <option value="${anoAnterior}${mesAnterior}">${meses[(mesAnterior-1) % 12]} - ${anoAnterior}</option>
                                <option value="${anoAtual}${mesAtual}">${meses[(mesAtual-1) % 12]} - ${anoAtual}</option>
                                <option value="${anoSeguinte}${mesSeguinte}">${meses[(mesSeguinte-1) % 12]} - ${anoSeguinte}</option>
                                `;

                $('#faturaCompra').empty().append(options);

                if (data.getUTCDate() >= 15) {
                    $('#faturaCompra option:last').prop('selected', true);
                } else {
                    $('#faturaCompra option').eq(1).prop('selected', true);
                }
            } catch (error) {
                this.setCustomValidity(error.message);
                $('#faturaCompra').empty().append('<option value="">Data Inválida!</option>');
            }
        } else if (valorAtual.length === 0) {
            $('#faturaCompra').empty().append('<option value="">...</option>');
        } else {
            $('#faturaCompra').empty().append('<option value="">Data Incompleta!</option>');
        }
    }

    $(this).val(valorAtual);
};


$(function() {
    $('#valorCompra').on('input', inputValorCompra);
    $('#parcelaCompra').on('input', inputParcelaCompra);
    $('#descCompra').on('keydown', inputDescCompra);
    $('#dataCompra').on('input keydown', inputDataCompra);

    $('#btnNovaCompra').on('click', function(event) {
        $('#modalCompra').modal('show');
        $('#modalCompraLabel').text($(this).data('titulo'));
        $('#hashCompra').val(0);
        $('#formCompra')[0].reset();
        $('#faturaCompra').empty().append('<option value="">...</option>');
        $('#divTabelaCompra').hide();
        $('#btnCompraExcluir').hide();
        $('#divBotoesCompra').removeClass('justify-content-between justify-content-lg-evenly');
        $('#divBotoesCompra').addClass('justify-content-end');
    })

    $('#tableBodyFaturas').on('click', 'tr', function(event) {
        $('#divTabelaCompra').show();
        $('#modalCompraLabel').text($(this).data('titulo'));
        $('#modalCompra').modal('show');
        $('#btnCompraExcluir').show();
        $('#divBotoesCompra').addClass('justify-content-between justify-content-lg-evenly');
        $('#divBotoesCompra').removeClass('justify-content-end');
        
        const hash = $(this).data('hash');
        const url = $('#tableBodyFaturas').data('url');
        const linha_id = $(this).data('id');
        
        const data = $(this).find('td').eq(1).text().trim();
        const parcelas = $(this).find('td').eq(6).text().split('/')[1].trim();
        $('#btnConfirmaExclusao').attr('data-hash', hash);
        
        $.ajax({
            url: url,
            method: 'GET',
            data: {hash: hash},
            success: function(resposta) {
                const linhas = resposta.data;
                let tableContent = '';

                for (let linha of linhas) {
                    const meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
                    const faturaFormatada = `${meses[linha.fatura_mes-1]} - ${linha.fatura_ano}`;
                    const valFormatado = parseFloat(linha['valor_parcela']).toLocaleString('pt-BR', { minimumFractionDigits: 2 });

                    tableContent += `
                    <tr>
                        <td class="text-center text-muted text-nowrap">
                            ${faturaFormatada}
                        </td>
                        <td class="text-center fw-medium text-nowrap">
                            R$ ${valFormatado}
                        </td>
                        <td class="text-center text-muted">
                            <small>${`${linha['parcelas']}`.slice(0, -2)} / ${Number(`${linha['parcelas']}`.slice(-2))}</small>
                        </td>
                    </tr>`;
                }
                $('#tableBodyCompras').html(tableContent);
            },
            error: function(resposta) {
                console.error(resposta.message);
            },
            complete: function(resposta) {
                if (resposta.responseJSON.status == 'success') {
                    const dados = resposta.responseJSON.data[0];
                    $('#userCompra').val(dados.user_id);
                    $('#bancoCompra').val(dados.banco_id);
                    $('#categoriaCompra').val(dados.categoria_id);
                    $('#dataCompra').val(data);
                    $('#dataCompra').trigger('input');
                    $('#valorCompra').val(dados.valor_total);             
                    $('#valorCompra').trigger('input');
                    $('#descCompra').val(dados.descricao);
                    $('#hashCompra').val(dados.hash);
                    $('#parcelaCompra').val(parcelas);

                    $('#btnConfirmaExclusao').attr('data-id', linha_id);
                }
            }
        })
    });

    $('#formCompra').on('submit', function(event) {
        event.preventDefault();

        const dadosFormulario = $(this).serialize();
        const url = $(this).attr('action');

        const btn = $('#formCompraSubmit');
        const textoOriginal = btn.text();
        btn.prop('disabled', true).text('Enviando...');

        $.ajax({
            url: url,
            method: 'POST',
            data: dadosFormulario,
            success: function(resposta) {
                if (resposta.status === 'success') {
                    atualizarFatura(resposta.ano, resposta.mes, 'mes');
                    $('#modalCompra').modal('hide');
                    exibirMensagem('Compra Registrada/Atualizada com Sucesso!')
                } else if (resposta.status === 'error') {
                    alert('Houve um erro!')
                } else {
                    alert('O servidor nao respondeu corretamente.')
                }
            },
            error: function(erro) {
                console.log("Erro na requisição:", erro);
                alert("Ocorreu um erro ao salvar a compra. Tente novamente.");
            },
            complete: function() {
                btn.prop('disabled', false).text(textoOriginal);
            }
        });
    });

    $('#btnCompraExcluir').on('click', function() {
        $('#modalCompra').modal('hide');
        $('#modalExclusao').modal('show');
    });

    $('#modalExclusao').on('hidden.bs.modal', function() {
        if ($(this).data('ignorar-retorno') === true) {
            $(this).data('ignorar-retorno', false);
        } else {
            $('#modalCompra').modal('show');
        }
    });

    $('#btnConfirmaExclusao').on('click', function() {
        const url = $(this).data('url');
        const hash = $(this).data('hash');
        const id = $(this).data('id');
        const parametros = {hash: hash, id: id}


        $.ajax({
            url: url,
            method: 'GET',
            data: parametros,
            success: function(resposta) {
                atualizarFatura(resposta.ano, resposta.mes, 'mes');
                exibirMensagem('Compra Excluída com Sucesso!')
            },
            error: function(resposta) {
                console.error(resposta);
            },
            complete: function(r) {
                const resposta = r.responseJSON;
                $('#modalExclusao').data('ignorar-retorno', true);
                $('#modalExclusao').modal('hide');
            }
        });
    });
});