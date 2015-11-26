var x = 0;

function getAlbumImages(songs) {
	for ( i = 0; i < songs.values.length; i++) {
		$.ajax({
			url : 'https://api.spotify.com/v1/tracks/' + songs.values[i],
			success : function(response) {
				create_panel(response);
			}
		});

	}
}

function carouselElement(i, src) {
	return $('<div></div>')
		.addClass("item")
		.append($('<p></p>')
			.text()
			)
		.append($('<img></img>')
			.attr({
			'src' : src
			})
			.addClass("first-slide")
		);
}

function create_panel(result) {
	element_nav = $('<li></li>').attr({
		'data-target' : "#myCarousel",
		'data-slide-to' : x
	});
	element_main = $('<div></div>')
		.addClass("item")
		.append($('<div></div>')
			.addClass('container')
			.append($('<div></div>')
				.addClass('carousel-caption')
				.append($('<img></img>')
					.attr({'src': result.album.images[0].url})
					.css({'maxWidth': "100%",
						  'maxHeight':"450px",
						  'minWidth': "500px"
					})
				)
				.append($('<div></div>')
					.addClass('carousel-caption-text-wrapper')
					.append($('<h1></h1>')
						.text(x+1)
					)
					.append($('<p></p>')
						.text(result.name)
					)
				)
			)
		)
		.append($('<img></img>')
			.attr({
			'src' : "data:image/gif;base64,R0lGODlhAQABAIAAAHd3dwAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw=="
			}).append($('<img></img>')
					.attr({'src': result.album.images[0].url})
					.css({'maxWidth': "100%",
						  'maxHeight':"450px"
					})
				)
		);
	if (x == 0) {
		element_nav.addClass('active');
		element_main.addClass('active');

	}
	$('.carousel-indicators').append(element_nav);
	$('.carousel-inner').append(element_main);
	x++;
}
