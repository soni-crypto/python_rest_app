
let mode_portrait = false;
if (window.innerHeight > window.innerWidth){
    mode_portrait = true;
}
window.addEventListener("resize", ()=>{
    if (window.innerHeight > window.innerWidth){
        mode_portrait = true;
    }else{
        mode_portrait = false;
    }
})
if (mode_portrait){
    localStorage.setItem("config_nav", JSON.stringify({"state":"close", "mode":"light"}))
}
const container_data_body_all = document.getElementById("container-main-body-template-app");
const btn_with_more_option = document.querySelectorAll(".btn-with-more-option");
btn_with_more_option.forEach((btn)=>{
    btn.addEventListener("click", ()=>{
        let div_ctn = btn.nextElementSibling;
        if (div_ctn.style.display === "flex"){
            div_ctn.style.display = "none";
        }else{
            div_ctn.style.display = "flex";
        }
    })
});
let config_nav = localStorage.getItem("config_nav");
const nav_container_left = document.getElementById("container-main-nav-left");
const btn_open_nav = document.querySelector(".btn-open-nav");
const btn_close_nav = document.querySelector(".btn-close-nav");
if (!config_nav){
    localStorage.setItem("config_nav", JSON.stringify({"state":"close", "mode":"light"}))
    if(!mode_portrait){
        localStorage.setItem("config_nav", JSON.stringify({"state":"open", "mode":"light"}))
        nav_container_left.style.width = "14.1rem";
        container_data_body_all.style.marginLeft = "14.1rem";
        container_data_body_all.style.width = "calc(100% - 14.1rem)";
    };
}else{
    config_nav = JSON.parse(config_nav);
    if (config_nav.state === "open"){
        nav_container_left.style.width = "14.1rem";
        btn_open_nav.style.display = "none";
        btn_close_nav.style.display = "block";
        if(!mode_portrait){
            container_data_body_all.style.marginLeft = "14.1rem";
            container_data_body_all.style.width = "calc(100% - 14.1rem)";
        }
    }else{
        nav_container_left.style.width = "0rem";
        btn_open_nav.style.display = "block";
        btn_close_nav.style.display = "none";
        container_data_body_all.style.marginLeft = "0rem";
        container_data_body_all.style.width = "100%";
    }
    
    btn_open_nav.addEventListener("click", ()=>{
        nav_container_left.style.width = "14.1rem";
        btn_close_nav.style.display = "block";
        btn_open_nav.style.display = "none";
        if(!mode_portrait){
            container_data_body_all.style.marginLeft = "14.1rem";
            container_data_body_all.style.width = "calc(100% - 14.1rem)";
        }
        localStorage.setItem("config_nav", JSON.stringify({"state":"open", "mode":"light"}))
    })
    btn_close_nav.addEventListener("click", ()=>{
        nav_container_left.style.width = "0rem";
        btn_close_nav.style.display = "none";
        btn_open_nav.style.display = "block";
        container_data_body_all.style.marginLeft = "0rem";
        container_data_body_all.style.width = "100%";
        localStorage.setItem("config_nav", JSON.stringify({"state":"close", "mode":"light"}))
    })
}
// const btn_open_modal_notify = document.getElementById("btn-open-modal-notify");
// const btn_open_modal_profile = document.getElementById("btn-open-modal-profile");
// btn_open_modal_notify.addEventListener("click", ()=>{
//     let div_ctn = btn_open_modal_notify.nextElementSibling;
//     if(div_ctn.style.display === "flex"){
//         div_ctn.style.display = "none";
//     }else{
//         div_ctn.style.display = "flex";
//         btn_open_modal_profile.nextElementSibling.style.display="none";
//     }
// })
// btn_open_modal_profile.addEventListener("click", ()=>{
//     let div_ctn = btn_open_modal_profile.nextElementSibling;
//     if(div_ctn.style.display === "flex"){
//         div_ctn.style.display = "none";
//     }else{
//         div_ctn.style.display = "flex";
//         btn_open_modal_notify.nextElementSibling.style.display="none";
//     }
// })


// cerrar notificaciones de conexion frontend y backend
const btn_close_flashed_messages = document.querySelectorAll(".close-flashed-message");
btn_close_flashed_messages.forEach(b=>{ b.addEventListener("click", ()=>{ b.parentElement.parentElement.remove(); }); });

// loader mobile controll
const main_loader_mobile = document.getElementById('container-main-loader-mobile-all');
const loader_container_type_classroom = document.querySelector(".loader-container-type-classroom");
if (mode_portrait){
    document.querySelectorAll('form').forEach(link => {
        link.addEventListener('submit', function(event) {
            main_loader_mobile.style.display = 'flex';
            loader_container_type_classroom.style.display = "initial";
        });
    });
    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function(event) {
            main_loader_mobile.style.display = 'flex';
            loader_container_type_classroom.style.display = "initial";
        });
    });
    window.addEventListener('popstate', function(event) {
        main_loader_mobile.style.display = 'none';
        loader_container_type_classroom.removeAttribute("style");
    });
    window.addEventListener('load', function() {
        main_loader_mobile.style.display = 'none';
        loader_container_type_classroom.removeAttribute("style");
    });
    window.addEventListener('pageshow', function(event) {
        main_loader_mobile.style.display = 'none';
        loader_container_type_classroom.removeAttribute("style");
    });
    
}else{
    document.querySelectorAll('form').forEach(link => {
        link.addEventListener('submit', function(event) {
            loader_container_type_classroom.style.display = "initial";
        });
    });
    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function(event) {
            loader_container_type_classroom.style.display = "initial";
        });
    });
    window.addEventListener('popstate', function(event) {
        loader_container_type_classroom.removeAttribute("style");
    });
    window.addEventListener('load', function() {
        loader_container_type_classroom.removeAttribute("style");
    });
    window.addEventListener('pageshow', function(event) {
        loader_container_type_classroom.removeAttribute("style");
    });
}