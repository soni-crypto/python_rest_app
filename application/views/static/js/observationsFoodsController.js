class ObservationsFoodsController{
    delete(){
        const btns = document.querySelectorAll(".btn-delete-observation");
        btns.forEach((btn) => {
            btn.addEventListener("click", async()=>{
                let row = btn.dataset.identifier;
                await fetch ("/honey/observations_foods_delete?row="+String(row)).then(res => res.text()).then(data =>{
                    location.reload();
                })
            })
        })
    }
}