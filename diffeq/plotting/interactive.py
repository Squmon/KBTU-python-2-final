from random import randint, random
import random
import diffeq.utils.vectors as ve


template ='''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>TITLE__</title>
    <style>
        body { margin: 0; overflow: hidden; background-color: #050505; font-family: sans-serif; }
        canvas { display: block; width: 100vw; height: 100vh; }
        .info { position: absolute; top: 10px; left: 10px; color: #555; pointer-events: none; }
    </style>
</head>
<body>
<div class="info">TITLE__</div>
<canvas id="glCanvas"></canvas>

<script id="vs" type="x-shader/x-vertex">#version 300 es
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec4 aCol;

out vec4 vColor;

uniform float focus;
uniform vec2 sphere_vector;
uniform vec3 camera_position;
uniform float screenK;
uniform float time;

mat2 rotate(float a){
    return mat2(cos(a), sin(a), -sin(a), cos(a));
}

float get_t(vec3 F, vec3 P, vec3 camera_pos, float f){
    return f / (dot(F, P - camera_pos) + 0.00001);
}

void main() {
    vec3 D = vec3(0.0, 0.0, 1.0);
    vec3 X = vec3(1.0, 0.0, 0.0);
    vec3 Y = vec3(0.0, 1.0, 0.0);

    vec3 pointPos = aPos;
    pointPos.xy *= rotate(sphere_vector.x);
    pointPos.yz *= rotate(sphere_vector.y);

    float t = get_t(D, pointPos, camera_position, focus);
    vec3 L = t * (pointPos - camera_position) + camera_position;    
    vec2 screenpos = vec2(dot(L - camera_position, X), dot(L - camera_position, Y) * screenK);

    gl_Position = vec4(screenpos, 0.0, 1.0);
    
    if (dot(D, pointPos - camera_position) >= 0.0) {
        vColor = aCol;
    } else {
        vColor = vec4(0.0);
    }
}
</script>

<script id="fs" type="x-shader/x-fragment">#version 300 es
precision mediump float;
in vec4 vColor;
out vec4 FragColor;

void main(){
    FragColor = vColor;
}
</script>

<script>
    const canvas = document.querySelector("#glCanvas");
    const gl = canvas.getContext("webgl2");

    if (!gl) alert("WebGL 2 не поддерживается");

    //shaders
    function createShader(gl, type, source) {
        const shader = gl.createShader(type);
        gl.shaderSource(shader, source);
        gl.compileShader(shader);
        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
            console.error(gl.getShaderInfoLog(shader));
            gl.deleteShader(shader); return null;
        }
        return shader;
    }
    const program = gl.createProgram();
    gl.attachShader(program, createShader(gl, gl.VERTEX_SHADER, document.getElementById("vs").text.trim()));
    gl.attachShader(program, createShader(gl, gl.FRAGMENT_SHADER, document.getElementById("fs").text.trim()));
    gl.linkProgram(program);
    gl.useProgram(program);

    //data list
    let trajectores = LISTOFL;
    
    //grid
    const axisLength = 2.0;
    const negC = 0.1;

    // X
    trajectores.push([
        -axisLength*negC, 0, 0,  1.0, 0.0, 0.0, 1.0,
        axisLength, 0, 0,  1.0, 0.0, 0.0, 1.0
    ]);

    // Y
    trajectores.push([
        0, -axisLength*negC, 0,  0.0, 1.0, 0.0, 1.0,
        0,  axisLength, 0,  0.0, 1.0, 0.0, 1.0
    ]);

    // Z
    trajectores.push([
        0, 0, -axisLength*negC,  0.3, 0.3, 1.0, 1.0,
        0, 0,  axisLength,  0.3, 0.3, 1.0, 1.0
    ]);
    let renderObjects = [];

    trajectores.forEach(data => {
        const vao = gl.createVertexArray();
        gl.bindVertexArray(vao);

        const vbo = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(data), gl.STATIC_DRAW);

        let plen = 3;
        let clen = 4;
        let c = clen + plen;
        let _size = 4;

        gl.enableVertexAttribArray(0);
        gl.vertexAttribPointer(0, plen, gl.FLOAT, false, c*_size, 0);
        gl.enableVertexAttribArray(1);
        gl.vertexAttribPointer(1, clen, gl.FLOAT, false, c*_size, plen*_size);

        renderObjects.push({
            vao: vao,
            count: data.length / c
        });
        gl.bindVertexArray(null);
    });

    //uniforms
    const u = {
        focus: gl.getUniformLocation(program, "focus"),
        sphere: gl.getUniformLocation(program, "sphere_vector"),
        cam: gl.getUniformLocation(program, "camera_position"),
        screenK: gl.getUniformLocation(program, "screenK"),
        time: gl.getUniformLocation(program, "time")
    };

    let mouse = { x: 0, y: 0 };
    let lastMouse = { x: 0, y: 0 };
    let zoom = 25;
    let isMouseDown = false;

    window.onmousedown = e => {
        if (e.button === 0) {
            isMouseDown = true;
            lastMouse.x = e.clientX;
            lastMouse.y = e.clientY;
        }
    };

    window.onmouseup = e => {
        if (e.button === 0) {
            isMouseDown = false;
        }
    };

    window.onmousemove = e => {
        if (isMouseDown) {
            let dx = (e.clientX - lastMouse.x) / window.innerWidth * Math.PI * 2;
            let dy = (e.clientY - lastMouse.y) / window.innerHeight * Math.PI * 2;
            mouse.x += dx;
            mouse.y += dy;
            lastMouse.x = e.clientX;
            lastMouse.y = e.clientY;
        }
    };

    window.onwheel = e => {
        zoom *= e.deltaY < 0 ? 1 / 1.1 : 1.1;
    };

    //----------------------------
    function render(t) {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        gl.enable(gl.BLEND);
        gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
        gl.viewport(0, 0, canvas.width, canvas.height);
        gl.clear(gl.COLOR_BUFFER_BIT);

        gl.uniform1f(u.focus, 1.0);
        gl.uniform2f(u.sphere, mouse.x, mouse.y);
        gl.uniform3f(u.cam, 0, 0, -zoom);
        gl.uniform1f(u.screenK, canvas.width / canvas.height);
        gl.uniform1f(u.time, t * 0.001);

        renderObjects.forEach(obj => {
            gl.bindVertexArray(obj.vao);
            gl.drawArrays(gl.LINE_STRIP, 0, obj.count);
        });

        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);
</script>
</body>
</html>
'''

