function showFile(e) {
    var f = e.target.files[0];
    if (!f.type.match('image.*')) return;
    var fr = new FileReader();
    fr.onload = (function(theFile) {
        return function(e) {
            var avatar = document.getElementById('avatar-image');
            avatar.src = e.target.result;
            avatar.style.display = 'block';
        };
    })(f);
    fr.readAsDataURL(f);
}
document.getElementById('inputImage').addEventListener('change', showFile, false);
