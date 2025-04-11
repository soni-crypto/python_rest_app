const btn_open_profile = document.getElementById("open-profile-mobile-view");
const btn_close_profile = document.getElementById("close-profile-mobile-view");
const panel_div = document.getElementById("profile-user-details-in-panel");

btn_open_profile.addEventListener("click", () =>{
    panel_div.style.width = "16rem";
    panel_div.style.overflow = "visible";
    panel_div.style.position = "absolute";
    panel_div.style.left = "0rem";
})
    btn_close_profile.addEventListener("click", ()=>{
    panel_div.style.width = "0px";
    panel_div.style.overflow = "hidden";
})