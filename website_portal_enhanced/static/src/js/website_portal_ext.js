$(document).ready(function(){
    $('#image_src').change(function(){
        $('#preview_image').attr('src',"data:image/png;base64,"+$('#image_src').val());
    }).change();
});

function handle(files) {
    var file = files[0];
    var imageType = /image.*/;
    var img = document.createElement("img");
    img.classList.add("obj");
    img.file = file;
    var reader = new FileReader();
    reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result;
    $('#image_src').val((e.target.result).split(',')[1]).change();}; })(img);
    if (file){
        reader.readAsDataURL(file);
    }
}