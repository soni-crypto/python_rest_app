
let cmpny_ltlg= document.getElementById("location_coord_restaurant").value;

const update_cost = ()=>{
    const tds_price_product = document.querySelectorAll(".span_price_product");
    const span_total_cost = document.getElementById("container-span-total-cost");
    let total_price = 0;
    tds_price_product.forEach(td_price => {
        let price_array = td_price.textContent.split(" ");
        total_price = parseFloat(total_price) + parseFloat(price_array[1]);
    })
    total_price = String(total_price.toFixed(2));
    span_total_cost.textContent = total_price;
}
const update_cost_delivery = (price_)=>{
    const tds_price_product = document.querySelectorAll(".span_price_product");
    const span_total_cost = document.getElementById("amount-all-delivery-with-food");
    let total_price = 0;
    tds_price_product.forEach(td_price => {
        let price_array = td_price.textContent.split(" ");
        total_price = parseFloat(total_price) + parseFloat(price_array[1]);
    })
    total_price = total_price + parseFloat(price_);
    total_price = String(total_price.toFixed(2));
    span_total_cost.textContent = total_price;
    
}
const preview_image = (id_input, id_img) => {
    const image_target = document.getElementById(id_img);
    const input_file = document.getElementById(id_input);
    input_file.addEventListener("change", () =>{
        const archivo = input_file.files[0];
        if (archivo){
            const lector = new FileReader();
            lector.onload = function (e){
                image_target.src = e.target.result;
            }
            lector.readAsDataURL(archivo);
        }   
    })

}
const save_reservation = () => {
    const modal_message = document.getElementById("modal-message-pay");
    const btn_close_modal = document.getElementById("btn-close-modal-message");

    const btn_submit = document.getElementById("button_submit_reservation");
    const date_reservation = document.getElementById("date_reservation");
    const time_reservation = document.getElementById("time_reservation");
    const type_reservation = Array.from(document.getElementsByName("reservation-type"));
    const message_reservation = document.getElementById("message_reservation");
    const voucher_reservation = document.getElementById("voucher_reservation");

    const request1_reservation = document.getElementById("request1_reservation");
    const request2_reservation = document.getElementById("request2_reservation");
    
    const my_location_coordinate = document.getElementsByName("my_location_coordinate");
    const price_per_delivery = document.getElementById("price_per_delivery");
    preview_image("voucher_reservation","preview-image-changed-voucher");

    btn_submit.addEventListener("click", async() =>{
        const new_type_reservation = type_reservation.filter(type => type.checked);
        
        if (request1_reservation.checked && request2_reservation.checked){
            if (date_reservation.value.length > 0 && time_reservation.value.length > 0 && voucher_reservation.files.length > 0 && new_type_reservation.length > 0){
                document.getElementById("container-main-loader-proccess-order").style.display="flex";
                const form_data = new FormData();
                form_data.append("date_reservation", date_reservation.value);
                form_data.append("time_reservation", time_reservation.value);
                form_data.append("type_reservation", new_type_reservation[0].value);
                form_data.append("message_reservation", message_reservation.value);
                form_data.append("voucher_reservation", voucher_reservation.files[0]);
                form_data.append("my_location_coordinate", my_location_coordinate[0].value);
                form_data.append("price_per_delivery", price_per_delivery.value || 0.0);
                form_data.append("products", localStorage.getItem("products"));
                await fetch("/pages/pay/save_reservation", {
                    method:"POST", 
                    body:form_data,
                }).then(res => res.text()).then(data =>{
                    localStorage.removeItem("products");
                    document.getElementById("container-main-loader-proccess-order").style.display="none";
                    location.href = "/userapp/reservations";
                })
            }else{
                document.getElementById("message-policy-and-terms").style.display="none";
                document.getElementById("message-required-fields").style.display="flex";
                modal_message.classList.add("is-active");    
            }
        }else{
            document.getElementById("message-required-fields").style.display="none";
            document.getElementById("message-policy-and-terms").style.display="flex";
            modal_message.classList.add("is-active");
        }
    })

    // Close modal
    btn_close_modal.addEventListener("click", ()=>{
        modal_message.classList.remove("is-active");
    })
}
const order_now = ()=>{
    const inputs_type_order_decorate = document.getElementsByName("type_order");
    inputs_type_order_decorate.forEach(i=>{
        i.addEventListener("click", ()=>{
            inputs_type_order_decorate.forEach(is =>{
                if (is.value === i.value){
                    is.parentElement.classList.add("selected");
                }else{
                    is.parentElement.classList.remove("selected");
                }
            })
        })
    })
    const number_table = document.getElementsByName("number-table");
    number_table.forEach((n)=>{
        n.addEventListener("click", ()=>{
            number_table.forEach((nw)=>{nw.nextElementSibling.classList.remove("selected")});
            const sel = Array.from(number_table).find((nt)=> nt.checked);
            const inp = document.getElementById(sel.id);
            inp.nextElementSibling.classList.add("selected");
        })
    });
    const continue_order_now = document.getElementById("continue-order-now");
    if (continue_order_now){
        continue_order_now.addEventListener("click", async()=>{
            openModal(document.getElementById("container-modal-type-order"));
        });
    }
    const continue_show_tables = document.getElementById("btn-continue-order-type");
    continue_show_tables.addEventListener("click", ()=>{
        const inputs = document.getElementsByName("type_order");
        const input_type_order =  Array.from(inputs).find((i)=>i.checked);
        if (input_type_order){
            closeModal(document.getElementById("container-modal-type-order"));
            openModal(document.getElementById("container-modal-table-number"));
        }else{
            openModalMessageLittle("No ha seleccionado el tipo de orden", true);
        }
    });
    const return_to_modal_type_order = document.getElementById("return-to-modal-type-order");
    return_to_modal_type_order.addEventListener("click", ()=>{
        openModal(document.getElementById("container-modal-type-order"));
        closeModal(document.getElementById("container-modal-table-number"));
    });
    const send_data_order_now = document.getElementById("send-data-order-now");
    send_data_order_now.addEventListener("click", async()=>{
        const validate_input = Array.from(number_table).find((nt)=> nt.checked);
        const input_type_order =  Array.from(inputs_type_order_decorate).find((i)=>i.checked);
        if (validate_input){
            const data_json = JSON.parse(localStorage.getItem("products")); 
            closeModal(document.getElementById("container-modal-table-number"));
            document.getElementById("container-main-loader-proccess-order").style.display="flex";
            await fetch("/userapp/order/save_order", {
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                },
                body:JSON.stringify({"id_table":validate_input.value,"type_order":input_type_order.value,  "data":data_json}),
            }).then(res => res.text()).then(data=>{
                socket.emit("order_state_1", {"id":data}, (response)=>{
                    localStorage.removeItem("products");
                    location.href = "/userapp/orders";
                });
            }).catch((err)=>{
                console.log(err);
                document.getElementById("container-main-loader-proccess-order").style.display="none";
                openModalMessageLittle("Ocurrió un error al enviar su orden", true);
            })
        }else{
            openModalMessageLittle("Seleccione el número de mesa.", true);
        }
    })
}
window.addEventListener("click", (element)=>{
    let a = element.target;
    let class_name = a.getAttribute("class");
    let identifier = a.dataset.identifier;
    const products = JSON.parse(localStorage.getItem("products"));
    if (class_name === "btn-cantity-minus"){
        products.forEach((product)=>{
            if (parseInt(product.identifier) === parseInt(identifier)){
                if (parseInt(product.cantity) > 1){
                    product.cantity = parseInt(product.cantity) - 1;
                    const span_element = a.nextElementSibling;
                    span_element.textContent = product.cantity;

                    let td_price = a.parentElement.parentElement.previousElementSibling.querySelector(".span_price_product");
                    let price_array = td_price.textContent.split(" ");
                    td_price.textContent = price_array[0] + " " + String((parseFloat(price_array[1]) - parseFloat(product.price_unique)).toFixed(2));
                    
                }
            }
        })
        localStorage.setItem("products", JSON.stringify(products));
        update_cost();

    }else if (class_name === "btn-cantity-more"){
        products.forEach((product)=>{
            if (parseInt(product.identifier) === parseInt(identifier)){
                if (parseInt(product.cantity) >= 0){
                    product.cantity = parseInt(product.cantity) + 1;
                    const span_element = a.previousElementSibling;
                    span_element.textContent = product.cantity;

                    let td_price = a.parentElement.parentElement.previousElementSibling.querySelector(".span_price_product");
                    let price_array = td_price.textContent.split(" ");
                    td_price.textContent = price_array[0] + " " + String((parseFloat(price_array[1]) + parseFloat(product.price_unique)).toFixed(2));
                    
                }
            }
        })
        localStorage.setItem("products", JSON.stringify(products));
        update_cost();

    }else if (class_name === "delete-product"){
        let container_row = a.parentElement.parentElement;
        let identifier_delete = identifier;
        if (!container_row.classList.contains("container-row-main-product")){
            container_row = container_row.parentElement;
        };
        if (!container_row.classList.contains("container-row-main-product")){
            container_row = container_row.parentElement;
        };
        identifier_delete = container_row.querySelector("button.delete-product").dataset.identifier;
        const products = JSON.parse(localStorage.getItem("products"));
        if (products){
            products.forEach((product, index) =>{
                if (parseInt(product.identifier) === parseInt(identifier_delete)){
                    products.splice(index, 1);
                }
            })
            localStorage.setItem("products", JSON.stringify(products));
            container_row.remove();
        }
        update_cost();
    }
})

