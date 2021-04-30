const modalBody = document.getElementById('modal-body');
const reportBtn = document.getElementById('report-btn');
const mainChart = document.getElementById('main-chart');
const reportForm = document.getElementById('report-form');
const alertBox = document.getElementById('alert-box');
// console.log(reportForm);

const reportName = document.getElementById('id_name');
const reportRemarks = document.getElementById('id_remarks');
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;


const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type} mt-3" role="alert">
           ${msg}
        </div>
    `
}

reportBtn.addEventListener('click', () => {
    mainChart.setAttribute('class', 'w-100')
    modalBody.prepend(mainChart);


    reportForm.addEventListener('submit', e => {
        console.log('Pressed');
        e.preventDefault();
        const formData = new FormData();

        formData.append('csrfmiddlewaretoken', csrf);
        formData.append('name', reportName.value);
        formData.append('remarks', reportRemarks.value);
        formData.append('image', mainChart.src);

        $.ajax({
            type: 'POST',
            url : 'reports/save/',
            data: formData,
            success: function(res){
                // console.log(res);
                
                handleAlerts('success', 'Report Created')
                reportForm.reset();
            },
            error: function(err){
                // console.log("Error Message" + err);
                handleAlerts('danger', 'Oops... Something went wrong...');
            },
            processData: false,
            contentType: false,
        });
    });
    
});

