var canvas=document.getElementById('myCanvas');
var ctx=canvas.getContext('2d');
var contain=document.getElementById('cvsct');
var clear = document.getElementById('clear');
var send = document.getElementById('send');
var answer = document.getElementById('answer');


window.onresize = layout

function layout() {
    var wh;
    var parent = contain.parentNode;
    if(parent.offsetWidth >= parent.offsetHeight){
        contain.style.height = ''
        contain.style.width = parent.offsetHeight + 'px'
        contain.style.marginTop = ''
    }else{
        contain.style.marginTop = (parent.offsetHeight - parent.offsetWidth) * 0.5 + 'px';
        contain.style.width = parent.offsetWidth + 'px'
        contain.style.height = parent.offsetWidth + 'px'
    }
    canvas.width = contain.clientWidth;
    canvas.height = contain.clientHeight
    ctx.fillStyle='#000000';
    ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.strokeStyle = '#fff';
    top.x = canvas.offsetLeft;
    top.y = canvas.offsetTop;
}

layout()

var isdown = false;
var lastP = {};
var top = {};

window.addEventListener('touchmove',function (e) {
    if(!filter(e)) return;
    if(isdown) {
        e.preventDefault();
        ctx.lineWidth = 50
        ctx.lineCap = "round"
        ctx.lineJoin = "round";
        ctx.beginPath();
        ctx.moveTo(lastP.x - top.x, lastP.y - top.y);
        ctx.lineTo(e.touches[0].clientX - top.x, e.touches[0].clientY - top.y)
        ctx.stroke();
    }
    lastP.x = e.touches[0].clientX;
    lastP.y = e.touches[0].clientY;
},{ passive: false })

window.onmousemove = function (e) {
    if(!filter(e)) return;
    if(isdown) {
        ctx.lineWidth = 50
        ctx.lineCap = "round"
        ctx.lineJoin = "round";
        ctx.beginPath();
        ctx.moveTo(lastP.x - top.x, lastP.y - top.y);
        ctx.lineTo(e.clientX - top.x, e.clientY - top.y)
        ctx.stroke();
    }
    lastP.x = e.clientX;
    lastP.y = e.clientY;
}

window.addEventListener('touchstart', function (e) {
    if(!filter(e)) return;
    if(e.target == canvas) {
        e.preventDefault()
        isdown = true;
        lastP.x = e.touches[0].clientX;
        lastP.y = e.touches[0].clientY;
    }
},false)

window.onmousedown = function (e) {
    if(!filter(e)) return;
    if(e.target == canvas) {
        isdown = true;
    }
}


window.addEventListener('touchend',function (e) {
    if(filter(e))
        isdown = false;
},false)

window.onmouseup = function (e) {
    if(filter(e))
        isdown = false;
    if(!isdown) return;
    if(e.button === 2){
        isdown = false;
        ctx.fillRect(0,0,canvas.width,canvas.height);
    }
}

clear.onclick = function (e) {
    if(!filter(e)) return;
    ctx.fillRect(0,0,canvas.width,canvas.height);
}

send.onclick = function (e) {
    if(!filter(e)) return;
    var base64 = canvas.toDataURL('image/png',0.1)
    var req=new XMLHttpRequest();
    req.open("POST","getres",true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    base64 = base64.replace(/\+/g, "%2B");
    base64 = base64.replace(/\&/g, "%26");
    req.send('base64='+base64)
    req.onreadystatechange=function()
    {
        if (req.readyState==4 && req.status==200)
        {
            console.log(req.responseText)
            answer.innerHTML=req.responseText;
        }
    }
}


function filter(e){
    if(!e.button) {
        return true;
    }
    return false;
}


function doNothing(){
        window.event.returnValue=false;
        return false;
}