const config_steep_page_view =() =>{
    // const template_1 = document.querySelector(".container-mask-methods-pay");
    const template_2 = document.querySelector(".container-mask-form");
    const continue_btn_1 = document.getElementById("continue-btn-1");
    // const continue_btn_2 = document.getElementById("continue-btn-2");
    // const back_btn_1 = document.getElementById("back-btn-1");
    const back_btn_2 = document.getElementById("back-btn-2");
    continue_btn_1.addEventListener("click", ()=>{
        // template_1.style.zIndex = "-5";
        template_2.style.zIndex = "5";
    });
    // continue_btn_2.addEventListener("click", ()=>{
        // template_1.style.zIndex = "-5"; 
        // template_2.style.zIndex = "5";
    // });
    // back_btn_1.addEventListener("click", ()=>{
    //     // template_1.style.zIndex = "-5";
    //     template_2.style.zIndex = "-5";
    // });
    back_btn_2.addEventListener("click", ()=>{
        // template_1.style.zIndex = "-5";
        template_2.style.zIndex = "-5";
    });
}

function calcularDistancia(lat1, lon1, lat2, lon2) {
    const R = 6371; // Radio de la Tierra en kilómetros
    const dLat = gradosARadianes(lat2 - lat1);
    const dLon = gradosARadianes(lon2 - lon1);
    const a = 
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(gradosARadianes(lat1)) * Math.cos(gradosARadianes(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distancia = R * c; // Distancia en kilómetros
    return distancia;
}

function gradosARadianes(grados) {
    return grados * (Math.PI / 180);
}
const distance_with_coord = document.getElementById("distance-with-coord");
const input_company_location_coord = document.getElementById("company_location_coord");
input_company_location_coord.addEventListener("new_coordinate", ()=>{
    let lat_1 = null;
    let lng_1 = null;
    if (cmpny_ltlg){
        let temp_1 = cmpny_ltlg.split(",");
        lat_1 = temp_1[0];
        lng_1 = temp_1[1];   
    
        let temp = input_company_location_coord.value.split(",");
        const distancia = calcularDistancia(lat_1, lng_1, temp[0], temp[1]);
        distance_with_coord.textContent = distancia.toFixed(2);
        const price_delivery = document.getElementById("price_per_delivery").value;
        const distance_max_delivery_cfg = document.getElementById("distance_max_delivery_cfg").value;
        const btn_confirm_delivery = document.getElementById("confirm-send-by-delivery");
        if (distancia.toFixed(2) <= parseFloat(distance_max_delivery_cfg)){
            btn_confirm_delivery.removeAttribute("disabled");
            btn_confirm_delivery.removeAttribute("style");
        }else{
            btn_confirm_delivery.style.textDecoration = "line-through";
            btn_confirm_delivery.disabled = true;
            openModalMessageLittle("<span>Rango de distancia no permitida.</span>", true);
        }
        update_cost_delivery(price_delivery);
    }
});
