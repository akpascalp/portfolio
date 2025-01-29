<script setup>
import { onMounted } from 'vue';
import SpriteText from 'https://esm.sh/three-spritetext';

const technologies = {
    Python: {
        GUI: ['PyQt'],
        Web: ['Flask', 'Django', 'FastAPI'],
        'Data Science': ['Keras', 'Tensorflow']
    },
    JavaScript: {
        frontend: ['Vue.js'],
        '3D': ['Three.js']
    },
    Database: {
        SQL: ['MySQL'],
        NoSQL: ['MongoDB']
    },
    PHP: {
        backend: ['Laravel']
    },
    'REST API': {
        tools: ['Postman']
    },
    'CI/CD': ['Docker', 'Git', 'Jenkins']
};

const createGraph = () => {
    const graphData = {
        nodes: [{ id: '', group: -1 }],
        links: []
    };

    const addNodesAndLinks = (parent, obj, group) => {
        Object.keys(obj).forEach((key, index) => {
            const currentGroup = group === 0 ? index - 1 : group;
            graphData.nodes.push({ id: key, group: currentGroup });
            graphData.links.push({ source: parent, target: key });
            if (typeof obj[key] === 'object' && !Array.isArray(obj[key])) {
                addNodesAndLinks(key, obj[key], currentGroup);
            } else if (Array.isArray(obj[key])) {
                obj[key].forEach((subKey) => {
                    graphData.nodes.push({ id: subKey, group: currentGroup });
                    graphData.links.push({ source: key, target: subKey });
                });
            }
        });
    };

    addNodesAndLinks('', technologies, 0);

    // eslint-disable-next-line no-undef
    const Graph = ForceGraph3D()(document.getElementById('graph'))
        .graphData(graphData)
        .nodeAutoColorBy('group')
        .linkDirectionalParticles(2)
        .linkDirectionalParticleSpeed(0.01)
        .linkOpacity(0.2)
        .linkWidth(1.5)
        .nodeThreeObject((node) => {
            const sprite = new SpriteText(node.id);
            sprite.material.depthWrite = false; // make sprite background transparent
            sprite.color = node.color;
            sprite.textHeight = 16;
            return sprite;
        })
        .backgroundColor('#f0f0f0')
        .showNavInfo(false)
        .linkAutoColorBy('type')
        .linkColor(() => 'rgb(0, 0, 0)')
        .width(360)
        .height(310);

    // Spread nodes a little wider
    Graph.d3Force('charge').strength(-200);
};

onMounted(() => {
    createGraph();
});
</script>

<template>
    <Card>
        <template #header>
            <div class="flex justify-center text-xl mt-6">Technologies</div>
        </template>
        <template #content>
            <div class="flex justify-center">
                <div id="graph"></div>
            </div>
        </template>
    </Card>
</template>
