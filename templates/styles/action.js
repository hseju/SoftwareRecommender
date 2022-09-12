document.addEventListener("DOMContentLoaded", function(){
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(element){
        return new bootstrap.Tooltip(element);
    });
});



function validateForm() {
    console.log("In validate")
    var name =  document.getElementById('name').value;
    if (name == "") {
        document.querySelector('.status').innerHTML = "Name cannot be empty";
        return false;
    }
    var email =  document.getElementById('email').value;
    if (email == "") {
        document.querySelector('.status').innerHTML = "Email cannot be empty";
        return false;
    } else {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if(!re.test(email)){
            document.querySelector('.status').innerHTML = "Email format invalid";
            return false;
        }
    }
    var subject =  document.getElementById('subject').value;
    if (subject == "") {
        document.querySelector('.status').innerHTML = "Subject cannot be empty";
        return false;
    }
    var message =  document.getElementById('message').value;
    if (message == "") {
        document.querySelector('.status').innerHTML = "Message cannot be empty";
        return false;
    }
    document.querySelector('.status').innerHTML = "Sending...";
  }


$('.selectpicker').selectpicker({
    liveSearch:true,
    showTick:false
});

$(document).on('click', '.dropdown-menu li', function(event){
    if($(this).hasClass('active')){
  $(this).parent().prev('div').parent().next('select').selectpicker('val',''); } 
});

$(document).bind("keyup",".dropdown-menu li", function(e){
    var activeIndex = $(".dropdown-menu li.active").data('original-index');
    var selectedIndex = $(".dropdown-menu li.selected").data('original-index');
    if(e.which == 13){
       if(selectedIndex == activeIndex){
          $(".dropdown-menu li.active").find("a").trigger('click');
       
       } else {
          $(".dropdown-menu li.active").removeClass('active').find("a").trigger('click'); 
       }
    }
});