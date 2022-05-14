function reveal() {
    var logo = document.getElementById('logo')
    var navList = document.getElementById('navList')
    var airplane = document.getElementById('airplane')
    
    var windowHeight = window.pageYOffset;

    // this animates the navbar
      if (windowHeight > 100 ) {
        logo.classList.add("active");
        navList.classList.add("increasePadding");
        airplane.classList.add("changePosition");
      } else {
        logo.classList.remove("active");
        navList.classList.remove("increasePadding");
      }

      if (windowHeight < 180) {
        airplane.classList.add("changePosition");
      } else {
        airplane.classList.remove("changePosition");
      }
        console.log(screen.width)
  }
  
window.addEventListener("scroll", reveal);


document.addEventListener("DOMContentLoaded", function(event) { 
  var bars = document.getElementById('bars')
  var navOptions = document.getElementById('navOptions')
  var xmark = document.getElementById('xmark')
 

  bars.addEventListener('click',function(){
  //we ready baby
    navOptions.classList.toggle("slidein");
    xmark.classList.toggle("show");
    bars.classList.toggle("noshow");
    if(screen.width <= 1024){
      var coll = document.getElementsByClassName("dropdown");
      var i;
      console.log(coll)
      for (i = 0; i < coll.length; i++) {
        console.log(i)
        coll[i].addEventListener("click", function() {
          
          var content = this.lastElementChild;
          console.log(content)
          if (content.style.display === "block") {
            content.style.display = "none";
          } else {
            content.style.display = "block";
          }
        });
      }
    }
  })


  xmark.addEventListener('click',function(){
    navOptions.classList.toggle("slidein");
    bars.classList.toggle("noshow");
    xmark.classList.toggle("show");
  })

});







  