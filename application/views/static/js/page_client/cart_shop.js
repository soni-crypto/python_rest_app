const template = (con, id, name, quantity, price, money)=>{
    let t = '<tr>'+
            // '    <td>'+ con +'</td>'+
            '    <td class="text-nowrap">'+ name +'</td>'+
            '    <td>'+
            '        <div class="container-btn-control-quantity">'+
            '            <button class="button btn-subtract" data-id="'+ id +'" data-price="'+ price +'">-</button>'+
            '            <span class="span-quantity">'+ quantity +'</span>'+
            '            <button class="button btn-add" data-id="'+ id +'" data-price="'+ price +'">+</button>'+
            '        </div>'+
            '    </td>'+
            '    <td class="text-nowrap">'+ money +' '+ (price * quantity).toFixed(2) +'</td>'+
            '    <td><button class="button is-danger btn-delete" data-id="'+ id +'" data-price="'+ price +'">x</button></td>'+
            '</tr>';
    return t;
}

const span_total_amount = document.getElementById("span-total-amount-container");
const tbody_main_cart = document.getElementById("tbody-main-cart");
const jdapp = localStorage.getItem("jdapp");
const message = document.getElementById("input-note-message");

if (jdapp){
    let jdapp_temp = JSON.parse(jdapp);
    const icon_money = jdapp_temp.data.money;
    message.value = jdapp_temp.data.message;
    if (jdapp_temp.data.category === 1){
        document.getElementsByName("category")[0].checked = true;   
    }else if(jdapp_temp.data.category === 2){
        document.getElementsByName("category")[1].checked = true;
    }else if(jdapp_temp.data.category === 3){
        document.getElementsByName("category")[2].checked = true;
    }else{
        document.getElementsByName("category")[0].checked = true;
    }
    let con = 1;
    let price_total = 0;
    jdapp_temp.products.forEach(d=>{
        const resp = template(con, d.product, d.name, d.quantity, d.price, icon_money);
        tbody_main_cart.insertAdjacentHTML("beforeend", resp);
        con ++;
        price_total += d.price * d.quantity;
    })
    span_total_amount.textContent = price_total.toFixed(2);
    


    // controls storage
    const btn_delete = document.querySelectorAll(".btn-delete");
    const btn_subtract = document.querySelectorAll(".btn-subtract");
    const btn_add = document.querySelectorAll(".btn-add");
    btn_delete.forEach(btn =>{
        btn.addEventListener("click", ()=>{
            let i = 0;
            jdapp_temp.products.forEach(d=>{
                if (parseInt(d.product) === parseInt(btn.dataset.id)){
                    jdapp_temp.products.splice(i, 1);
                    btn.parentElement.parentElement.remove();
                    console.log(btn.parentElement.previousElementSibling);
                    span_total_amount.textContent = (parseFloat(span_total_amount.textContent) - (d.quantity * d.price)).toFixed(2);
                }
                i ++;
            });
            localStorage.setItem("jdapp", JSON.stringify(jdapp_temp));
        });
    });
    btn_subtract.forEach(btn =>{
        btn.addEventListener("click", ()=>{
            jdapp_temp.products.forEach(d=>{
                if (parseInt(d.product) === parseInt(btn.dataset.id)){
                    if (d.quantity > 1){
                        d.quantity -= 1;
                        btn.nextElementSibling.textContent = d.quantity;
                        span_total_amount.textContent = (parseFloat(span_total_amount.textContent) - parseFloat(btn.dataset.price)).toFixed(2);
                        btn.parentElement.parentElement.nextElementSibling.textContent = icon_money + " " + (d.quantity * d.price).toFixed(2);
                    }
                }
            });
            localStorage.setItem("jdapp", JSON.stringify(jdapp_temp));
        })
    })
    btn_add.forEach(btn =>{
        btn.addEventListener("click", ()=>{
            jdapp_temp.products.forEach(d=>{
                if (parseInt(d.product) === parseInt(btn.dataset.id)){
                    d.quantity += 1;
                    btn.previousElementSibling.textContent = d.quantity;
                    span_total_amount.textContent = (parseFloat(span_total_amount.textContent) + parseFloat(btn.dataset.price)).toFixed(2);
                    btn.parentElement.parentElement.nextElementSibling.textContent = icon_money + " " + (d.quantity * d.price).toFixed(2);
                }
            });
            localStorage.setItem("jdapp", JSON.stringify(jdapp_temp));
        })
    })
    const btn_save = document.getElementById("button_continue");
    btn_save.addEventListener("click", ()=>{
        const category = Array.from(document.getElementsByName("category")).filter(a => a.checked)[0].value;
        message.value;
        jdapp_temp.data.category = parseInt(category);
        jdapp_temp.data.message = message.value;
        localStorage.setItem("jdapp", JSON.stringify(jdapp_temp));
        if (category != 1){
            location.href = "calendar";
        }else{
            location.href = "table";
        }
    })
}
