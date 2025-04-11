const state_reservation = () =>{
    const btns_change_state = document.querySelectorAll(".button-change-state-all");    
    btns_change_state.forEach((btn) => {
        btn.addEventListener("click", async() =>{
            btn.textContent = "Espere...";
            const container_btns = btn.parentElement;
            let data_btn = btn.dataset.identifier;
            data_btn = data_btn.split("-");
            const formData = new FormData();
            formData.append("id_reservation", data_btn[0]);
            formData.append("id_admin", data_btn[1]);
            formData.append("state", data_btn[2]);
            await fetch("/honey/update_state_reservations", {
                method:"POST",
                body: formData,
            }).then(res => res.text()).then(data => {
                if (data === "ok"){
                    const div_ctn = document.createElement("div");
                    div_ctn.classList.add("container-button-accepted-state");
                    const span_message = document.createElement("span");
                    span_message.classList.add("message-state-reservation","message-state-reservation__accepted");
                    if (data_btn[2] === "1"){
                        const button_open_modal = document.createElement("button");
                        button_open_modal.classList.add("button-modal-reservation-concluded");
                        button_open_modal.dataset.identifier = data_btn[0];
                        button_open_modal.textContent = "Terminar";
                        span_message.textContent = "Aceptado";
                        div_ctn.appendChild(button_open_modal);
                    }else if (data_btn[2] === "2"){
                        span_message.textContent = "Rechazado";
                    }
                    div_ctn.appendChild(span_message);
                    container_btns.innerHTML="";
                    container_btns.insertAdjacentElement("beforeend", div_ctn);            
                }
                
            });
        })   
    })
}
const voucher_preview = () => {
    const divs = document.querySelectorAll(".container-image-voucher");
    const model_voucher = document.querySelector(".image-voucher-zoom-in-modal");
    divs.forEach(element => {
        element.addEventListener("click", () => {
            model_voucher.src = element.querySelector("img").src;
            openModal(document.getElementById("modal_view_voucher"));
        })
    });
}

const filter_reservations = () =>{
    const select_ = document.getElementById("select-filter-state-reservations");
    const block_reservations = document.querySelectorAll(".block-reservation-main");
    select_.addEventListener("change", () =>{
        let value_state = select_.value;
        block_reservations.forEach((block) => {
            let state_block = block.dataset.stateReservation;
            if (value_state === "todos"){
                block.style.display = "block";
            }else if (String(state_block) === String(value_state)){
                block.style.display = "block";
            }else{
                block.style.display = "none";
            }
        })
    })
}

const window_event = () =>{
    document.addEventListener("click", (elem)=>{
        if (elem.target.classList.contains("button-modal-reservation-concluded")){
            const root_container = elem.target.closest(".block-reservation-main")
            const id_reservation = elem.target.dataset.identifier;
            openModal(document.getElementById("modal-reservation-concluded"));
            const button_to_conclude_reservation = document.getElementById("button-to-conclude-reservation");
            button_to_conclude_reservation.addEventListener("click", ()=>{
                
                const methods_pay = document.getElementsByName("type_of_customer_behavior");
                let method_pay_selected = Array.from(methods_pay).filter((method) => method.checked);
                if (method_pay_selected.length >= 1){
                    method_pay_selected[0].value
                    const form_data = new FormData();
                    form_data.append("state", 3);
                    form_data.append("id_reservation", id_reservation);
                    button_to_conclude_reservation.textContent="Procesando...";
                    fetch("/honey/update_state_reservations", {
                        method : "POST",
                        body : form_data,
                    }).then(response => response.text()).then(data =>{
                        methods_pay.forEach(m =>{
                            m.checked = false;
                        })
                        root_container.remove();
                        button_to_conclude_reservation.textContent="Concluir";
                        closeModal(document.getElementById("modal-reservation-concluded"));
                    })
                }

            })
        }
        
    })
}