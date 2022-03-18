function generate_mail_otp(otp_type) {
    $('.alert-success').hide();
    $('.alert-danger').hide();
    var email = $('#id_email').val();
    var csrf_token = $("[name=csrfmiddlewaretoken]").val();
    if (email === '') {
        alert('Please enter a valid email address');
    } else {
        $.post('/verifications/mail/' + otp_type,
            {
                "email": email,
                "csrfmiddlewaretoken": csrf_token
            },
            function(data, status) {
                if (status == "success") {
                    if (data === 'None') {
                        $('.alert-danger').show();
                    } else {
                        $('.alert-success').show();
                    }
                }
            }
        );
    }
}