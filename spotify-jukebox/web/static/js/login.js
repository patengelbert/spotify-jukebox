$(function () {
    $('button').click(function () {
        var user = $('#username').val();
        var pass = $('#password').val();
        $.ajax({
            url: '/login',
            data: $('form').serialize(),
            type: 'POST',
            success: function (response) {
                window.parent.closeModal();
                window.parent.location.reload();
            },
            error: function (error) {
                /* Handle Erorr */
            }
        });
    });
});