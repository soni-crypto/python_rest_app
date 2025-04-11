const favorities = () =>{
    const checkbox_favority = document.querySelector(".checkbox-favority-admin");
    if(checkbox_favority){
        checkbox_favority.addEventListener("change", async() => {
            if (checkbox_favority.value){
                let state = 0;
                if (checkbox_favority.checked){
                    state = 1;
                }
                await fetch("/userapp/favorities/add?to="+String(checkbox_favority.value)+"&state="+String(state)).then(res => res.text()).then(data => {
                    console.log(data);
                })
            }else{
                console.log("error")
            }
        })  
    }
}