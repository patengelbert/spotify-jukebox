$('a.open-login-dialog').on('click', function (e) {
    var src = $(this).attr('data-src');
    var height = $(this).attr('data-height') || 330;
    var width = $(this).attr('data-width') || 400;

    $("#loginModal .modal-title").text(src.toUpperCase());
    $("#loginModal iframe").attr({
        'src': src,
        'height': height,
        'width': width
    });
});