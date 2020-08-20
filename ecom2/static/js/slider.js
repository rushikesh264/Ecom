
		var slideIndex = 1;
		var timer = null;
		showSlides(slideIndex);
	
		// Next/previous controls
		function plusSlides(n) {
			clearTimeout(timer);
		  showSlides(slideIndex += n);
		}
		
		
		// Thumbnail image controls
		function currentSlide(n) {
			clearTimeout(timer);
			
		  showSlides(slideIndex = n);
		}
	  
		function showSlides(n) {
		  var i;
		  var slides = document.getElementsByClassName("mySlides");
		   var dots = document.getElementsByClassName("dot");
		   if (n==undefined){n = ++slideIndex}
		  if (n > slides.length) {slideIndex = 1}
		  if (n < 1) {slideIndex = slides.length}
		for (i = 0; i < slides.length; i++)
		{
			  slides[i].style.display = "none";
		  }
		 for (i = 0; i < dots.length; i++)
		  {
			  dots[i].className = dots[i].className.replace(" active1", "");
		  }

		 dots[slideIndex-1].className += " active1";
		  slides[slideIndex-1].style.display = "block";
		  timer = setTimeout(showSlides, 3000);
		}
