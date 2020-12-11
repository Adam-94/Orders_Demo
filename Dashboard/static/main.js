
var modal = document.getElementById('modal');
var addBtn = document.getElementById('modal-btn');
var span = document.getElementsByClassName('close')[0];

var closeMsg = document.getElementsByClassName('msg-close')[0];
var div = document.getElementById('message-div');


$('#searchbar').on('keyup', function () {

    let search = $('#searchbar').val();

    // POST
    fetch('/home', {

        // Specify the method
        method: 'POST',

        // JSON
        headers: {
            'Content-Type': 'application/json'
        },

        // A JSON payload
        body: JSON.stringify(search)

    }).then(function (response) { // At this point, Flask has printed our JSON
        return response.text();
    }).then(function (data) {
        console.log(data);
        let val = $('#searchbar').val();
        $('body').html(data);
        $('#searchbar').val(val);
        $('#searchbar').focus();
    });
})


$(document).ready(function () {
    if ($('.flash__body').html != "") {
        $(".flash").addClass("animate--drop-in-fade-out");
        setTimeout(function () {
            $(".flash").removeClass("animate--drop-in-fade-out");
        }, 4500);
    }
});


addBtn.onclick = function () {
    console.log('show');
    modal.style.display = 'block';
}

span.onclick = function () {
    console.log('hide');
    modal.style.display = 'none';
    document.getElementById('customer-form').reset();
}

closeMsg.onclick = function () {
    div.style.display = 'none';
}

function validateAndSend() {
    if (form.fname.value == '' || form.lname.value == '' ||
        form.address.value == '' || form.phone.value == '') {
        console.log(form.fname.value);
    }
    else {
        $('#customer-form').submit();
    }
}

function validateOrderForm() {
    if (form.invoice.value == '' || form.order.value == '') {
        console.log(form.invoice.value);
    }
    else {
        $('#order-form').submit();
    }
}

