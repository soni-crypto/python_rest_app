class CrudControl {
    base_url =  "/honey/";
    timeCalcOrder(){
        const spans_min = document.querySelectorAll('.minutos-pasados');
        spans_min.forEach((span_min)=>{
            const fechaCreacion = new Date(span_min.textContent); // Automáticamente reconoce la zona horaria
            const ahora = new Date(); // Fecha actual en la zona horaria local
    
            // Calcular la diferencia en minutos
            const diferenciaMilisegundos = ahora - fechaCreacion;
            let minutosPasados = Math.floor(diferenciaMilisegundos / 60000);
            let segundos = Math.floor((diferenciaMilisegundos % 60000) / 1000);
            
            function actualizarTiempo() {
                segundos++;
                if (segundos === 60) {
                    segundos = 0;
                    minutosPasados++;
                }
    
                const tiempoFormateado = `${String(minutosPasados).padStart(2, '0')}:${String(segundos).padStart(2, '0')}`;
                span_min.textContent = tiempoFormateado + " minutos";
                if (span_min.getAttribute("style")){
                    span_min.removeAttribute("style");
                }
            }
            setInterval(actualizarTiempo, 1000);
        })
    }
    order_complet(){
        const btn_cofirm = document.getElementById("btn-lock-order");
        let identifier = null;
        let state_order_temp = 0;
        window.addEventListener("click", (e)=>{
            if (e.target.classList.contains("btn-lock-more-data")){
                state_order_temp = e.target.dataset.state;
                identifier = e.target.dataset.identifier;
                openModal(document.getElementById("confirm-modal"));
            }
        })
        
        btn_cofirm.addEventListener("click",async()=>{
            btn_cofirm.textContent = "Confirmando...";
            btn_cofirm.disabled = true;
            await fetch("/honey/update_order_state?row="+String(identifier)+"&state="+String(state_order_temp)).then(res => res.text()).then(data=>{
                console.log(parseInt(state_order_temp));
                if (parseInt(state_order_temp) === 21){
                    socket.emit("order_state_21", {"id":identifier}, (response)=>{
                        btn_cofirm.textContent = "Si, confirmo";
                        closeModal(document.getElementById("confirm-modal"));
                    });
                }else if (parseInt(state_order_temp) === 22){
                    socket.emit("order_state_22", {"id":identifier}, (response)=>{
                        btn_cofirm.textContent = "Si, confirmo";
                        closeModal(document.getElementById("confirm-modal"));
                    });
                }else if (parseInt(state_order_temp) === 3){
                    socket.emit("order_state_3", {"id":identifier}, (response)=>{
                        btn_cofirm.textContent = "Si, confirmo";
                        closeModal(document.getElementById("confirm-modal"));
                    });
                }else if (parseInt(state_order_temp) === 4){
                    socket.emit("order_state_4", {"id":identifier}, (response)=>{
                        btn_cofirm.textContent = "Si, confirmo";
                        closeModal(document.getElementById("confirm-modal"));
                    });
                }
                btn_cofirm.removeAttribute("disabled");
            })
        })
    }
    order_delete(){
        const btn_confirm = document.getElementById("btn-delete-order");
        let identifier = null;
        window.addEventListener("click", (e)=>{
            if (e.target.classList.contains("btn-del-more-data")){
                identifier = e.target.dataset.identifier;
                openModal(document.getElementById("delete-modal"));
            }
        });
        btn_confirm.addEventListener("click", async()=>{
            if (identifier){
                btn_confirm.textContent = "Rechazando...";
                btn_confirm.disabled = true;
                await fetch("/honey/order/delete?row="+String(identifier)).then(res => res.text()).then(data=>{
                    socket.emit("order_state_6", {"id":identifier}, (response)=>{
                        btn_confirm.textContent = "Rechazar";
                        btn_confirm.removeAttribute("disabled");
                        closeModal(document.getElementById("delete-modal"));
                    });
                });

            };           
        });
    }
    orderEdit(){
        const btns_all = document.querySelectorAll(".btn-edit-more-data");
        const type_food = document.getElementById("type_food");
        const name_food = document.getElementById("name_food");
        const extras_food = document.getElementById("extras_food");
        const quantity_food = document.getElementById("quantity_food");
        const table_number = document.getElementById("table_number");
        const class_food = document.getElementById("class_food");
        let identifier = null;
        
        type_food.addEventListener("change", async()=>{
            name_food.innerHTML="<option selected disabled value=''>Seleccione plato*</option>";
            const req_id = String(type_food.value);
            await fetch(`datafoodmain/${req_id}`).then(res=>res.json()).then(data=>{
                
                data.data.forEach((list_data)=>{
                    const optionTag = document.createElement("option");
                    optionTag.value=list_data[0];
                    optionTag.textContent=list_data[1];
                    name_food.insertAdjacentElement("beforeend", optionTag)
                })
                
            })
        })
        const insert_food = () =>{
            return new Promise((resolve, reject)=>{
                name_food.innerHTML="<option selected disabled value=''>Seleccione plato*</option>";
                const req_id = String(type_food.value);
                fetch(`datafoodmain/${req_id}`).then(res=>res.json()).then(data=>{    
                    
                    data.data.forEach((list_data)=>{
                        const optionTag = document.createElement("option");
                        optionTag.value=list_data["id"];
                        optionTag.textContent=list_data["name"];
                        name_food.insertAdjacentElement("beforeend", optionTag)
                        resolve();
                    })  
                })
            })
        }
        btns_all.forEach((btn) =>{
            btn.addEventListener("click", async()=>{
                identifier = btn.dataset.identifier;
                await fetch ("/honey/update?row="+String(identifier)).then(response => response.json()).then(data =>{
                    
                    type_food.value = data.type_food;
                    extras_food.value = data.extras_food;
                    quantity_food.value = data.quantity_food;
                    table_number.value = data.table_number;
                    class_food.value = data.class_food;
                    insert_food().then( ()=>{
                        
                        name_food.value = data.name;
                        this.openModal("edit-modal");
                    })
                    

                })
            })
        })
        const btn_confirm = document.getElementById("btn-edit-confirm");
        btn_confirm.addEventListener("click", async()=>{
            if(identifier){
                if (type_food.value.length > 0 && name_food.value.length > 0 && quantity_food.value.length > 0 && table_number.value.length > 0 && class_food.value.length > 0){
                    const form_data = new FormData();
                    form_data.append("id_row", identifier);
                    form_data.append("name", name_food.value);
                    form_data.append("type_food", type_food.value);
                    form_data.append("extras_food", extras_food.value);
                    form_data.append("quantity_food", quantity_food.value);
                    form_data.append("table_number", table_number.value);
                    form_data.append("class_food", class_food.value);

                    await fetch(this.base_url + "update",{
                        method : "POST",
                        body : form_data,
                    }).then(res => res.text()).then(data =>{
                        this.closeModal("edit-modal");
                        location.reload();
                    })
                };
            }
        })

    }
    order_update_food = () =>{
        const btns = document.querySelectorAll(".button-open-data-order-edit-in-order");
        const ctn_c = document.querySelector(".container-observations");
        const tag_image_food = document.getElementById("image-food-view-update");
        const tag_name_food = document.getElementById("name-food-view-update");
        const tag_quantity_food = document.getElementById("quantity-food-view-update");
        const tag_type_food = document.getElementById("type-food-view-update");
        const data = {}
        let identifier = null;
        btns.forEach(btn =>{
            btn.addEventListener("click", async()=>{
                data.id_data_order = btn.dataset.idDataOrder;
                await fetch("/honey/order/update/data_order", {
                    method : "post",
                    headers : {
                        "Content-Type": "application/json",
                    },
                    body : JSON.stringify(data),
                }).then(res => res.json()).then(data=>{
                    
                    if (data){
                        ctn_c.innerHTML = "";
                        const data_comm = data.data_comments;
                        const data_food = data.data_food;
                        const comm_order = data_food.observation.split("///").filter((e)=> e );
                        identifier = data_food.id;
                        tag_image_food.src = data_food.food_image;
                        tag_name_food.textContent = data_food.food_name;
                        tag_quantity_food.value = data_food.quantity;
                        if (data_food.type_order === 1){
                            tag_type_food.querySelectorAll("option")[0].setAttribute("selected", true);
                            tag_type_food.querySelectorAll("option")[1].removeAttribute("selected");
                        }else if (data_food.type_order === 2){
                            tag_type_food.querySelectorAll("option")[1].setAttribute("selected", true);
                            tag_type_food.querySelectorAll("option")[0].removeAttribute("selected");
                        }
                        data_comm.forEach(d =>{
                            if (comm_order.includes(d.comment_text)){
                                const html = `
                                            <label for="c${d.id}">
                                                <input type="checkbox" value="${d.comment_text}" name="comm_u" id="c${d.id}" checked class="checkbox-input-value-new-comment-order" required>
                                                <span>${d.comment_text}</span>
                                            </label>`
                                            ;
                                    ctn_c.insertAdjacentHTML("beforeend", html);
                            }else{
                                const html = `
                                            <label for="c${d.id}">
                                                <input type="checkbox" value="${d.comment_text}" name="comm_u" id="c${d.id}" class="checkbox-input-value-new-comment-order" required>
                                                <span>${d.comment_text}</span>
                                            </label>`
                                            ;
                                    ctn_c.insertAdjacentHTML("beforeend", html);
                            }
                        })
                        openModal(document.getElementById("modal-update-food-data-in-order"));
                    }else{
                        alert("Ocurrió un error");
                    }
                })
            })
        })
        const btn_submit = document.getElementById("button-update-data-order-main");
        btn_submit.addEventListener("click", async()=>{
            if (identifier){
                btn_submit.disabled = true;
                btn_submit.textContent = "Actualizando...";
                const checkbox_comm = Array.from(document.querySelectorAll("input[name='comm_u']")).filter((e) => e.checked).map(e => e.value).join("///");
                const form_data = new FormData();
                form_data.append("new_comment", checkbox_comm);
                form_data.append("new_quantity", tag_quantity_food.value);
                form_data.append("new_type", tag_type_food.value);
                form_data.append("id_data_order", identifier)
                await fetch("/honey/order/update/data_order/update", {
                    method : "post",
                    body: form_data,
                }).then(res => res.json()).then(data =>{
                    location.reload();
                })
            }
        })
    }
    order_update_table = () =>{
        const btns_table = document.querySelectorAll(".button-open-table-edit-in-order");
        const tables = document.getElementsByName("new-table-update-order");
        const btn_submit = document.getElementById("btn-submit-form-update-table");
        const data = {}
        btns_table.forEach(btn =>{
            btn.addEventListener("click", ()=>{
                data.order_id = btn.dataset.orderId;
                data.order_table = btn.dataset.orderTable;
                Array.from(tables).forEach(table =>{
                    if (table.dataset.numberTable === data.order_table){
                        table.setAttribute("checked", true);
                    }else{
                        table.removeAttribute("checked");
                    }
                })
                openModal(document.getElementById('modal-edit-table-order'));           
            })
        })
        tables.forEach(t =>{
            t.addEventListener("click", ()=>{
                data.id_table = t.value;
            })
        })
        btn_submit.addEventListener("click", async()=>{
            await fetch("/honey/order/update/table", {
                method : "post",
                headers : {
                    "Content-Type" : "application/json",
                },
                body : JSON.stringify(data),
            }).then(res => res.json()).then(data =>{
                if (data.state === "ok"){
                    location.reload();
                }else{
                    alert("Ocurrió un error");
                }
            })
        })
    }
}
