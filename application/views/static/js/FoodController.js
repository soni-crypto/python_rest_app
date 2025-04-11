class FoodController {
    base_url =  "/honey/";
    
    createFood(){
        const btn_open = document.getElementById("btn-create-ui-main-template");
        btn_open.addEventListener("click", ()=>{
            openModal(document.getElementById("modal-create"));
        })
    }
    editFood(){
        const btns_open_modal = document.querySelectorAll(".btn-edit-more-data");
        const input_name = document.getElementById("name-edit");
        const input_description = document.getElementById("description-edit");
        const input_price = document.getElementById("price-edit");
        const input_product_code = document.getElementById("product_code-edit");
        const input_preparation_time = document.getElementById("preparation_time-edit");
        const input_type_food = document.getElementById("type_food-edit");
        const input_image = document.getElementById("image-edit");
        const btn_confirm = document.getElementById("btn-confirm-update");
        let identifier = null;
        btns_open_modal.forEach(btn =>{
            btn.addEventListener("click",async() => {
                identifier = btn.dataset.identifier;
                await fetch(this.base_url+"updatefoods?row="+String(identifier)).then(res => res.json()).then(data=>{
                    if (data){
                        openModal(document.getElementById("modal-edit"));
                        input_name.value = data.name;
                        input_description.value = data.description;
                        input_price.value = data.price;
                        input_preparation_time.value = data.preparation_time;
                        input_type_food.value = data.type_food;
                        input_product_code.value = data.product_code;
                    }else{
                        alert("Ocurrió un error");
                    }
                })
            })
        })
        btn_confirm.addEventListener("click", async() =>{
            if (identifier){
                btn_confirm.textContent = "Actualizando...";
                btn_confirm.disabled = true;
                const form_data = new FormData();
                form_data.append("row", identifier);
                form_data.append("name", input_name.value);
                form_data.append("description", input_description.value);
                form_data.append("price", input_price.value);
                form_data.append("preparation_time", input_preparation_time.value);
                form_data.append("product_code", input_product_code.value);
                form_data.append("type_food", input_type_food.value);
                form_data.append("image", input_image.value);
                await fetch(this.base_url+"updatefoods",{
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
            }
        })
    }
    deleteFood(){
        const btn_delete = document.getElementById("btn-delete-type-food");
        const btns_del = document.querySelectorAll(".btn-del-more-data");
        let identifier = null;
        btns_del.forEach((btn) =>{
            btn.addEventListener("click", ()=>{
                openModal(document.getElementById("modal-delete"));
                identifier = btn.dataset.identifier;
            })
        })
        btn_delete.addEventListener("click", async() =>{
            if (identifier){
                btn_delete.textContent = "Eliminando...";
                btn_delete.disabled = true;
                await fetch(this.base_url + "delete_f_d?row="+String(identifier)).then(res=>res.text()).then(data=>{
                    btn_delete.textContent = "Eliminado";
                    location.reload();
                })
            }else{
                alert("Ocurrió un error")
            }
        })
    }
    updateStateFood(){
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
                btn_confirm.disabled = true;
                const form_data = new FormData();
                form_data.append("row", identifier);
                form_data.append("state", state);
                await fetch(this.base_url+"updatefoods",{
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