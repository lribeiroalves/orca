function submeterNovaData(novoMes, novoAno, user) {
    const selectMes = document.getElementById('mes');
    const selectAno = document.getElementById('ano');
    const selectUser = document.getElementById('user');
    
    selectMes.value = novoMes;
    selectUser.value = user;

    let option_exists = [...selectAno.options].find(opt => opt.value === novoAno);
    if (option_exists) {
        selectAno.value = novoAno;
    } else {
        let newOption = new Option("Novo Ano", novoAno);
        selectAno.add(newOption);
        selectAno.value = novoAno;
    }
    
    console.log(selectMes.value);
    console.log(selectAno.value);
    console.log(selectUser.value);
    
    form = document.getElementById('formFiltro');
    form.submit()
}