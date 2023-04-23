var msg = document.querySelector(".msg");
var client_connect = [];
msg.value = "";
var state = false;
var state_option = false;
var sound = document.querySelector(".notify")
var send = document.querySelector(".send");
var menu = document.querySelectorAll(".menu a");
var option = document.querySelector(".option");
var form = document.querySelector(".form");
var href = window.location.origin;
var socketio = io.connect(href);
var username = new String(document.querySelector(".username").textContent).trim();
var photo_profile = document.querySelector(".photo_profile");
var msgZone = document.querySelector(".msgzone");
function sendMessage(msg){
    createMsgBox(username,new Date().getDay()+" "+new Date().getHours()+":"+new Date().getMinutes(),msg,"emiter");
    socketio.emit('message',{'msg':msg});
}
/* socketio event */
socketio.on('connect',function(){
    state = true;
})
socketio.on('client_connect',function(data){

})
socketio.on("client_disconnect",function(data){

})
socketio.on('new_message',function(data){
    data = data;
    console.log(data)
    if(data.username != username){
        createMsgBox(data.username,data.date,data.msg,"reciver");
        sound.play();
    }
})
socketio.on('new_client',function(){

})
/* send message event */
send.addEventListener("click",function(){
    var message = msg.value;
    sendMessage(message);
    msg.value = "";
    
})
/* key event */
window.addEventListener("keydown",function(e){
    if(e.key == "Enter"){
        e.preventDefault();
        sendMessage(msg.value);
        msg.value = "";
    }
})
/* menu event */
for(var i=0;i<menu.length;i++){
    menu[i].addEventListener("click",function(ev){
        if(this.getAttribute("title") == "menu"){
            if(document.body.clientWidth > 799){
                if(!option.classList.contains("hidden")){
                    option.classList.add("hidden");
                    form.classList.add("max");
                    msgZone.classList.add("max")
                }else{
                    option.classList.remove("hidden")
                    form.classList.remove("max");
                    msgZone.classList.remove("max")
                }
            }
            if(document.body.clientWidth < 799){
                if(option.classList.contains("all") == false){
                    option.classList.add("all");
                    form.classList.add("none");
                }else{
                    option.classList.remove("all");
                    form.classList.remove("none");
                }
            }
        }
        if(this.getAttribute("title") == "discussion"){
            console.log(this)
        }
    })
}
/* other function */
function extension_verification(extension_pattern,file){
    return extension_pattern;
}
function createMsgBox(username,date,msg,type){
    var msgBox = document.createElement("div");
    msgBox.classList.add("msgbox");
    if(type == "emiter"){
        msgBox.classList.add("emiter");
    }
    if(type == "reciver"){
        msgBox.classList.add("reciver");
    }
    var username_msg = document.createElement("span");
    username_msg.classList.add("username_msg");
    var date_msg = document.createElement("span");
    var p = document.createElement("p")
    date_msg.classList.add("date_msg");
    username_msg.innerHTML = username;
    date_msg.textContent = date;
    p.innerHTML = msg;
    msgBox.appendChild(username_msg);
    msgBox.appendChild(p);
    msgBox.appendChild(date_msg);
    msgZone.appendChild(msgBox);
}
function createSound(){
    navigator.getUserMedia({
        audio:true
    },function(stream){
        var media = new MediaRecorder(stream)
        console.log(media)
    },function(err){
        console.log(err)
    })
}
/* event profile  */
photo_profile.addEventListener("change",function(){
    var fic = photo_profile.files[0];
    if(new String(fic.type).startsWith("image") == true){
        socketio.emit("photo_profile",{"data":fic});
    }
})