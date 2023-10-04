UsernameField = document.getElementById('username');
UsernameFeedback = document.getElementById('invalid-username');
EmailField = document.getElementById('email');
EmailFeedback = document.getElementById('invalid-email');
PassField = document.getElementById('password');
PassFeedback = document.getElementById('invalid-password');
RepassField = document.getElementById('repass');
RepassFeedback = document.getElementById('invalid-repass');
passwordToggle = document.querySelector('.password-toggle');
button = document.getElementById('Register-Button');
form = document.getElementById("myForm");



passwordToggle.addEventListener('click', function () {
    const type = PassField.getAttribute('type') === 'password' ? 'text' : 'password';
    PassField.setAttribute('type', type);
    this.classList.toggle('fa-eye-slash');
    
});

UsernameField.addEventListener('keyup',(e)=>{
    usernameVal =e.target.value;
    UsernameField.classList.remove("is-invalid");
    UsernameFeedback.style.display="none";
    if(usernameVal.length>0){
        fetch("/auth/validate_username/",{
            body : JSON.stringify({username:usernameVal}) ,
            method : 'post'
        })
        .then(res => res.json())
        .then(data =>{
            if (data.username_error)
            {
                UsernameField.classList.add("is-invalid");
                UsernameFeedback.innerHTML='<p>' + data.username_error + '</p>';
                UsernameFeedback.style.display="block";
             
            }
         
            
        })
        
    }
    

});

EmailField.addEventListener('keyup',(e)=>{
    Emailval =e.target.value;
    EmailField.classList.remove("is-invalid");
    EmailFeedback.style.display="none";
    if(usernameVal.length>0){
        fetch("/auth/validate_email/",{
            body : JSON.stringify({email:Emailval}) ,
            method : 'post'
        })
        .then(res => res.json())
        .then(data =>{
            if (data.email_error)
            {
                EmailField.classList.add("is-invalid");
                EmailFeedback.innerHTML='<p>' + data.email_error + '</p>';
                EmailFeedback.style.display="block";
        
            }
     
        })
        
    }
    

});

PassField.addEventListener('keyup',(e)=>{
    Passval =e.target.value;
    PassField.classList.remove("is-invalid");
    PassFeedback.style.display="none";
    if(usernameVal.length>0){
        fetch("/auth/validate_pass/",{
            body : JSON.stringify({password:Passval}) ,
            method : 'post'
        })
        .then(res => res.json())
        .then(data =>{
            if (data.pass_error)
            {
                PassField.classList.add("is-invalid");
                PassFeedback.innerHTML='<p>' + data.pass_error + '</p>';
                PassFeedback.style.display="block";
            }
            
        })
        
    }
    

});

RepassField.addEventListener('keyup',(e)=>{
    RePassval =e.target.value;
    Passval= PassField.value;
    RepassField.classList.remove("is-invalid");
    RepassFeedback.style.display="none";
    if(RePassval.length>0){
        fetch("/auth/validate_repass/",{
            body : JSON.stringify({
                password:Passval,
                re_password:RePassval
            }) ,
            method : 'post'
        })
        .then(res => res.json())
        .then(data =>{
            if (data.password_error)
            {
                RepassField.classList.add("is-invalid");
                RepassFeedback.innerHTML='<p>' + data.password_error + '</p>';
                RepassFeedback.style.display="block";
                button.disabled =true;
            }
            else{
                button.disabled =false;
            }
        })
        
    }
    

});

form.addEventListener("input", function() {
    var hasErrors = false;
    var hasEmptyFields = false;
    var inputs = form.querySelectorAll("input");

inputs.forEach(function(input) {
    if (input.classList.contains("is-invalid") ) {
      hasErrors = true;
      console.log(hasErrors)
    }
    if (input.value.trim() === "")
    {
        hasEmptyFields = true
    }
    var lastInput = inputs[inputs.length - 1];
    if (lastInput.classList.contains("is-invalid") || lastInput.value.trim() === "") {
      hasErrors = true;
      hasEmptyFields = true;
    }

  });

  if (hasErrors || hasEmptyFields) {
    button.disabled = true;
  } else {
    console.log(hasErrors)
    button.disabled = false;
  }
});