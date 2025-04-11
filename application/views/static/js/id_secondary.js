const update_id_secondary = () =>{
    const id_secondary_input = document.getElementById("id_secondary");
    const container_state = document.getElementById("container-state-id-secondary");
    const loader_ping = container_state.querySelector(".loader-ping");
    const svg_1 = container_state.querySelectorAll("svg")[0];
    const svg_2 = container_state.querySelectorAll("svg")[1];
    id_secondary_input.addEventListener("input", async()=>{
        loader_ping.style.display="block";
        svg_1.style.display="none";
        svg_2.style.display="none";
        await fetch("/honey/update_id_secondary?value="+String(id_secondary_input.value)).then(res => res.text()).then(data =>{
            if (data === "ok"){
                // id_secondary_input.name = "id_secondary";
                svg_2.style.display="none";
                loader_ping.style.display="none";
                svg_1.style.display="block";
            }else{
                // id_secondary_input.name = "";
                svg_1.style.display="none";
                loader_ping.style.display="none";
                svg_2.style.display="block";
            }
            
        });
    })
}