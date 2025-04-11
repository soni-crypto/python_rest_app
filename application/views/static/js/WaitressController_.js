class WaitressController{
    searchWaitressCreate(){
        const input_search = document.getElementById("user_search");
        const btn_search = document.getElementById("btn-search-user");
        const container_result = document.getElementById("cotainer-result-search-users");
        let id_w = null;
        btn_search.addEventListener("click", async()=>{
            let value = input_search.value;
            await fetch("waitress/waitress_search?e="+String(value)).then(res => res.json()).then(data =>{
                id_w = data.id;
                container_result.innerHTML="";
                
                if (Object.keys(data).length > 0) {
                    if (data.status === "Libre"){
                        
                    }
                    let template =  '<div class="container-block">'+
                                    '    <div class="container-image-profile">'+
                                    '        <img src="'+ data.image +'" alt="profile user">'+
                                    '    </div>'+
                                    '    <div class="container-info-user">'+
                                    '        <div class="row-details-user">'+
                                    '            <strong>Nombre: </strong>'+
                                    '            <span>'+ data.first_name +'</span>'+
                                    '        </div>'+
                                    '        <div class="row-details-user">'+
                                    '            <strong>Apellido: </strong>'+
                                    '            <span>'+ data.last_name +'</span>'+
                                    '        </div>'+
                                    '        <div class="row-details-user">'+
                                    '            <strong>Estado: </strong>'+
                                    '            <span>'+ data.status +'</span>'+
                                    '        </div>'+
                                    '        <div class="container-button-append-user">'+
                                    '            <button class="button-append-user" data-m="'+ data.id +'">'+
                                    '                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"><path fill="#ffffff" d="M19.49 5.57a6 6 0 0 1-1.893 8.962c-.649.351-1.43.135-1.952-.386l-5.79-5.791c-.522-.522-.738-1.303-.388-1.952A6 6 0 0 1 18.43 4.51l2.29-2.29a.75.75 0 1 1 1.061 1.06zm-2.017 7.263a4.5 4.5 0 1 0-6.306-6.306c-.266.349-.186.833.125 1.143l5.038 5.038c.31.31.794.391 1.143.125M3.28 21.78l2.29-2.29a6 6 0 0 0 8.962-1.893c.351-.649.135-1.43-.387-1.952l-5.79-5.79c-.522-.522-1.303-.738-1.952-.388A6 6 0 0 0 4.51 18.43l-2.29 2.29a.75.75 0 1 0 1.06 1.061m4.39-10.488l5.038 5.038c.31.31.39.794.125 1.143a4.5 4.5 0 1 1-6.306-6.306c.349-.266.833-.186 1.143.125"/></svg>'+
                                    '                Enviar solicitud</button>'+
                                    '        </div>'+
                                    '    </div>'+
                                    '</div>';
                    container_result.insertAdjacentHTML("afterbegin", template);
                    
                }else{
                    
                    let template = '<div class="text-not-found-users"><span>🤔</span><span>No encontrado</span></div>';
                    container_result.insertAdjacentHTML("afterbegin", template);
                    
                }
            });           
        });
        container_result.addEventListener("click", async(el)=>{
            if (el.target.className === "button-append-user"){
                if (id_w){
                    const identifier  = id_w;
                    const form_data = new FormData();
                    form_data.append("id_user", id_w);
                    await fetch("waitress/waitress_link_up",{
                        method: "POST",
                        body : form_data,
                    }).then(res => res.json()).then(data =>{
                        if (data.response === "ok"){
                            el.target.setAttribute("disabled", true);
                            el.target.style.cursor = "not-allowed";
                            el.target.textContent = "Solicitud enviado";
                        }else if(data.response === "exists"){
                            el.target.setAttribute("disabled", true);
                            el.target.style.cursor = "not-allowed";
                            el.target.textContent = "En espera";
                        }else{
                            el.target.setAttribute("disabled", true);
                            el.target.style.cursor = "not-allowed";
                            el.target.textContent = "Ocurrió un error";
                        }
                        console.log("id_user: ", id_w, data);
                        // setTimeout(()=>{
                        //     location.href = "waitress_view";
                        // }, 1000)
                    });
                }
            }
        });
    }
}