const update_profile = () => {
    const btn_submit_update = document.getElementById("btn_submit_update");

    const image_preview = document.getElementById("image-preview-main");
    const image_update_input = document.getElementById("image_update_input");      
    image_update_input.addEventListener("change", () =>{
        const lector = new FileReader();
        const accepted_extensions = ["image/webp", "image/jpeg", "image/png", "image/jpg"]
        console.log(image_update_input.files[0].type);
        if (accepted_extensions.includes(image_update_input.files[0].type)){
            if (image_update_input.files[0]){
                lector.onload = function (e){
                    image_preview.src = e.target.result;
                }
                lector.readAsDataURL(image_update_input.files[0]);
            }
        }else{
            let ms = document.querySelector(".message-main-span-update");
            ms.textContent="El archivo seleccionado no es una imagen";
            ms.style.color = "red";
            setTimeout(()=>{
                ms.textContent = "";
                ms.removeAttribute("style");
            }, 2000);
        }
    })


    const first_name_update_input =document.getElementById("first_name_update_input");
    const last_name_update_input = document.getElementById("last_name_update_input");
    const email_update_input = document.getElementById("email_update_input");
    const tel_whats_update_input = document.getElementById("tel_whats_update_input");
    const location_update_input = document.getElementById("location_update_input");
    const password_update_input = document.getElementById("password_update_input");
    btn_submit_update.addEventListener("click", async() =>{
        const form_data = new FormData();
        form_data.append("image", image_update_input.files[0]);
        form_data.append("first_name", first_name_update_input.value);
        form_data.append("last_name", last_name_update_input.value);
        form_data.append("email", email_update_input.value);
        form_data.append("tel_whats", tel_whats_update_input.value);
        form_data.append("location", location_update_input.value);
        form_data.append("password", password_update_input.value);
        await fetch("/userapp/profile/edit_profile", {
            method : "POST",
            body : form_data,
        }).then(res => res.text()).then(data => {
            const span_message = document.querySelector(".message-main-span-update");
            if (data === "ok"){
                span_message.textContent = "Cambios guardados correctamente";
            }else{
                span_message.textContent = "Ocurrió un error";
            }
            setTimeout(() =>{
                span_message.textContent = "";
            }, 1200)
        })
    })
}
