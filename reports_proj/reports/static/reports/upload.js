const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
const alertBox = document.getElementById('alert-box');

Dropzone.autoDiscover = false;
const myDropzone = new Dropzone('#my-dropzone', {
    url: '/reports/upload/',
    init: function(){
        this.on('sending', function(file, xhr, formData){
            console.log('sending');
            formData.append('csrfmiddlewaretoken', csrf);
        })
        this.on('success', function(file, response){
            // console.log(response.exists);
            var alertStyle = '';
            if (response.exists){
                alertStyle = `
                    <div class="alert alert-danger" role="alert">
                        Oops! Looks like this file is already uploaded.
                    </div>`
            }else{
                alertStyle = `
                    <div class="alert alert-success" role="alert">
                        Your file is uploaded sucessfully.
                    </div>`
            }
            alertBox.innerHTML = alertStyle;
        })
    },
    maxFiles: 3,
    maxFilesize: 5,
    acceptedFiles: '.csv',
});