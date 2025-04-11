const login = () => {
    const btn_validation = document.getElementById("btn-login-app");
    const number = document.getElementById("user_number");
    const password = document.getElementById("user_password");
    btn_validation.addEventListener("click", async() => {
        btn_validation.innerHTML = "<div class='loader'></div>";
        await fetch("/userapp/credential_validation?number="+String(number.value)+"&password="+String(password.value)).then(res => res.text()).then(data => {
            if (data === "ok"){
                location.href = "/userapp/redirect_home";
            }else{
                document.getElementById("message-credentials-incorrect").textContent = "Credencial incorrecto";
                btn_validation.innerHTML = "Acceder";
            }
        })
    });

}

const create_account_redirect = () =>{
    const btn = document.querySelector(".button-redirect-create");
    btn.addEventListener("click", ()=>{
        btn.innerHTML = "<div class='loader'></div>";
    })
}