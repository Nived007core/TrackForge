const avatar =document.getElementById("profileAvatar");
const dropdown=document.getElementById("dropdownmenu");
avatar.addEventListener("click",function(){
    if (dropdown.style.display==="block"){
        dropdown.style.display="none";
    } else{
        dropdown.style.display="block";
    }
});