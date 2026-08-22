function submeterNovaData(novoMes, novoAno, user, tipo='entrada') {
    const selectMes = document.getElementById('mes');
    const selectAno = document.getElementById('ano');
    const selectUser = document.getElementById('user');
    const campoTipo = document.getElementById('tipo');
    
    selectMes.value = novoMes;
    selectUser.value = user;
    campoTipo.value = tipo;

    let option_exists = [...selectAno.options].find(opt => opt.value === novoAno);
    if (option_exists) {
        selectAno.value = novoAno;
    } else {
        let newOption = new Option("Novo Ano", novoAno);
        selectAno.add(newOption);
        selectAno.value = novoAno;
    }
    
    form = document.getElementById('formFiltro');
    form.submit()
}