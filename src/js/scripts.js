import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

let scene, camera, renderer, orbit;
let cubes = [];  // Array untuk menyimpan objek cube

// Fungsi untuk membuat tekstur dengan angka di dalamnya
function createTexture(number) {
    const canvas = document.createElement('canvas');
    canvas.width = 64;
    canvas.height = 64;
    const context = canvas.getContext('2d');

    context.fillStyle = 'white';
    context.fillRect(0, 0, 64, 64);
    context.fillStyle = 'black';
    context.font = '60px Arial';
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    context.fillText(number, 32, 32);

    return new THREE.CanvasTexture(canvas);
}

// Fungsi untuk memulai algoritma dan mendapatkan initial state
async function startAlgorithm() {
    const response = await fetch('http://127.0.0.1:5000/start-algorithm', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    const nums = await response.json();
    renderArray(nums);  // Render array di Three.js
}

// Fungsi untuk mengirim pesan 'okay' ke backend dan memilih algoritma
async function sendOkay() {
    const selectedAlgorithm = document.getElementById("algorithmChoice").value;
    const response = await fetch('http://127.0.0.1:5000/okay', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ algorithm: selectedAlgorithm })
    });
    const updatedNums = await response.json();
    renderArray(updatedNums);  // Render array yang diperbarui di Three.js
}

// Render array dalam Three.js
function renderArray(nums) {
    // Hapus cube yang ada sebelumnya
    cubes.forEach(cube => scene.remove(cube));
    cubes = [];

    const cubeGeometry = new THREE.BoxGeometry();
    const offset = 1.8;
    let index = 0;

    // Loop untuk membuat dan menempatkan cube sesuai array `nums`
    for (let z = 2; z >= -2; z--) { // Change loop order to z, y, x
        for (let y = 2; y >= -2; y--) {
            for (let x = -2; x <= 2; x++) {
                const unique = nums[index];
                index++;

                const cubeNumTexture = createTexture(unique);
                const cubeNumMaterial = new THREE.MeshBasicMaterial({ map: cubeNumTexture });
                const cube = new THREE.Mesh(cubeGeometry, cubeNumMaterial);

                cube.position.set(x * offset, y * offset, z * offset);
                scene.add(cube);
                cubes.push(cube);
            }
        }
    }
}

// Inisialisasi Three.js
function init() {
    // Setup renderer
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Setup scene
    scene = new THREE.Scene();

    // Setup camera
    //Adding Camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    // set camera position
    camera.position.set(10,10,10);

    // adding axes helper
    const axeshelper = new THREE.AxesHelper(5);
    scene.add(axeshelper);

    // Setup orbit controls
    orbit = new OrbitControls(camera, renderer.domElement);

    // Event listener untuk tombol Start dan Okay
    document.getElementById("startButton").addEventListener("click", startAlgorithm);
    document.getElementById("okayButton").addEventListener("click", sendOkay);

    animate();
}

// Fungsi animasi
function animate() {
    requestAnimationFrame(animate);
    orbit.update();
    renderer.render(scene, camera);
}

init();
