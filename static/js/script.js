let prevScrollPos = window.scrollY;

window.onscroll = function() {
  let currentScrollPos = window.scrollY;
  let navbar = document.getElementById("container");

  if (prevScrollPos > currentScrollPos) {
    navbar.style.top = "0";
  } else {
    navbar.style.top = "-95px"; // Adjust this value to hide the navbar completely
  }

  prevScrollPos = currentScrollPos;
}

