const modal_day_app = document.getElementById("config-disp-day-app");
const eventDispInputId = document.getElementById("eventDisp");
const btn_create_new_event = document.getElementById("btn-create-new-event");
const dataDay = {};
document.addEventListener("click", (e)=>{
    // if (e.target.classList.contains("fc-daygrid-day-frame") && !e.target.parentElement.classList.contains("fc-day-disabled")){
    //     dataDay.start = e.target.parentElement.dataset.date;
    //     eventDispInputId.value = "";
    //     btn_create_new_event.textContent = "Guardar";
        // console.log("js aparte")
        // openModal(modal_day_app);
    // }
})
const input_state = document.getElementById("state");
const input_title = document.getElementById("title");
const input_date_end = document.getElementById("date-end");
const input_date_start = document.getElementById("date-start");
const input_backgroundColor = document.getElementById("backgroundColor");
const input_textColor = document.getElementById("textColor");
const input_url = document.getElementById("url");
// btn_create_new_event.addEventListener("click", async()=>{
//     btn_create_new_event.disabled = true;
//     let route_ = "";
//     if (eventDispInputId.value){
//         route_ = "/honey/schedule/update";
//         dataDay.id = eventDispInputId.value;
//         dataDay.start = input_date_start.value;
//     }else{
//         route_ = "/honey/schedule/create";
//     }
//     dataDay.title = input_title.value; 
//     dataDay.end = input_date_end.value; 
//     dataDay.url = input_url.value,
//     dataDay.state = input_state.value;
//     dataDay.display = ""; // background para descativar cuadro
//     dataDay.color = "";
//     dataDay.backgroundColor = input_backgroundColor.value;
//     dataDay.textColor = input_textColor.value;
//     dataDay.borderColor = input_backgroundColor.value;
//     dataDay.overlap = "";
//     dataDay.groupId = input_state.value;
//     dataDay.constraint = "";
//     await fetch(route_, {
//         method: "post",
//         headers: {
//             "Content-Type" : "application/json",
//         },
//         body: JSON.stringify(dataDay),
//     }).then(res => res.json()).then(data =>{
//         location.reload();
//     })
// })