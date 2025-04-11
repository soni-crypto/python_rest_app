const concludeOrder = () =>{
    const btn_conclude_order = document.querySelectorAll(".btn-conclude-order");
    btn_conclude_order.forEach(btn =>{
        btn.addEventListener("click", async()=>{
            btn.textContent = "Concluyendo...";
            btn.disabled = true;
            let id = btn.dataset.identifier;
            let state = btn.dataset.state;
            await fetch("/honey/update_order_state?row="+String(id)+"&state="+String(state)).then(res => res.text()).then(data=>{
                btn.textContent = "Concluído";
                location.reload();
            });
        })
    });
}
const releaseOrder = () =>{
    const btn_release_table = document.getElementById("btn-release-table");
    if (btn_release_table){
        btn_release_table.addEventListener("click", async()=>{
            btn_release_table.textContent = "Eliminando...";
            btn_release_table.disabled = true;
            const form_data = new FormData();
            form_data.append("state_update", 1);
            form_data.append("id_table_update", btn_release_table.dataset.identifier);
            await fetch("/honey/table/update", {
                method:"POST",
                body: form_data,
            }).then(res => res.json()).then(data =>{
                btn_release_table.textContent = "Eliminado";
                // location.href = "/honey/table";
                location.reload();
            })
        })
    }
}
const concludeOrderAll = () =>{
    const btn = document.getElementById("btn-conclude-all-orders");
    btn.addEventListener("click", async()=>{
        btn.textContent = "Concluyendo...";
        btn.disabled = true;
        const id = btn.dataset.identifierTable;
        const u = btn.dataset.u != "None" ? btn.dataset.u : "";
        const l = btn.dataset.l != "None" ? btn.dataset.l : "";
        await fetch("/honey/update_order_state/complet_by_table?row="+String(id)+"&u="+String(u)+"&l="+String(l)).then(res => res.text()).then(data=>{
            btn.textContent = "Concluído";
            location.href = "/honey/table/details?table="+String(id);
        });
    })

}

const concludeOrderWithPayments = () => {
    const form = document.getElementById("form-concluded-order-main");
    const modal = document.getElementById("modal-process-info-conclud-order-main");
    const btns_open_modal = document.querySelectorAll(".btn-process-order-with-payment");
    const btn_conclude_order_main = document.getElementById("btn-conclude-order-main");
    const pay_method_input_cal = document.querySelectorAll(".pay-method-input-cal");
    let mode = null;
    let identifier = null;
    let state = null;
    let table_id = null;
    let user = null;
    let user_level = null;
    let amount_main = true;
    
    
    btns_open_modal.forEach((btn) => {
        btn.addEventListener("click", ()=>{
            form.querySelectorAll("input[type=hidden]").forEach(p =>{
                p.remove();
            })
            amountAllOrders = btn.dataset.amountAllOrders;
            mode = btn.dataset.mode;
            identifier = btn.dataset.identifier;
            state = btn.dataset.state;
            table_id = btn.dataset.table;
            user = btn.dataset.u;
            user_level = btn.dataset.l;
            const get_names = ["mode", "identifier", "state", "table_id", "user", "user_level"];
            const get_values = [mode, identifier, state, table_id, user, user_level];
            for (let i = 0; i <= 5; i++ ){
                const input = document.createElement("input");
                input.type = "hidden";
                input.name = get_names[i];
                input.value = get_values[i];
                form.insertAdjacentElement("beforeend", input);
            };
            amount_main = parseFloat(amountAllOrders);
            document.getElementById("amount-to-view").textContent = amountAllOrders;
            openModal(modal); 
        });
    });
    btn_conclude_order_main.addEventListener("click", async()=>{
        let sum_value_inputs = 0;
        Array.from(pay_method_input_cal).forEach(e=>{
            const value = e.value;
            if (value){
                sum_value_inputs += parseFloat(value);
            }
        })
        console.log(amount_main, sum_value_inputs);
        if (amount_main === sum_value_inputs){
            const form_data = new FormData(form);
            await fetch("/honey/order/process_order_concluded", {
                method : "post",
                body: form_data,
            }).then(res => res.json()).then((data) =>{
                if (data){
                    const r = new Promise(async(resolve, reject) =>{
                        if (parseInt(data.mode) === 1){
                            let id = data.identifier;
                            let state = data.state;
                            await fetch("/honey/update_order_state?row="+String(id)+"&state="+String(state)).then(res => res.text()).then(data=>{
                                resolve("ok");
                            });
                        }else if (parseInt(data.mode) === 2){
                            const id = data.table_id;
                            const u = data.user;
                            const l = data.user_level;
                            await fetch("/honey/update_order_state/complet_by_table?row="+String(id)+"&u="+String(u)+"&l="+String(l)).then(res => res.text()).then(data=>{
                                resolve("ok");
                            });
                        }else{
                            alert("Ocurrió un error");
                        }
                    })
                    r.then(response =>{
                        closeModal(modal);
                        location.reload();
                    })
                }else{
                    alert("Ocurrió un error");
                }

            });
        }else{
            if (amount_main > sum_value_inputs){
                alert("El monto cobrado es inferior al monto por cobrar")
            }else if (amount_main < sum_value_inputs){
                alert("El monto cobrado es superior al monto por cobrar")
            }else{
                alert("Ocurrió")
            }
        }
    });
    
};

const autocompletClientByEmail = () =>{
    const input = document.getElementById("input-email-search-client");
    input.addEventListener("input", async()=>{
        await fetch("/honey/freeuser/read?email="+input.value).then(res => res.json()).then(data =>{
            JsonToForm("form-concluded-order-main", data);
        })
    });
}