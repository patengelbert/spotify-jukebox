$('a.open-login-dialog').on('click', function (e) {
    var src = $(this).attr('data-src');
    var height = $(this).attr('data-height') || 330;

    $("#loginModal iframe").attr({
        'src': src,
        'height': height,
    });
});