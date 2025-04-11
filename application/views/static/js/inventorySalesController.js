const salesUpdate = () =>{
    const btn_update_sales = document.querySelectorAll(".btn-update-sales");
    const message_update_sales = document.querySelector(".message-update-sales");
    let i = null;
    let s = null;
    btn_update_sales.forEach(btn =>{
        btn.addEventListener("click", ()=>{
            i = btn.dataset.i;
            s = btn.dataset.s;
            if (s === "2"){
                message_update_sales.textContent = "Monto cobrado";
            }else if (s === "3"){
                message_update_sales.textContent = "Monto abonado";
            }else{
                message_update_sales.textContent = "ERROR";
            }
            openModal(document.getElementById("modal-update-sale"))
        })
    })
    const btn_conclude_update_sale = document.getElementById("btn-conclude-update-sale");
    const new_amount_update = document.getElementById("new-amount-update");
    btn_conclude_update_sale.addEventListener("click", async()=>{
        btn_conclude_update_sale.textContent = "Confirmando...";
        btn_conclude_update_sale.disabled = true;
        const form_data = new FormData();
        form_data.append("amount_update", new_amount_update.value);
        form_data.append("id", i);
        await fetch("/honey/inventory/sales/update", {
            method : "POST",
            body : form_data,
        }).then(res => res.json()).then(data =>{
            console.log(data)
            location.reload();
        })
    })
}
const salesDelete = () =>{
    const btn_delete_sales = document.querySelectorAll(".btn-delete-sales");
    let i = null;
    btn_delete_sales.forEach((btn)=>{
        btn.addEventListener("click", ()=>{
            i = btn.dataset.i;
            openModal(document.getElementById("modal-delete-sale"));
        })
    })
    const btn_confirm = document.getElementById("btn-confirm-delete-sale");
    btn_confirm.addEventListener("click", async()=>{
        btn_confirm.textContent = "Eliminando...";
        btn_confirm.disabled = true;
        await fetch("/honey/inventory/sales/delete?i="+String(i)).then(res => res.json()).then(data =>{
            btn_confirm.textContent = "Eliminado";
            location.reload();
        });
    });
}