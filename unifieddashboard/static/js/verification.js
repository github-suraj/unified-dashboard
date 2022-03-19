async function postAjax(url, data) {
    return $.ajax({
        url: url,
        type: 'POST',
        data: data,
        dataType: 'json',
        success: function(json) {
            var jsonData = json;
            return jsonData;
        }
    }); 
}

async function generate_mail_otp(otp_type) {
    var email = $('#id_email').val();
    var csrf_token = $("[name=csrfmiddlewaretoken]").val();
    var model = document.getElementById('signupOTPModel');
    var modelText = document.getElementById('signupOTPModelText');

    modelText.innerHTML = '';
    modelText.style.color = 'red';

    $('#loading').show();
    if (email === '') {
        modelText.innerHTML = 'Please enter a valid email address!';
    } else {
        var url = '/verifications/mail/' + otp_type;
        var data = {
            "email": email,
            "csrfmiddlewaretoken": csrf_token
        }
        try {
            var jsonData = await postAjax(url, data);
            modelText.innerHTML = jsonData.message;
            if (jsonData.success == true) {
                modelText.style.color = 'green';
            }
        } catch(error) {
            modelText.innerHTML = 'Unable to sent email with OTP';
        }
    }
    $('#loading').hide();
    model.showModal();
}
