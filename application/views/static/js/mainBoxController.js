const closeBoxMain = () =>{
    const btn_submit = document.getElementById("btn-submit-close-box");
    btn_submit.addEventListener("click", async()=>{
        await fetch("/honey/mainbox/close").then(res => res.json()).then(data =>{
            location.reload();
        })
    })
}
const openBoxMain = () =>{
    const form = document.getElementById("form-open-box");
    form.addEventListener("submit", async(e)=>{
        e.preventDefault();
        const form_data = new FormData(form);
        await fetch("/honey/mainbox/open", {
            method:"post",
            body:form_data,
        }).then(res => res.json()).then(data =>{
            location.reload();
        })
    })
}
const registerExpensesIncome = () =>{
    const form1 = document.getElementById("form-income");
    const form2 = document.getElementById("form-expenses");
    form1.addEventListener("submit", async(e)=>{
        e.preventDefault();
        const form_data = new FormData(form1);
        await fetch("/honey/mainbox/register_ei", {
            method : "post",
            body : form_data,
        }).then(res => res.json()).then(data =>{
            location.reload();
        })
    })
    form2.addEventListener("submit", async(e)=>{
        e.preventDefault();
        const form_data = new FormData(form2);
        await fetch("/honey/mainbox/register_ei", {
            method : "post",
            body : form_data,
        }).then(res => res.json()).then(data =>{
            location.reload();
        })
    })
}
const ieBox = () =>{
    const btns = document.querySelectorAll(".btn-ie-controll-box");
    btns.forEach(btn=>{
        btn.addEventListener("click", async()=>{
            let i = btn.dataset.identifier;
            await fetch ("/honey/mainbox/delete_ei?i="+String(i)).then(res => res.json()).then(data =>{
                location.reload();
            });
        })
    })
}
const createBox = () =>{
    const input = document.getElementById("input-name-new-box");
    const btn = document.getElementById("btn-create-new-box");
    btn.addEventListener("click", async()=>{
        if (input.value){
            const form_data = new FormData();
            await fetch("").then(res => res.json()).then(data =>{
                console.log(data);
            })
        }else{

        }
    })
}
