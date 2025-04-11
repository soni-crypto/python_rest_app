

// funcion para autocompletar un formularo con un json por id o name
function JsonToForm(form_id, json, mode = "name", in_attr = "value"){
    try {
        if (mode === "name"){
            const form = document.getElementById(form_id);
            const inputs = form.querySelectorAll("input, select, textarea, radio, checkbox");
            for (const j in json){  
                inputs.forEach(i=>{
                    if (i.name === j){
                        if (i.tagName === "SELECT"){
                            const opts = i.querySelectorAll("option");
                            opts.forEach(o=>{
                                if (o.value === String(json[j])){
                                    o.setAttribute("selected", true);
                                }else{
                                    o.removeAttribute("selected");
                                };
                            });
                        }else if (i.tagName === "INPUT"){
                            i.value = json[j];
                        }
                    };
                });
            };
        }else if (mode === "class"){
            const ctn = document.getElementById(form_id);
            const tags = ctn.querySelectorAll("span, strong, h1, h2, h3, h4, h5");
            for (const j in json){  
                tags.forEach(i=>{
                    if (i.classList.contains(j)){
                        i.textContent = json[j];
                    };
                });
            };
        };
        return "ok";
    } catch (error) {
        return error;
    }
};