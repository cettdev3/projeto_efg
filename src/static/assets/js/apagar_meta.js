(function(){
    const btnexcluir = document.querySelectorAll(".deleteFromMeta");

btnexcluir.forEach(btn =>{
    btn.addEventListener('click',(e)=>{
        const confirmacao = confirm("Deseja realmente excluir este registro?");
        if(!confirmacao){
            e.preventDefault();
        }
    });
});
    
})();