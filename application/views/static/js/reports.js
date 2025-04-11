const config = () =>{
    let open = true;
    const btn_config = document.getElementById("btn-config");
    const box = document.getElementById("container-config");
    btn_config.addEventListener("click", ()=>{
        if (open){
            box.classList.remove("block-2-close");
            open = false;
        }else{
            box.classList.add("block-2-close");
            open = true;
        }
    })
    
}