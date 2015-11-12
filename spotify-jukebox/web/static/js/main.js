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

function login_success(user){
	current_user = user;
	$(".open-login-dialog").each(function(e){
		$(this).hide();
	});
	$("#user-link").show();
	$("#logout-link").show();
	if(current_user.admin){
		$("#admin-link").show();
	}
}

$('a#logout-link').on('click', function (e){
	current_user = null;
	$(".open-login-dialog").each(function(e){
		$(this).show();
	});
	$("#user-link").hide();
	$("#logout-link").hide();
	$("#admin-link").hide();
});