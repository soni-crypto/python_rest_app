const animate_btn = () => {
    const btn_view_ = document.getElementById("btn-view-products-in-cart");

}
const add_to_cart = () =>{
    document.getElementById("btn-close-admin-not-supported").addEventListener("click", () => {closeModal(document.getElementById("modal-message-admin-not-supported"));});
    document.getElementById("modal-background-admin-not-supported").addEventListener("click", () => {closeModal(document.getElementById("modal-message-admin-not-supported"));});
    
    const btn_add = document.querySelectorAll(".button-append-product-to-car");
    btn_add.forEach( btn =>{
        btn.addEventListener("click", ()=>{
            svg_animate = btn.previousElementSibling;
            svg_animate.style.display = "block";
            setTimeout(()=>{
                svg_animate.style.display = "none";
            }, 1000);
            let identifier = btn.dataset.identifier;
            let app = btn.dataset.app;
            let price_unique = btn.dataset.price_unique;
            
            const products = localStorage.getItem("products");
            if (products){
                const product_list = JSON.parse(products);
                
                const unique_admin = product_list.map(item => item.app).every(app_ls => {
                    return parseInt(app_ls) === parseInt(app);
                } );
                
                if (unique_admin || product_list.length === 0){
                    let not_exist = true;
                    product_list.forEach(product =>{
                        if (parseInt(product.identifier) === parseInt(identifier)){
                            product.cantity = product.cantity + 1;
                            not_exist = false;
                        }
                    })
                    if (not_exist){
                        product_list.push({"identifier" : identifier, "cantity": 1, "app":app, "price_unique":price_unique});
                    }
                    localStorage.setItem("products", JSON.stringify(product_list));
                }else{
                    openModal(document.getElementById("modal-message-admin-not-supported"));
                }

            }else{
                const data = [{"identifier" : identifier, "cantity": 1, "app": app, "price_unique":price_unique}]
                localStorage.setItem("products", JSON.stringify(data));
            }
        })
    })
}