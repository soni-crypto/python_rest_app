const preview_image = (input_image, image) => {
    const tag_input_image = document.getElementById(input_image);
    const image_preview = document.getElementById(image);
    const file = new FileReader();
    tag_input_image.addEventListener("change", () =>{
        if (tag_input_image.files[0]){
            file.onload = function(e){
                image_preview.src = e.target.result;
            };
            file.readAsDataURL(tag_input_image.files[0]);
        }
    })
}