const template_html_icon = (id, name, url_name) =>{
    let template_html = `<div class='container-block-renderer-icon' ><img data-identifier='${id}' class='icon-food-image-search' src='${url_name}' alt='${name}'> <span class='tag is-small'>${name}</span></div>`;
    return template_html;
}
const image_input_controll = () =>{
    const input_text_list = document.querySelectorAll(".image_name_search_input");
    input_text_list.forEach((input_text)=>{
        input_text.addEventListener("input", async() =>{
            const container_all_icons  = input_text.nextElementSibling;
            container_all_icons.innerHTML = "Buscando...";
            let value_text = input_text.value;
            await fetch("/honey/images/get?search="+String(value_text)).then(res => res.json()).then(data=>{
                if (data.length > 0){
                    container_all_icons.innerHTML="";
                    data.forEach(element => {
                        container_all_icons.insertAdjacentHTML("beforeend", template_html_icon(element.id, element.name, element.url_name));
                    });
                }else{
                    container_all_icons.innerHTML ="No se encontró iconos";
                }
            })
        })
    })
}
document.addEventListener("click", (element)=>{
    const element_selected = element.target;
    if (element_selected.classList[0] === "icon-food-image-search"){
        let container_all = element_selected.parentElement.parentElement;
        let identifier = element_selected.dataset.identifier;
        let name = element_selected.getAttribute("alt");
        const it = container_all.previousElementSibling;
        const ih = it.previousElementSibling;
        it.value = name;ih.value = identifier;


    }
})  

/* <input type="hidden" name="image-edit" id="image-edit" required>
<input type="text" id="image_name_search_input" class="form-control" required>
<div class="container-all-image-renderer-search-user"></div> */