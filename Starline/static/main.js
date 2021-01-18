
var modal = document.getElementById('modal');

$('#modal-btn').click(function () {
    console.log('show');
    modal.style.display = 'block';
});

$('.close').click(function () {
    console.log('hide');
    modal.style.display = 'none';
    document.getElementById('customer-form').reset();
});


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

function validateCustomerDeletion() {

}

function validateOrderDeletion() {

}

$(document).ready(function () {

    $('#searchbar').on('keyup', function () {

        const search = $('#searchbar').val();

        // POST
        fetch('/home', {
            // Specify the method
            method: 'POST',
            // JSON
            headers: { 'Content-Type': 'application/json' },
            // A JSON payload
            body: JSON.stringify(search),

        }).then(function (response) { // At this point, Flask has printed our JSON
            return response.text();
        }).then(function (data) {
            var val = $('#searchbar').val();
            $('body').html(data);
            $('#searchbar').val(val);
            $('#searchbar').focus();
        });
    });

    $(document).ready(function () {
        if ($('.flash__body').html != "") {
            $(".flash").addClass("animate--drop-in-fade-out");
            setTimeout(function () {
                $(".flash").removeClass("animate--drop-in-fade-out");
            }, 4500);
        }
    });
});


