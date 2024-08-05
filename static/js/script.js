let prevScrollPos = window.scrollY;

window.onscroll = function() {
  let currentScrollPos = window.scrollY;
  let signin = document.getElementById("sign_in");
  let logout = document.getElementById("sign-out-btn")
  let navbar = document.getElementById("container");
  let logo = document.getElementById("logo_text");
  let bar1 = document.getElementById("bar1")
  let bar2 = document.getElementById("bar2")
  let bar3 = document.getElementById("bar3")
  let wishlist = document.getElementById("wishlist");






  if (currentScrollPos==0) {
    navbar.style.top = "0";
    navbar.style.backgroundColor = 'transparent';
    logo.style.color = 'white'
    wishlist.style.color = 'white';
    document.getElementById("bag").style.color="white";
    

    document.getElementById("profile-btn").style.color = "white";
    if (signin !==null){
      signin.style.color="white";

    }
   
    if (logout !==null){
      logout.style.color="white";

    }
    document.getElementById("search-btn").style.color="white";
    bar1.style.backgroundColor="white";
    bar2.style.backgroundColor="white";
    bar3.style.backgroundColor="white";

    
    
    


  } else {
    
    navbar.style.backgroundColor = '#f3f4f9';
    logo.style.color = 'black';

    navbar.style.transition = '0.5s';
    wishlist.style.color = 'black';
    document.getElementById("search-btn").style.color="black";

    document.getElementById("bag").style.color="black";
    document.getElementById("profile-btn").style.color = "black";

    if (signin !==null){
      signin.style.color="black";

    }
    if (logout !==null){
      logout.style.color="black";



    }

    bar1.style.backgroundColor="black";
    bar2.style.backgroundColor="black";
    bar3.style.backgroundColor="black";
    
    

     // Adjust this value to hide the navbar completely
  }

  prevScrollPos = currentScrollPos;
}

