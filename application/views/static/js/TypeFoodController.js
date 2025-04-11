class TypeFoodController {
    base_url =  "/honey/";
    
    createTypeFood(){
        const btn_create = document.getElementById("btn-create-type-food");
        const input_name_type = document.getElementById("name_type");
        const description = document.getElementById("description");
        const input_image = document.getElementById("image");

        btn_create.addEventListener("click", async function(){
            if (input_name_type.value.length > 0){
                btn_create.textContent = "Guardando...";
                btn_create.disabled = true;
                const form_data = new FormData();
                form_data.append("name_type", input_name_type.value);
                form_data.append("description", description.value);
                form_data.append("image", input_image.value);
                
                await fetch ("typefoodabs",{
                    method: "POST",
                    body: form_data,
                }).then(res => res.text()).then(data =>{
                    btn_create.textContent = "Guardado";
                    location.reload();
                });
            }else{
                alert("Complete los campos requeridos");
            }
        })
    }
    deleteTypeFood(){
        const btn_delete = document.getElementById("btn-delete-type-food");
        const btns_del = document.querySelectorAll(".btn-del-more-data");
        let identifier = null;
        btns_del.forEach((btn) =>{
            btn.addEventListener("click", ()=>{
                identifier = btn.dataset.identifier;
                openModal(document.getElementById("modal-delete"));
            })
        })
        btn_delete.addEventListener("click", async() =>{
            if (identifier){
                btn_delete.textContent = "Eliminando";
                btn_delete.disabled = true;
                await fetch("typefoodroute_delete?row="+String(identifier)).then(res=>res.text()).then(data=>{
                    location.reload();
                })
            }else{
                alert("Ocurrió un error, vuelve a selecionar tipo de plato")
            }
        })
    }
    editTypeFood(){
        const btns_open_modal = document.querySelectorAll(".btn-edit-more-data");
        const btn_confirm = document.getElementById("btn-edit-type-food");
        let identifier = null;
        const input_name_type = document.getElementById("name_type-edit");
        const input_image = document.getElementById("image-edit");
        const description = document.getElementById("description-edit");
        btns_open_modal.forEach((btn) =>{
            btn.addEventListener("click", async()=>{
                openModal(document.getElementById("modal-edit"));
                identifier = btn.dataset.identifier;
                await fetch(this.base_url +"typefoodabs_view?row="+String(identifier)).then(res => res.json()).then(data=>{
                    description.value = data.description;
                    input_name_type.value = data.name_type;
                });
            })
        })
        btn_confirm.addEventListener("click", async()=>{
            if (identifier ){
                btn_confirm.textContent = "Actualizando...";
                btn_confirm.disabled = true;
                const form_data = new FormData();
                form_data.append("row", identifier);
                form_data.append("name_type", input_name_type.value);
                form_data.append("description", description.value);
                form_data.append("image", input_image.value);
                await fetch(this.base_url + "typefoodroute_update",{
                    method: "POST",
                    body: form_data,
                }).then(res => res.text()).then(data =>{
                    if (data === "ok"){
                        btn_confirm.textContent = "Actualizado";
                        location.reload();
                    }else{
                        alert("Ocurrió un error");        
                    }
                });
            }else{
                alert("Ocurrió un error");
            }
        })
    }
    updateStateTypeFood(){
        const btns_open_modal = document.querySelectorAll(".btn-lock-more-data");
        const btn_confirm = document.getElementById("btn-lock-update-save");
        let identifier = null;
        let state = null;
        btns_open_modal.forEach((btn) =>{
            btn.addEventListener("click", ()=>{
                identifier = btn.dataset.identifier;
                if (parseInt(btn.dataset.state) === 0){
                    state = 1
                    btn_confirm.textContent = "Activar";
                }else if (parseInt(btn.dataset.state) === 1){
                    btn_confirm.textContent = "Desactivar";
                    state = 0
                }else{
                    btn_confirm.textContent = "Error";
                    btn_confirm.setAttribute("disabled", true);
                }
                openModal(document.getElementById("modal-lock"));
            })
        });

        btn_confirm.addEventListener("click", async() =>{
            if (identifier){
                btn_confirm.textContent = "Espere...";
                const form_data = new FormData();
                form_data.append("row", identifier);
                form_data.append("state", state);
                await fetch(this.base_url+"typefoodroute_update",{
                    method: "POST",
                    body: form_data,
                }).then(res => res.text()).then(data =>{
                    if (data === "ok"){
                        location.reload();
                    }else{
                        alert("Ocurrió un error");
                    }
                })
            }
        })   
    }
}