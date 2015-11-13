$(function () {
    $('button').bind('click', function () {
        var user = $('#username').val();
        var pass = $('#password').val();
        $.ajax({
            url: '/login',
            data: $('form').serialize(),
            type: 'POST',
            success: function (response) {
                window.parent.location.reload();
            },
            error: function (error) {
                /* set error message*/
                $("#error_message").text(request.responseText);
                $(".error").show();
            }
        });
        return false;
    });
});