<script setup>
import { onMounted, ref, watch, onUnmounted, computed } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import axios from 'axios';

const paramsInit = { S: 0.99, I: 0.01, R: null, beta: 0.3, gamma: 0.1, day: 0, population: 1000 };
const params = ref({ ...paramsInit });
let scene, camera, renderer, controls;
const spheres = [];
const interval = ref(null);
const colors = {
    susceptible: 0xa3c8ff,
    infected: 0xffa07a,
    recovered: 0x21a645
};
const isRunning = computed(() => {
    return interval.value !== null;
});

const hexToCssColor = (hex) => {
    return `#${hex.toString(16).padStart(6, '0')}`;
};

const capitalize = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
};

const fetchSimulation = async () => {
    console.log(params.value);
    const response = await axios.get('http://127.0.0.1:8000/sir', { params: params.value });
    params.value = response.data;
    updateScene();
};

const calculateSpherePositions = (states) => {
    const positions = [];
    const radius = 75;
    const numPoints = states.length;

    for (let i = 0; i < numPoints; i++) {
        let r = radius * Math.cbrt(Math.random());
        let theta = Math.random() * 2 * Math.PI;
        let phi = Math.acos(2 * Math.random() - 1);

        if (states[i] === 'I') {
            r *= 0.1;
        }

        const x = r * Math.sin(phi) * Math.cos(theta);
        const y = r * Math.sin(phi) * Math.sin(theta);
        const z = r * Math.cos(phi);

        positions.push([x, y, z]);
    }

    return positions;
};

const updateScene = () => {
    const totalPopulation = params.value.population;
    const numInfected = Math.max(0, Math.round(params.value.I * totalPopulation));
    const numRecovered = Math.max(0, Math.round(params.value.R * totalPopulation));
    const numSusceptible = Math.max(0, totalPopulation - numInfected - numRecovered);

    const states = [...Array(numInfected).fill('I'), ...Array(numRecovered).fill('R'), ...Array(numSusceptible).fill('S')];

    const positions = calculateSpherePositions(states);

    if (spheres.length !== positions.length) {
        spheres.forEach((sphere) => scene.remove(sphere));
        spheres.length = 0;

        positions.forEach((pos, i) => {
            const color = states[i] === 'S' ? colors.susceptible : states[i] === 'I' ? colors.infected : colors.recovered;

            const geometry = new THREE.SphereGeometry(1);
            const material = new THREE.MeshStandardMaterial({ color });
            const sphere = new THREE.Mesh(geometry, material);
            sphere.position.set(...pos);
            scene.add(sphere);
            spheres.push(sphere);
        });
    } else {
        positions.forEach((pos, i) => {
            const sphere = spheres[i];
            const targetColor = states[i] === 'S' ? colors.susceptible : states[i] === 'I' ? colors.infected : colors.recovered;

            new THREE.Vector3(...pos).lerp(sphere.position, 0.1);

            const currentColor = sphere.material.color;
            currentColor.lerp(new THREE.Color(targetColor), 1);
        });
    }

    const noInfected = states.every((state) => state !== 'I');
    if (noInfected) {
        clearInterval(interval.value);
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

    camera.position.z = 130;

    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.screenSpacePanning = false;
    controls.minDistance = 10;
    controls.maxDistance = 500; // improve zoom back

    const animate = () => {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    };
    animate();

    axios.get('http://127.0.0.1:8000/sir', { params: params.value }).then(() => {
        interval.value = setInterval(fetchSimulation, 500);
    });
});

onUnmounted(() => {
    if (interval.value) clearInterval(interval.value);
});

const startSimulation = () => {
    if (interval.value) return;
    interval.value = setInterval(fetchSimulation, 500);
};

const pauseSimulation = () => {
    clearInterval(interval.value);
    interval.value = null;
};

const resetSimulation = () => {
    clearInterval(interval.value);
    interval.value = null;
    params.value = { ...paramsInit };
};

watch(
    params,
    () => {
        axios.get('http://127.0.0.1:8000/sir', { params: params.value });
    },
    { deep: true }
);
</script>

<template>
    <Card>
        <template #header>
            <div class="flex justify-between mt-4 mx-4">
                <h1>Simulation</h1>
                <div>Jour {{ params.day }}</div>
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
                    <Button @click="startSimulation" icon="pi pi-play-circle" :disabled="isRunning"></Button>
                    <Button @click="pauseSimulation" icon="pi pi-pause-circle" :disabled="!isRunning"></Button>
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
