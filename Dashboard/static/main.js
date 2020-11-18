
var modal = document.getElementById('modal');
var addBtn = document.getElementById('modal-btn');
var span = document.getElementsByClassName('close')[0];

var closeMsg = document.getElementsByClassName('msg-close')[0];
var div = document.getElementById('message-div');


$("#table").on('click','#table-view',function(){
    // get the current row
    var currentRow=$(this).closest("tr"); 
    var customerID =currentRow.find("td:eq(0)").text(); // customer ID
    
    fetch('/view_customer', {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(customerID),
        cache: "no-store",
        headers: new Headers({
            "content-type": "application/json"
        })
    })

    .then(function(res) {
        if (res.status !== 200) {
            console.log('Problem with status code: ' + res.status);
            return;
        }

        res.json().then(function (data) {
            console.log(data);
        });
    })
    .catch(function (error) {
        console.log('Fetch error: ' + error)
    });
})

addBtn.onclick = function() {
    console.log('show');
    modal.style.display = 'block';
}

span.onclick = function() {
    console.log('hide');
    modal.style.display = 'none';
    document.getElementById('customer-form').reset();
}

closeMsg.onclick = function() {
    div.style.display = 'none';
}

function validateAndSend() {
    if (form.fname.value == '' || form.lname.value == '' ||
        form.address.value == '' || form.phone.value == '') {
            console.log($('form').serializeArray());
            console.log(form.fname.value);
        }
    else {
        console.log('Submitting form')
        $('#customer-form').submit();
    }
}

