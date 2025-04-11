const create_new_product = ()=>{
    const btn_submit_new_product = document.getElementById("btn-submit-new-product");
    const form = document.getElementById("form-new-product");
    form.addEventListener("submit", async(e)=>{
        e.preventDefault();
        const form_data = new FormData(form);
        btn_submit_new_product.disabled = true;
        btn_submit_new_product.textContent = "Creando mesa...";
        await fetch("/honey/inventory/create", {
            method:"POST",
            body:form_data,
        }).then(res => res.json()).then(data =>{
            btn_submit_new_product.textContent = "Mesa creada";
            location.reload();
        });
    });
};
const update_product = ()=>{
    const btns_edit = document.querySelectorAll(".btn-edit-product");
    let id_product = null;
    btns_edit.forEach(btn =>{
        btn.addEventListener("click", async()=>{
            btn.disabled = true;
            await fetch("/honey/inventory/get?i="+String(btn.dataset.id)).then(res => res.json()).then(data=>{
                btn.removeAttribute("disabled");
                if (data){
                    id_product = btn.dataset.id;
                    JsonToForm("form-update-product", data);
                    openModal(document.getElementById("update-product"));
                };
            });
        });
    });
    const btn_submit_update_product = document.getElementById("btn-submit-update-product");
    btn_submit_update_product.addEventListener("click", async()=>{
        btn_submit_update_product.disabled = true;
        btn_submit_update_product.textContent = "Actualizando...";
        const form_data = new FormData(document.getElementById("form-update-product"));
        if (id_product){form_data.append("id_product", id_product);}
        await fetch("/honey/inventory/update", {
            method:"POST",
            body:form_data,
        }).then(res => res.json()).then(data =>{
            btn_submit_update_product.textContent = "Actualizado";
            location.reload();
        });
    })
}
const delete_product = ()=>{
    const btns_edit = document.querySelectorAll(".btn-delete-product");
    let id_delete = null;
    btns_edit.forEach(btn =>{
        btn.addEventListener("click", ()=>{
            id_delete = btn.dataset.id;
            openModal(document.getElementById("delete-product-modal"));
        });
    });
    const btn_delete = document.getElementById("btn-submit-delete-product");
    btn_delete.addEventListener("click", async()=>{
        btn_delete.disabled = true;
        btn_delete.textContent = "Eliminando...";
        await fetch("/honey/inventory/delete?i="+String(id_delete)).then(res => res.json()).then(data=>{
        btn_delete.textContent = "Eliminado";
            location.reload();
        });
    });
}

