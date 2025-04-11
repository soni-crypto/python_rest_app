class NotificationsController{
    base_url =  "/honey/";
    closeModal(modal_id){
        const modal_close = document.getElementById(modal_id);
        $(modal_close).modal('hide');
    }
    openModal(modal_id){
        const modal_open = document.getElementById(modal_id);
        $(modal_open).modal('show');
    }
    approveRequest (){
        const btns = document.querySelectorAll(".button-approve-request");
        btns.forEach(btn =>{
            btn.addEventListener("click", async()=>{
                let identifier = btn.dataset.identifier;
                const form_data = new FormData();
                form_data.append("id", identifier);
                form_data.append("status", 2);
                await fetch(this.base_url + "waitress_linked_admin", {
                    method : "POST",
                    body : form_data,
                }).then(res => res.text()).then(data =>{
                    location.reload()
                })
            })
        })
    }
    rejectRequest (){
        const btns = document.querySelectorAll(".button-reject-request");
        btns.forEach(btn =>{
            btn.addEventListener("click", async()=>{
                let identifier = btn.dataset.identifier;
                const form_data = new FormData();
                form_data.append("id", identifier);
                form_data.append("status", 0);
                await fetch(this.base_url + "waitress_linked_admin", {
                    method : "POST",
                    body : form_data,
                }).then(res => res.text()).then(data =>{
                    location.reload()
                })
            })
        })
    }
    deleteRequest(){
        const btns_delete = document.querySelectorAll(".delete-btn-notification");
        btns_delete.forEach((btn) =>{
            btn.addEventListener("click", async() => {
                let row = btn.dataset.row;
                await fetch("/honey/notifications_users/delete?row="+String(row)).then(res => res.text()).then((data) => {
                    let parent = btn.parentElement.parentElement;
                    parent.remove()
                })
            })
        })
    }
}