$(document).ready(function () {

    $.getJSON('klucz.php', function (data) {
        $('#nonce').val(data.nonce);
    });

    $('#send').click(function () {
        $.ajax({
            url: 'switching.php',  // Najpierw pobierz najlepszy serwer
            method: 'POST',
            success: function (data) {
                if (data && data.server) {
                    var najlepszySerwer = data.server;

                    var url = 'http://' + najlepszySerwer + '/wer.php';

                    // Wysłanie właściwego żądania AJAX do wybranego serwera
                    $.ajax({
                        url: url,
                        method: 'POST',
                        data: JSON.stringify({
                            user: $('#user').val(),
                            net: $('#net').val(),
                            nonce: $('#nonce').val()
                        }),
                        contentType: 'application/json; charset=utf-8',
                        success: function (data) {
                            console.log(data);
                            if (data && data.code === 'OK') {
                                $('#alertbad').removeClass('d-block').addClass('d-none');
                                $('#alertok').removeClass('d-none').addClass('d-block');
                            } else {
                                $('#alertok').removeClass('d-block').addClass('d-none');
                                $('#alertbad').removeClass('d-none').addClass('d-block');
                            }
                        },
                        error: function (xhr, status, error) {
                            console.error("Error with the request:", error);
                        }
                    });
                } else {
                    console.error("Server response is invalid:", data);
                }
            },
            error: function (xhr, status, error) {
                console.error("Error with switching request:", error);
            }
        });

    });


    function generateNonce() {
        return Math.random().toString(36).substring(2, 15);
    }

    function hash(value) {
        return CryptoJS.MD5(value).toString(CryptoJS.enc.Hex);
    }

    function calculateNet() {
        const password = $('#pass').val();
        const nonce = $('#nonce').val();
        if (password && nonce) {
            return hash(hash(password) + nonce);
        }
        return '';
    }

    $('#user, #pass').on('input', function () {
        $('#net').val(calculateNet());
    });
});