const createCategory = () =>{
    const btn = document.getElementById("btn-submit-create-category");
    const form_category = document.getElementById("form-create-category");
    btn.addEventListener("click", async()=>{
        btn.disabled = true;
        btn.textContent = "Enviando...";
        const form_data = new FormData(form_category);
        await fetch("/honey/inventory/category/create", {
            method : "POST",
            body: form_data,
        }).then(res => res.text()).then(data =>{
            btn.textContent = "Enviado";
            location.reload();
        })
    });
}
const updateCategory = () =>{
    const category_name_update = document.getElementById("category_name_update");
    const btns_open = document.querySelectorAll(".btns-update-category-product");
    let a_name = null;
    let i = null;
    btns_open.forEach((btn)=>{
        btn.addEventListener("click", ()=>{
            i = btn.dataset.identifier;
            a_name = btn.parentElement.previousElementSibling;
            category_name_update.value = a_name.textContent;
            openModal(document.getElementById("update-category-product"));
        });
    });
    const btn_submit = document.getElementById("btn-submit-update-category");
    btn_submit.addEventListener("click",async()=>{
        if (i){
            btn_submit.disabled = true;
            btn_submit.textContent = "Actualizando...";
            const form_data = new FormData();
            form_data.append("name", category_name_update.value);
            form_data.append("category_id", i);
            await fetch("/honey/inventory/category/update",{
                method:"POST",
                body: form_data,
            }).then(res => res.text()).then(data =>{
                a_name.textContent = category_name_update.value;
                closeModal(document.getElementById("update-category-product"));
                btn_submit.textContent = "Actualizar";
                btn_submit.removeAttribute("disabled");
            });
        };
    });
};
const deleteCategory = ()=>{
    const btns_delete = document.querySelectorAll(".btns-delete-category-product");
    let i = null;
    btns_delete.forEach(btn =>{
        btn.addEventListener("click", ()=>{
            i = btn.dataset.identifier;
            openModal(document.getElementById("delete-category-product-modal"));
        });
    });
    const btn_submit = document.getElementById("btn-submit-delete-category-product");
    btn_submit.addEventListener("click", async()=>{
        if (i){
            btn_submit.disabled = true;
            btn_submit.textContent = "Eliminando...";
            await fetch("/honey/inventory/category/delete?i="+String(i)).then(res => res.text()).then(data =>{
                btn_submit.textContent = "Eliminado";
                location.href="/honey/inventory";
            });
        }
    })
};
const sellProductPrepared = () =>{
    // const btn_buy = document.getElementById("btn-buy-product");
    // const btn_transfer = document.getElementById("btn-transfer-product");
    const btn_sell = document.getElementById("btn-sell-product");
    const blocks_product = document.querySelectorAll(".block-row-product");
    let p = null;
    let i = null;
    blocks_product.forEach(product =>{
        product.addEventListener("click", async()=>{
            // btn_buy.innerHTML = '<div class="loader"></div>';
            // btn_transfer.innerHTML = '<div class="loader"></div>';
            btn_sell.innerHTML = '<div class="loader"></div>';
            i = product.dataset.i;
            await fetch("/honey/inventory/get?i="+String(i)).then(res => res.json()).then(data =>{
                if (data){
                    p = data.sale_price;
                    const resj = JsonToForm("container-details-product", data, "class")
                    if (resj){
                        btn_sell.removeAttribute("disabled");
                        btn_sell.classList.add("btn-active-modal");
                        btn_sell.innerText = "Vender";
                        // btn_buy.removeAttribute("disabled");
                        // btn_buy.classList.add("btn-active-modal");
                        // btn_buy.innerText = "Comprar";
                        // btn_transfer.removeAttribute("disabled");
                        // btn_transfer.classList.add("btn-active-modal");
                        // btn_transfer.innerText = "Transferir";
                    }
                }
            })
        })
    })
    const quantity_sell = document.getElementById("quantity_sell");
    const price_total_sell_render = document.getElementById("price_total_sell_render");
    quantity_sell.addEventListener("input", ()=>{
        if (quantity_sell.value){
            price_total_sell_render.value = parseFloat(quantity_sell.value) * parseFloat(p);
        }
    })
    const discount_sell_appli = document.getElementById("discount_sell_appli");
    discount_sell_appli.addEventListener("input", ()=>{
        if (discount_sell_appli.value){
            let price_act = parseFloat(quantity_sell.value) * parseFloat(p)
            let porcnt = parseFloat(discount_sell_appli.value)/100;
            let val_2 = parseFloat(price_act) - (parseFloat(price_act) * porcnt);
            price_total_sell_render.value = val_2.toFixed(2);
        }else{
            price_total_sell_render.value = (parseFloat(quantity_sell.value) * parseFloat(p)).toFixed(2);
        }
    })
    const btn_confirm_sell_product = document.getElementById("btn-confirm-sell-product");
    const form_sell = document.getElementById("id-form-create-sell-data")
    form_sell.addEventListener("submit", async(e)=>{
        e.preventDefault();
        btn_confirm_sell_product.textContent = "Confirmando...";
        btn_confirm_sell_product.disabled = true;
        if (i){
            const form_data = new FormData(form_sell);
            form_data.append("id_product", i);
            await fetch("/honey/inventory/sales/create", {
                method:"POST",
                body: form_data,
            }).then(res => res.json()).then(data =>{
                location.reload();
            });
        }
    });
}