<script setup>
import { ref } from 'vue';

const name = 'Pascal PHAM';
const title = 'Ingénieur logiciel Python | Vue.js';
const subTitle = 'Attaché à un code propre et bien structuré, j’aime collaborer en équipe, partager les bonnes pratiques et être à l’écoute des besoins du client pour concevoir des solutions performantes et adaptées.';
const exp = 7;
const loc = 'Région Parisienne, France | Remote';

const links = [
    {
        icon: 'pi pi-github',
        url: 'https://github.com/akpascalp/',
        text: 'akpascalp'
    },
    {
        icon: 'pi pi-linkedin',
        url: 'https://www.linkedin.com/in/anhkhoa-pascal-pham/',
        text: 'Pascal Anh-Khoa PHAM'
    }
];

const technologies = ref([
    { name: 'Python', logo: '/techno_logo/python.svg' },
    { name: 'Vue.js', logo: '/techno_logo/vuejs.svg' },
    { name: 'MongoDB', logo: '/techno_logo/mongodb.svg' },
    { name: 'API', logo: '/techno_logo/api.svg' },
    { name: 'CI/CD', logo: '/techno_logo/cicd.svg' },
    { name: 'Data Sc.', logo: '/techno_logo/datascience.svg' }
]);
</script>

<template>
    <div class="col-span-12 lg:col-span-6 xl:col-span-6">
        <Card>
            <template #content>
                <div class="grid grid-cols-2 gap-8">
                    <img alt="user header" src="/profil.jpg" />
                    <div class="flex flex-col gap-2 mb-4">
                        <span class="block text-muted-color font-medium">{{ name }}</span>
                        <div class="text-surface-900 dark:text-surface-0 font-medium text-xl">{{ title }}</div>
                        <div class="text-muted-color dark:text-surface-400">{{ subTitle }}</div>
                        <div class="flex items-center text-surface-900 dark:text-surface-0 mt-2 gap-2">
                            <i class="pi pi-star"></i>
                            <p>+{{ exp }} ans d'exp.</p>
                        </div>
                        <div class="flex items-center text-surface-900 dark:text-surface-0 mt-2">
                            <i class="pi pi-map"></i>
                            <div class="ml-2">
                                {{ loc }}
                            </div>
                        </div>
                        <div class="flex flex-col mt-2 gap-2">
                            <a v-for="link in links" v-bind:key="link.text" :href="link.url" target="_blank" class="flex gap-2 items-center text-surface-900 dark:text-surface-0">
                                <i :class="link.icon"></i>
                                <p class="underline">{{ link.text }}</p>
                            </a>
                        </div>
                    </div>
                </div>
            </template>
            <template #footer>
                <div class="flex mt-2 gap-3 justify-center">
                    <Chip v-for="tech in technologies" :key="tech.name">
                        <img :src="tech.logo" :alt="tech.name + ' logo'" class="w-6" />
                        <span>{{ tech.name }}</span>
                    </Chip>
                </div>
            </template>
        </Card>
    </div>
</template>
