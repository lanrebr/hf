var canvas = document.getElementById("scenario");
var ctx = canvas.getContext("2d");
var width = canvas.width;
var height = canvas.height;
ctx.lineWidth = 1;
var socket = io()
socket.on('connect', function(){
    console.log("connected")
})
function connect(file){
    msg={"file":file}
    var sim= {}
    socket.emit("simulate", msg)
    socket.on('init', function(msg) {
        console.log("init ",msg)
        sim = msg
    });
    socket.on('update', function(msg) {
        var zoom = sim.parameters.zoom
        //console.log("message ",msg)
        //clear
        ctx.save();
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.clearRect(0, 0, width, height);
        ctx.restore();
        //redraw
        draw(sim.tanks[0],msg.ax,zoom);
        draw(sim.tanks[1],msg.bx,zoom);
        draw(sim.tanks[2],msg.cx,zoom);
        draw(sim.tanks[3],msg.dx,zoom);
    });
}

function level(tank, x, s){

    //clear(tank)

    z=20*s
    px0 = tank.positionx*z
    py0 = tank.positiony*z

    ctx.beginPath();

    py = py0 - x*z
    tank.py = py

    inpipe = tank.pipeheight - x >= 0
    px = px0
    if (inpipe){
        px = px0 + (tank.tankdiameter/2 - tank.pipediameter/2)*z
    }
    tank.fpx = px

    px = px0 + (tank.tankdiameter)*z
    if (inpipe){
        px = px0 + (tank.tankdiameter/2 + tank.pipediameter/2)*z
        console.log("reduced")
    }
    tank.tpx = px

    ctx.moveTo(tank.fpx,tank.py);
    ctx.lineTo(tank.tpx,tank.py);
    ctx.strokeStyle ='#0000ff';
    ctx.stroke();
}

function draw(tank, x, s){
    z=20*s
    px0 = tank.positionx*z
    py0 = tank.positiony*z

    ctx.beginPath();

    px = px0
    py = py0 - (tank.pipeheight+tank.tankheight)*z
    ctx.moveTo(px,py);

    py = py0 - (tank.pipeheight)*z
    ctx.lineTo(px, py);

    px = px0 + (tank.tankdiameter/2 - tank.pipediameter/2)*z
    ctx.lineTo(px, py);

    py = py0
    ctx.lineTo(px, py);

    px = px0 + (tank.tankdiameter)*z
    py = py0 - (tank.pipeheight+tank.tankheight)*z
    ctx.moveTo(px,py);

    py = py0 - (tank.pipeheight)*z
    ctx.lineTo(px, py);

    px = px0 + (tank.tankdiameter/2 + tank.pipediameter/2)*z
    ctx.lineTo(px, py);

    py = py0
    ctx.lineTo(px, py);

    ctx.strokeStyle = '#000000';
    ctx.stroke();

    level(tank, x, s)
} 

