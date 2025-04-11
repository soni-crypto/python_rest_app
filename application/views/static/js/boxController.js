const message_order_or_reservation = document.getElementById("message-order-or-reservation");
const btns_open_modal_box = document.querySelectorAll(".btn-open-modal-update-box-app");
const modal_input_saldo_general = document.getElementById("modal_input_saldo_general");
const modal_input_cantidad_general = document.getElementById("modal_input_cantidad_general");
const modal_input_saldo_diario = document.getElementById("modal_input_saldo_diario");
const modal_input_cantidad_diario = document.getElementById("modal_input_cantidad_diario");
// const close_box_btn = document.getElementById("modal-btn-close-box-main");
const upgrade_box_btn = document.getElementById("modal-btn-upgrade-box-main");
let category_data_box = 0;
btns_open_modal_box.forEach((btn) =>{
    btn.addEventListener("click", async()=>{
        await fetch("/honey/box/encrypted/get").then(res => res.json()).then(data =>{
            if (data){
                category_data_box = btn.dataset.type;
                if (btn.dataset.type === "1"){
                    message_order_or_reservation.textContent = "Ordenes";
                    modal_input_saldo_general.value = data.total_amount_order;
                    modal_input_saldo_diario.value = data.daily_amount_order;
                    modal_input_cantidad_general.value = data.total_quantity_order;
                    modal_input_cantidad_diario.value = data.daily_quantity_order;
                }else if(btn.dataset.type === "2"){
                    message_order_or_reservation.textContent = "Reservas";
                    modal_input_saldo_general.value = data.total_amount_reservation;
                    modal_input_saldo_diario.value = data.daily_amount_reservation;
                    modal_input_cantidad_general.value = data.total_quantity_reservation;
                    modal_input_cantidad_diario.value = data.daily_quantity_reservation;
                }
                openModal(document.getElementById("modal-config-all-main-box-app"));
            }
        })
    })
})
// close_box_btn.addEventListener("click", async()=>{
//     close_box_btn.disabled = true;
//     close_box_btn.querySelector("span").textContent = "Cerrando...";
//     await fetch("/honey/box/encrypted/close?category="+String(category_data_box)).then(res => res.text()).then(data => {
//         if (data === "ok"){
//             location.reload(); 
//         }else{
//             close_box_btn.querySelector("span").textContent = "Ocurrió un error";
//         }
//     })
// })
upgrade_box_btn.addEventListener("click", async()=>{
    upgrade_box_btn.disabled = true;
    upgrade_box_btn.textContent = "Guardando...";
    const form_data = new FormData();
    form_data.append("category", category_data_box);
    form_data.append("total_amount", modal_input_saldo_general.value);
    form_data.append("daily_amount", modal_input_saldo_diario.value);
    form_data.append("total_quantity", modal_input_cantidad_general.value);
    form_data.append("daily_quantity", modal_input_cantidad_diario.value);
    await fetch("/honey/box/encrypted/upgrade", {
        method:"POST",
        body: form_data,
    }).then(res => res.text()).then(data => {
        if (data === "ok"){
            location.reload(); 
        }else{
            upgrade_box_btn.textContent = "Ocurrió un error";
        }
    })
})