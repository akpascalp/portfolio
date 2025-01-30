<script setup>
import { onMounted, ref, watch, onUnmounted } from "vue";
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import axios from 'axios';

const params = ref({ S0: 0.99, I0: 0.01, beta: 0.3, gamma: 0.1 });
let scene, camera, renderer, controls;
const spheres = [];
let interval = null;
const currentDay = ref(0);
const colors = {
    susceptible: 0xa3c8ff,
    infected: 0xffa07a,
    recovered: 0x21a645
};

const hexToCssColor = (hex) => {
    return `#${hex.toString(16).padStart(6, '0')}`;
};

const capitalize = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
};

const fetchSimulation = async () => {
    const response = await axios.get('http://127.0.0.1:8000/step');
    currentDay.value = response.data.day;
    updateScene(response.data);
};

const updateScene = (data) => {
    // Vérifie si le nombre de sphères est suffisant avant de les manipuler
    if (spheres.length !== data.positions.length) {
        // Si les sphères n'ont pas été créées ou si le nombre a changé, recréer les sphères
        spheres.forEach((sphere) => scene.remove(sphere)); // Enlever les anciennes sphères
        spheres.length = 0; // Réinitialiser le tableau de sphères

        // Créer les sphères avec les nouvelles positions et états
        data.positions.forEach((pos, i) => {
            const color = data.states[i] === 'S' ? colors.susceptible : data.states[i] === 'I' ? colors.infected : colors.recovered; // Vert menthe pour "R"

            const geometry = new THREE.SphereGeometry(1);
            const material = new THREE.MeshStandardMaterial({ color });
            const sphere = new THREE.Mesh(geometry, material);
            sphere.position.set(...pos);
            scene.add(sphere);
            spheres.push(sphere);
        });
    } else {
        // Si les sphères existent déjà, effectuer une transition fluide
        data.positions.forEach((pos, i) => {
            const sphere = spheres[i];
            const targetColor = data.states[i] === 'S' ? colors.susceptible : data.states[i] === 'I' ? colors.infected : colors.recovered;

            // Transition fluide de la position
            new THREE.Vector3(...pos).lerp(sphere.position, 0.1);

            // Transition fluide de la couleur
            const currentColor = sphere.material.color;
            currentColor.lerp(new THREE.Color(targetColor), 1);
        });
    }

    // Vérifier si la propagation est terminée
    const allRecovered = data.states.every((state) => state === 'R');
    if (allRecovered) {
        // Arrêter les requêtes périodiques
        clearInterval(interval);
        console.log('Propagation terminée, les requêtes sont arrêtées.');
    }
};

onMounted(() => {
    const container = document.getElementById('graphSimulation');
    if (!container) return;

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, container.clientWidth / 300, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, 300);
    renderer.setClearColor(new THREE.Color(0xf5f5f5));
    container.innerHTML = '';
    container.appendChild(renderer.domElement);

    const light = new THREE.AmbientLight(0xffffff);
    scene.add(light);

    // Caméra éloignée pour mieux voir les points
    camera.position.z = 130;

    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.screenSpacePanning = false;
    controls.minDistance = 10;
    controls.maxDistance = 500; // Permet un meilleur zoom arrière

    // Animation
    const animate = () => {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    };
    animate();

    axios.get('http://127.0.0.1:8000/start', { params: params.value }).then(() => {
        interval = setInterval(fetchSimulation, 500);
    });
});

onUnmounted(() => {
    if (interval) clearInterval(interval);
});

const startSimulation = () => {
    if (interval) return;
    interval = setInterval(fetchSimulation, 500);
};

const pauseSimulation = () => {
    clearInterval(interval);
    interval = null;
};

const resetSimulation = () => {
    clearInterval(interval);
    interval = null;
    currentDay.value = 0;
};

watch(
    params,
    () => {
        axios.get('http://127.0.0.1:8000/start', { params: params.value });
    },
    { deep: true }
);
</script>

<template>
    <Card>
        <template #header>
            <div class="flex justify-between mt-4 mx-4">
                <h1>Simulation</h1>
                <div>Jour {{ currentDay }}</div>
            </div>
        </template>
        <template #content>
            <div class="flex justify-between">
                <div class="flex flex-wrap gap-2">
                    <IftaLabel v-for="(value, key) in params" :key="key">
                        <InputNumber v-model="params[key]" :step="0.01" style="width: 4rem" fluid />
                        <label>{{ key }}</label>
                    </IftaLabel>
                </div>
                <div class="grid grid-cols-3 gap-2 content-center">
                    <Button @click="startSimulation" icon="pi pi-play-circle"></Button>
                    <Button @click="pauseSimulation" icon="pi pi-pause-circle"></Button>
                    <Button @click="resetSimulation" icon="pi pi-fast-backward"></Button>
                </div>
            </div>
            <div id="graphSimulation" style="width: 100%; height: 300px" class="mt-4"></div>
            <div class="flex gap-1 mt-4">
                <Tag v-for="(color, key) in colors" :key="key" icon="pi pi-circle-fill" :style="{ backgroundColor: '#f5f5f5', color: hexToCssColor(color) }">
                    {{ capitalize(key) }}
                </Tag>
            </div>
        </template>
    </Card>
</template>
