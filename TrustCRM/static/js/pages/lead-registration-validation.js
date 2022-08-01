function check_status(){
    var check=document.getElementById("email_unav")
    if(check.checked){
        $('#email1').attr('readonly', true);
        $('#email2').attr('readonly', true);
    }
    else{
        $('#email1').attr('readonly', false);
        $('#email2').attr('readonly', false);
    }
    
    console.log(check)
}
function lead_regn_validation(){
    console.log("lead registration")
    var mailformat = /^\w+([\.-]?\w+)*[@gmail.com]*(\.\w{2,3})+$/;
    var email1=document.getElementById("email1").value
    var email2=document.getElementById("email2").value
    var mobile=document.getElementById("mobile").value
    var age=document.getElementById("age").value
    if(age<18){
        console.log("age ")
        $("#age").prop('required',true);
        //return false
        
    
    }
    
    if(email1 || email2){
        console.log("email present")
        //return true;
    }else if(!email1 && !email2){
        console.log(mobile)
        console.log(mobile.val)
        if(mobile){
            var len=mobile.value
            console.log("email not present")
            console.log("mobile present")
            console.log(len)
            if(len!=undefined){
                console.log(len.length)
                if(len.length!=10){
                    console.log("mobile valid")
                    $("#mobile").prop('required',true);
                }

            }
            
            
        }
        else{
            console.log("email not present")
            console.log("mobile not present")
            $("#mobile").prop('required',true);
            document.getElementById("email_unav").required = true;
        }
        
    }
    

    

}