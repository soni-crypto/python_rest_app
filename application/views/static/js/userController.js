const userUpdate = ()=>{
    const btn_update_user   = document.querySelectorAll(".btn-update-user");
    let i = null;
    btn_update_user.forEach(btn=>{
        btn.addEventListener("click", async()=>{
            i = btn.dataset.i;       
            await fetch("/honey/user/get?i="+String(i)).then(res => res.json()).then(data =>{
                if (data){
                    const res_ = JsonToForm("form-update-user", data);
                    console.log(res_);
                    openModal(document.getElementById("modal-update-user"));
                }
            }).catch(err =>{
                console.log(err);
            })
        })
    })
    const btn_update_confirm = document.getElementById("btn-update-confirm");
    btn_update_confirm.addEventListener("click", async()=>{
        if (i){
            btn_update_confirm.textContent = "Actualizando...";
            btn_update_confirm.disabled = true;
            const form_data = new FormData(document.getElementById("form-update-user"));
            await fetch ("/honey/user/update", {
                method : "post",
                body: form_data,
            }).then(res => res.json()).then((data)=>{
                location.reload();
            })
        }
    })
}
const userDelete = () =>{
    const btn_delete_user = document.querySelectorAll(".btn-delete-user");
    let i = null;
    btn_delete_user.forEach(btn =>{
        btn.addEventListener("click", ()=>{
            i = btn.dataset.i;
            openModal(document.getElementById("modal-confirm-delete"));
        })
    })
    const btn_delete_confirm = document.getElementById("btn-delete-confirm");
    btn_delete_confirm.addEventListener("click", async()=>{
        if (i){
            btn_delete_confirm.textContent = "Eliminando...";
            btn_delete_confirm.disabled = true;
            await fetch("/honey/user/delete?i="+String(i)).then(res => res.json()).then((data)=>{
                location.reload();
            })
        }
    })
}