const openModal = (id_modal) => {
    document.getElementById(id_modal).classList.add("is-active");
}
const closeModal = (id_modal) => {
    document.getElementById(id_modal).classList.remove("is-active");
}
const create_account = () =>{
    const last_name = document.getElementById("last_name");
    const first_name = document.getElementById("first_name");
    const email = document.getElementById("email");
    const telephone = document.getElementById("telephone");
    const password = document.getElementById("password");

    const input_all = document.querySelectorAll(".input-required");
    const btn_submit = document.getElementById("btn-create-account");
    const email_link_tag = document.getElementById("email-verification-link");
    btn_submit.addEventListener("click", async () =>{
        let state = true;
        input_all.forEach(input =>{
            if (input.value.length <=0){
                state = false;
            }
        })
        if (state){
            btn_submit.innerHTML = "<div class='loader'></div>";
            btn_submit.disabled = true;
            const form_data = new FormData();
            form_data.append("first_name", first_name.value);
            form_data.append("last_name", last_name.value);
            form_data.append("email", email.value);
            form_data.append("tel_whats", telephone.value);
            form_data.append("password", password.value);

            await fetch("/userapp/create-account", {
                method : "POST",
                body : form_data,
            }).then(res => res.text()).then(data => {
                if (data === "ok"){
                    btn_submit.innerHTML = "Crear cuenta";
                    btn_submit.disabled = false;
                    email_link_tag.setAttribute("href", "mailto:"+email.value);
                    email_link_tag.textContent = email.value;
                    openModal("modal-code-verification-main");

                    const code_1 = document.getElementById("code-1");
                    const code_2 = document.getElementById("code-2");
                    const code_3 = document.getElementById("code-3");
                    const code_4 = document.getElementById("code-4");
                    const list_code = [code_1, code_2, code_3, code_4];
                    list_code.forEach((ic, index)=>{
                        ic.addEventListener("input", ()=>{
                            if (list_code[index + 1]){
                                list_code[index + 1].focus();
                            }                                
                        })
                    });
                    
                    const btn_verification = document.getElementById("continue-btn");
                    btn_verification.addEventListener("click", async() => {
                        btn_verification.disabled = true;
                        btn_verification.textContent = "Autenticando...";
                        if (code_1.value.length > 0 && code_2.value.length > 0 && code_3.value.length > 0 && code_4.value.length > 0){
                            const code_verification = code_1.value + code_2.value + code_3.value + code_4.value;
                            await fetch("/userapp/code_verification?code_verification="+String(code_verification)).then(res => res.text()).then(data => {
                                if (data === "ok"){
                                    location.href = "/userapp/redirect_home";
                                }else{
                                    const text_failed = document.getElementById("container-message-code-incorrect__text");
                                    text_failed.style.display="block";
                                    setTimeout(() => {
                                        text_failed.style.display = "none";
                                        btn_verification.textContent = "Continuar";
                                        btn_verification.disabled = false;
                                    }, 1500)
                                }
                            })
                        }else{
                            const text_failed = document.getElementById("container-message-code-incorrect__text");
                            text_failed.style.display="block";
                            setTimeout(() => {
                                text_failed.style.display = "none";
                                btn_verification.textContent = "Continuar";
                                btn_verification.disabled = false;
                            }, 1500)
                        }
    
                    })
                }else if(data === "email"){
                    email.value="";
                    email.style.borderColor = "red";
                    btn_submit.innerHTML = "Crear cuenta";
                    btn_submit.disabled = false;
                }else if(data === "tel_whats"){
                    telephone.value="";
                    telephone.style.borderColor = "red";
                    btn_submit.innerHTML = "Crear cuenta";
                    btn_submit.disabled = false;
                }
            })
        }
    })
}
const closeModelVerification = () =>{
    const md = document.getElementById("modal-verification-close");
    md.addEventListener("click", ()=>{
        for (let i=1;i<=4; i++){
            document.getElementById("code-"+i).value = "";  
        }   
        closeModal("modal-code-verification-main");
    })
}