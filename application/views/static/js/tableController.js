const create_new_table = ()=>{
    const btn_submit_new_table = document.getElementById("btn-submit-new-table");
    const form_main = document.getElementById("form-new-table");
    btn_submit_new_table.addEventListener("click", async()=>{
        if (document.getElementById("category_id").value && document.getElementById("number_table").value && document.getElementById("limit_number_of_users").value){
            const form_data = new FormData(form_main);
            btn_submit_new_table.disabled = true;
            btn_submit_new_table.textContent = "Creando mesa...";
            await fetch("/honey/table/create", {
                method:"POST",
                body:form_data,
            }).then(res => res.json()).then(data =>{
                btn_submit_new_table.textContent = "Mesa creada";
                btn_submit_new_table.removeAttribute("disabled");
                const ts = form_main.querySelectorAll("input, select");
                ts.forEach(t =>{
                    if (t.tagName === "SELECT"){
                        const os = t.querySelectorAll("option");
                        os.forEach(o =>{
                            o.removeAttribute("selected");
                        })
                        os[0].setAttribute("selected", true);
                    }else{
                        t.value = "";
                    }
                })
                closeModal(document.getElementById("create-new-table"));
                // location.reload();
            });
        }
    });
}
const update_table = ()=>{
    const btns_edit = document.querySelectorAll(".btn-edit-table");
    const number_table = document.getElementById("number_table_update");
    const limit_number_of_users_update = document.getElementById("limit_number_of_users_update");
    const state_update = document.getElementById("state_update");
    const category_id_update = document.getElementById("category_id_update");
    btns_edit.forEach(btn =>{
        btn.addEventListener("click", async()=>{
            btn.disabled = true;
            await fetch("/honey/table/read?id_table="+String(btn.dataset.id)).then(res => res.json()).then(data=>{
                btn.removeAttribute("disabled");
                if (data){
                    number_table.value = data[0].number_table;
                    limit_number_of_users_update.value = data[0].limit_number_of_users;
                    let options = state_update.querySelectorAll("option");
                    options.forEach(o =>{
                        if (parseInt(o.value) === parseInt(data[0].state)){o.selected = true;}
                        else{o.removeAttribute("selected");}
                    });
                    let options_2 = category_id_update.querySelectorAll("option");
                    options_2.forEach(o =>{
                        console.log(parseInt(o.value) , parseInt(data[0].category_id))
                        if (parseInt(o.value) === parseInt(data[0].category_id)){o.selected = true;}
                        else{o.removeAttribute("selected");}
                    })

                    document.getElementById("id_table_update").value = btn.dataset.id;
                    openModal(document.getElementById("update-table"));
                }
            })
        })
    })
    const btn_submit_update_table = document.getElementById("btn-submit-update-table");
    btn_submit_update_table.addEventListener("click", async()=>{
        btn_submit_update_table.disabled = true;
        btn_submit_update_table.textContent = "Actualizando...";
        const form_data = new FormData(document.getElementById("form-update-table"));
        await fetch("/honey/table/update", {
            method:"POST",
            body:form_data,
        }).then(res => res.json()).then(data =>{
            btn_submit_update_table.textContent = "Actualizado";
            location.reload();
        });
    })
}
const delete_table = ()=>{
    const btns_edit = document.querySelectorAll(".btn-delete-table");
    let id_delete = null;
    btns_edit.forEach(btn =>{
        btn.addEventListener("click", ()=>{
            id_delete = btn.dataset.id;
            openModal(document.getElementById("delete-table-modal"));
        });
    });
    const btn_delete = document.getElementById("btn-submit-delete-table");
    btn_delete.addEventListener("click", async()=>{
        btn_delete.disabled = true;
        btn_delete.textContent = "Eliminando...";
        await fetch("/honey/table/delete?id="+String(id_delete)).then(res => res.json()).then(data=>{
        btn_delete.textContent = "Eliminado";
            location.reload();
        });
    });
}

const createCategory = () =>{
    const btn = document.getElementById("btn-submit-create-category");
    const category_name = document.getElementById("category_name");
    btn.addEventListener("click", async()=>{
        btn.disabled = true;
        btn.textContent = "Enviando...";
        const form_data = new FormData();
        form_data.append("name", category_name.value);
        await fetch("/honey/table/category/create", {
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
    const btns_open = document.querySelectorAll(".btns-update-category-table");
    let a_name = null;
    let i = null;
    btns_open.forEach((btn)=>{
        btn.addEventListener("click", ()=>{
            i = btn.dataset.identifier;
            a_name = btn.parentElement.previousElementSibling;
            category_name_update.value = a_name.textContent;
            openModal(document.getElementById("update-category-table"));
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
            await fetch("/honey/table/category/update",{
                method:"POST",
                body: form_data,
            }).then(res => res.text()).then(data =>{
                a_name.textContent = category_name_update.value;
                closeModal(document.getElementById("update-category-table"));
                btn_submit.textContent = "Actualizar";
                btn_submit.removeAttribute("disabled");
            });
        };
    });
};
const deleteCategory = ()=>{
    const btns_delete = document.querySelectorAll(".btns-delete-category-table");
    let i = null;
    btns_delete.forEach(btn =>{
        btn.addEventListener("click", ()=>{
            i = btn.dataset.identifier;
            openModal(document.getElementById("delete-category-table-modal"));
        });
    });
    const btn_submit = document.getElementById("btn-submit-delete-category-table");
    btn_submit.addEventListener("click", async()=>{
        if (i){
            btn_submit.disabled = true;
            btn_submit.textContent = "Eliminando...";
            await fetch("/honey/table/category/delete?i="+String(i)).then(res => res.text()).then(data =>{
                btn_submit.textContent = "Eliminado";
                location.href="/honey/table";
            });
        }
    })
};