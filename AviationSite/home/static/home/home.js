var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

// function for showing slide number 'n'
function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
  // setTimeout(showSlides, 2000);
}

var timeout;

// Loaded when page loads. It cycles through the pictures
// Had to load it when the first 'long' image loads cause it wouldn't detect the body loading
// Maybe its becuase this loading is needed for the body to fully load, making some weird paradox
function cycleSlides() {
  slideIndex++;
  showSlides(slideIndex);
  timeout = setTimeout(cycleSlides, 5000);
}

// Cancels the cycle when the mouse is moved over the slideshow,
// so that the user can view the images at their leisure
function cancelautoslide() {
  clearTimeout(timeout);
  timeout = setTimeout(cycleSlides, 5000);
}
