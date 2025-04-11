


const quantity_show_in_cart = document.getElementById("quantity-number-p-in-in-cart");
const btn_append_to_cart = document.querySelectorAll(".btn-product-append-to-cart");
let jdapp_temp = {"products":[], "data" : {"money": document.getElementById("currency_config_main").textContent, "message" : "", "price_delivery" : parseFloat(document.getElementById("delv").value), "delivery_address":"" }};
const jdapp = localStorage.getItem("jdapp");
if (jdapp){
    jdapp_temp = JSON.parse(jdapp);
    let quantity_in_cart_temp = 0;
    jdapp_temp.products.forEach((b =>{
        quantity_in_cart_temp += 1;
        // btn.classList.remove("btn-primary");
        // btn.textContent = "Agregado";
        // btn.disabled = true;
    }));
    quantity_show_in_cart.textContent = quantity_in_cart_temp;
}else{
    
}
btn_append_to_cart.forEach(btn =>{
    jdapp_temp.products.forEach((b =>{
        if(parseInt(b.product) === parseInt(btn.dataset.id)){
            btn.classList.remove("btn-primary");
            btn.textContent = "Agregado";
            btn.disabled = true;
        }
    }));
    btn.addEventListener("click", ()=>{
        btn.classList.remove("btn-primary");
        btn.textContent = "Agregado";
        btn.disabled = true;
        quantity_show_in_cart.textContent = parseInt(quantity_show_in_cart.textContent) + 1;
        jdapp_temp.products.push({
            "product" : parseInt(btn.dataset.id),
            "name" : btn.dataset.name,
            "quantity" : 1,
            "price" : parseFloat(btn.dataset.price),
        })
        localStorage.setItem("jdapp", JSON.stringify(jdapp_temp));

    })
})