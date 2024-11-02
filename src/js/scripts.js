import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/Addons.js';


// function to create texture with a number inside it
function createTexture(number) {
    const canvas = document.createElement('canvas');
    canvas.width = 64;
    canvas.height = 64;
    const context = canvas.getContext('2d');

    context.fillStyle = 'white';
    context.fillRect(0, 0, 64, 64);
    context.fillStyle = 'black';
    context.font = 'Arial 60px bold';
    context.textAlign = 'center';
    context.textBaseline = 'middle'
    context.fillText(number, 32, 32);

    return new THREE.CanvasTexture(canvas);

}

// function to shuffle an array of numbers
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (1 + i));
        [array[i], array[j]] = [array[i], array[j]];
    }
    return array;
}

// array from 1 - 125
let nums = [...Array(125).keys()].map(x => x + 1);
console.log(nums);
// nums = shuffleArray(nums);


// adding the rederer
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// adding the scene
const scene = new THREE.Scene();

// adding the camera
const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
)

// adding axes helper
const axeshelper = new THREE.AxesHelper(5);
scene.add(axeshelper);

// adding orbit
const orbit = new OrbitControls(camera, renderer.domElement);


// set camera position
camera.position.set(10,10,10);

// texture loader
const textureLoader = new THREE.TextureLoader();

// make cube geometry and cube material
const cubeGeometry = new THREE.BoxGeometry();
// const cubeMaterial = new THREE.MeshBasicMaterial({color: 0x0000ff});
// const cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
//test

const offset = 1.8;
let index = 0;

for(let z = 2; z >= -2; z--) {
    for(let y = 2; y >= -2; y--) {
        for(let x = -2; x <= 2; x++) {

            const unique = nums[index];
            index++;

            const cubeNumTexture = createTexture(unique);
            const cubeNumMaterial = new THREE.MeshBasicMaterial({ map: cubeNumTexture });



            const cube = new THREE.Mesh(cubeGeometry, cubeNumMaterial);
            cube.position.set(x*offset, y*offset, z*offset);
            scene.add(cube);
        }
    }
}

// animate function
function animate() {
    requestAnimationFrame(animate);

    orbit.update();

    renderer.render(scene, camera);
}

animate();