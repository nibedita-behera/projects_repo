console.log('register js is working')
const userNameField=document.querySelector('#userName')
const feedbackField=document.querySelector(".invalid-feedback")
const successmsg=document.querySelector(".success-username")
const emailField= document.querySelector('#emailField')
const emailInvalid= document.querySelector('.invalid-emailmsg')
const showPasswordToggle= document.querySelector('.showPasswordToggle')
const passwordField= document.querySelector('#passwordField')
const submitBtn=document.querySelector("#submit-btn")
const handleToggleInput=(e)=>{
  if(showPasswordToggle.textContent=='Show'){
      showPasswordToggle.textContent="Hide"
      passwordField.setAttribute("type",'text')
  }else{
     showPasswordToggle.textContent="Show"
     passwordField.setAttribute("type",'password')
  }
   
}
     
submitBtn.style.disabled=true
showPasswordToggle.addEventListener("click",handleToggleInput)
emailField.addEventListener("keyup",(e)=>{
    console.log('8888',888)
    const emailValue=e.target.value
    emailField.classList.remove("is-invalid")
    emailInvalid.style.display='none'
    
    if(emailValue.length > 0){
        fetch("http://127.0.0.1:8000/authentication/validate-email",{
        body:JSON.stringify({email:emailValue}),
        method:"POST"
      }).then(res=>res.json()).then(data=>{
        console.log('data',data)
        if(data.email_error){
            console.log('error')
            submitBtn.style.disabled=true
            emailField.classList.add("is-invalid")
            emailInvalid.style.display='block'
            emailInvalid.innerHTML=`<p>${data.email_error}</p>`
        }else{
          submitBtn.style.disabled=false
        }
      })
    }

    
})
userNameField.addEventListener("keyup",(e)=>{
    console.log('77777',888)
    const usernameval=e.target.value

      userNameField.classList.remove("is-invalid")
      feedbackField.style.display='none'
      successmsg.textContent=`Checking ${usernameval}`
      successmsg.style.display='block'
    
    
    if(usernameval.length>0){
        fetch("http://127.0.0.1:8000/authentication/validate-username",{
        body:JSON.stringify({username:usernameval}),
        method:"POST"
      }).then(res=>res.json()).then(data=>{
        console.log('data',data)
        successmsg.style.display='none'
        if(data.username_error){
            console.log('error')
            submitBtn.disabled=true;
            userNameField.classList.add("is-invalid")            
            feedbackField.style.display='block'
            feedbackField.innerHTML=`<p>${data.username_error}</p>`
        }else{
          submitBtn.removeAttribute('disabled')
        }
      })
    }

    
})  