def random_color(seed):
    rng = random.Random(seed)
    return [rng.random(), rng.random(), rng.random()]

def __basic_grad(t, **kwrgs):
    return [1.0, 1.0, 1.0, t]

def basic_grad(color = None, transparent_coof = 1.0):
    Col = color
    bias = randint(0, 100)
    def f(t, i, **kwrgs):
        if Col is None:
            color = random_color(i)
        else:
            color = Col
        return color + [t*transparent_coof]
    return f

def start_end_grad(color = None, transparent_coof = 1.0):
    Col = color
    bias = randint(0, 100)
    def f(t, i, **kwrgs):
        if Col is None:
            color = random_color(i + bias)
        else:
            color = Col
        return color + [4*t*(1 - t)*transparent_coof]
    return f

def __transpose(traj, axes, color = __basic_grad, i = None):
    if i is None:
        i = randint(0, 100)
    kx, ky, kz = axes
    output = []
    Tmin = min(traj['time'])
    Tmax = max(traj['time'])
    for x, y, z, time in zip(traj[kx], traj[ky], traj[kz], traj['time']):
        t = (time - Tmin)/(Tmax - Tmin)
        output += [x, y, z] + color(t = t, x = x, y = y, z = z, i = i)

    return output


def generate_html(trajectores, axes, path = 'output.html', color = __basic_grad, title =''):
    T = [__transpose(t, axes, color) for t in trajectores]
    Q = template.replace('LISTOFL', str(T)).replace('TITLE__', title)
    with open(path, 'w') as j:
        j.write(Q)
    return Q

