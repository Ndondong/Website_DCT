function show_image(img, idn) {
	if (img.files && img.files[0]) {
		var read = new FileReader();
		read.onload = function (e) {
			$('#' + idn + '')
				.attr('src', e.target.result)
				// .width(100)
				.height(200)
		};
		read.readAsDataURL(img.files[0]);
	}
}