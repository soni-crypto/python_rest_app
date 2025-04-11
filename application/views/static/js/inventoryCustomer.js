const createCustomer = () =>{
    const title_form = document.getElementById("title-form-message-mode");
    const btn_submit = document.getElementById("btn-submit-form");
    const form_customer = document.getElementById("form-customer");
    const btn_start = document.getElementById("btn-open-modal-create-customer");
    btn_start.addEventListener("click", ()=>{
        form_customer.reset();
        title_form.textContent = "Crear nuevo cliente";
        openModal(document.getElementById('modal-create-new-customer'));
        btn_submit.textContent = "Crear";
    });
    form_customer.addEventListener("submit", async(e)=>{
        e.preventDefault();
        const form_data = new FormData(form_customer);
        if (form_customer.dataset.mode === "create"){
            btn_submit.textContent = "Creando...";
            btn_submit.disabled = true;
            await fetch("/honey/inventory/customer/create", {
                method:"POST",
                body:form_data,
            }).then(res => res.json()).then(data=>{
                btn_submit.textContent = "Creado";
                location.reload();
            });
        }
    })
}
const updateCustomer = () =>{
    const modal_update = document.getElementById('modal-create-new-customer');
    const form_customer = document.getElementById("form-customer");
    const title_form = document.getElementById("title-form-message-mode");
    const btn_reset = document.getElementById("btn-submit-form-return-create");
    const btn_update = document.getElementById("btn-submit-form");
    const btn_edit_customer_all = document.querySelectorAll(".btn-edit-customer");
    let i = null;
    btn_reset.addEventListener("click", ()=>{
        closeModal(modal_update);
    })
    btn_edit_customer_all.forEach(btn =>{
        btn.addEventListener("click", async()=>{
            i = btn.dataset.i;
            if (i){
                await fetch("/honey/inventory/customer/read?i="+String(i)).then(res => res.json()).then(data =>{
                    if (data){
                        const resp = JsonToForm("form-customer", data);
                        if (resp === "ok"){
                            btn_update.textContent = "Actualizar";
                            form_customer.dataset.mode = "update";
                            title_form.textContent = "Actualizar datos del cliente";
                            form_customer.classList.add("form-update");
                            openModal(modal_update);
                        };
                    };
                });
            };
        });
    });
    form_customer.addEventListener("submit", async(e)=>{
        e.preventDefault();
        const form_data = new FormData(form_customer);
        form_data.append("i", i);
        if (form_customer.dataset.mode === "update"){
            btn_update.textContent = "Actualizando...";
            btn_update.disabled = true;
            await fetch("/honey/inventory/customer/update", {
                method:"POST",
                body:form_data,
            }).then(res => res.json()).then(data=>{
                btn_update.textContent = "Agregado";
                location.reload();
            });
        }
    })
};
const deleteCustomer = () =>{
    const modal_confirm = document.getElementById("modal-confirm-delete-customer");
    const btns_delete = document.querySelectorAll(".btn-delete-customer");
    const btn_cancel = document.getElementById("btn-cancel-delete");
    const btn_confirm = document.getElementById("btn-confirm-delete");
    let tr_selected = null;
    let i = null;
    btns_delete.forEach(btn =>{
        btn.addEventListener("click", ()=>{
            i = btn.dataset.i;
            tr_selected = btn.parentElement.parentElement.parentElement;
            openModal(modal_confirm);
        })
    });
    btn_cancel.addEventListener("click", ()=>{
        i = null;
        closeModal(modal_confirm);
    });
    btn_confirm.addEventListener("click", async()=>{
        btn_confirm.textContent = "Eliminando...";
        btn_cancel.disabled = true;
        await fetch("/honey/inventory/customer/delete?i="+String(i)).then(res => res.json()).then((data) =>{
            tr_selected.remove();
            closeModal(modal_confirm);
            btn_confirm.textContent = "Eliminar";
            console.log(data);
        });
    })
}