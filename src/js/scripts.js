import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

let scene, camera, renderer, orbit;
let cubes = [];  // Array untuk menyimpan objek cube

async function fetchIterationData() {
    const response = await fetch('http://127.0.0.1:5000/get-iteration-data');
    const data = await response.json();
    displayChart(data);  // Panggil fungsi untuk menampilkan chart
}

function displayChart(data) {
    const ctx = document.getElementById('objectiveChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({ length: data.length }, (_, i) => i + 1),
            datasets: [{
                label: 'Objective Function Value',
                data: data,
                fill: false,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { display: true, title: { display: true, text: 'Iteration' } },
                y: { display: true, title: { display: true, text: 'Objective Function Value' } }
            }
        }
    });
}


async function fetchStuckLocalOptima() {
    const response = await fetch('http://127.0.0.1:5000/get-stuck-local-optima');
    const data = await response.json();
    document.getElementById('stuckLocalOptimaCount').innerText = `Stuck di Local Optima: ${data}`;
}

// Fungsi untuk membuat tekstur dengan angka di dalamnya
function createTexture(number) {
    const canvas = document.createElement('canvas');
    canvas.width = 1024;
    canvas.height = 1024;
    const context = canvas.getContext('2d');

    context.fillStyle = 'white';
    context.fillRect(0, 0, 1024, 1024);
    context.fillStyle = 'black';
    context.font = '480px Arial';
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    context.fillText(number, 512, 512);

    const texture = new THREE.CanvasTexture(canvas);
    texture.minFilter = THREE.LinearFilter; // Mengurangi pikselasi pada tekstur
    texture.magFilter = THREE.LinearFilter;
    texture.anisotropy = renderer.capabilities.getMaxAnisotropy();

    return texture;
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

                // Buat tekstur untuk angka
                const cubeNumTexture = createTexture(unique);

                // Beri warna acak untuk setiap kubus
                const randomColor = new THREE.Color(Math.random(), Math.random(), Math.random());
                const cubeNumMaterial = new THREE.MeshBasicMaterial({ 
                    map: cubeNumTexture, 
                    color: randomColor  // Warna acak
                });

                const cube = new THREE.Mesh(cubeGeometry, cubeNumMaterial);
                cube.position.set(x * offset, y * offset, z * offset);
                
                scene.add(cube);
                cubes.push(cube);
            }
        }
    }
}


// Fungsi untuk menambahkan star field (bidang bintang)
function addStarField() {
    const starGeometry = new THREE.BufferGeometry();
    const starMaterial = new THREE.PointsMaterial({ color: 0xffffff });
    
    const starVertices = [];
    for (let i = 0; i < 1000; i++) {
        const x = THREE.MathUtils.randFloatSpread(200); // Sebaran acak dari -100 ke 100
        const y = THREE.MathUtils.randFloatSpread(200);
        const z = THREE.MathUtils.randFloatSpread(200);
        starVertices.push(x, y, z);
    }

    starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));

    const stars = new THREE.Points(starGeometry, starMaterial);
    scene.add(stars);
}


// Inisialisasi Three.js
function init() {
    // Setup renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);  // Menambahkan devicePixelRatio untuk kualitas lebih tinggi
    document.body.appendChild(renderer.domElement);

    // Setup scene
    scene = new THREE.Scene();
    // scene.background = new THREE.Color(0x537C76);

    // Setup camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(10, 10, 10);

    // Tambahkan axes helper
    const axeshelper = new THREE.AxesHelper(5);
    scene.add(axeshelper);

    // Setup orbit controls
    orbit = new OrbitControls(camera, renderer.domElement);

    // Star Background
    addStarField();

    // Event listener untuk tombol Start dan Okay
    document.getElementById("startButton").addEventListener("click", startAlgorithm);
    document.getElementById("okayButton").addEventListener("click", async () => {
        await sendOkay();
        await fetchIterationData();
        await fetchStuckLocalOptima();
    });
    animate();
}

// Fungsi animasi
function animate() {
    requestAnimationFrame(animate);
    orbit.update();
    renderer.render(scene, camera);
}

init();
