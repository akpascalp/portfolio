<script setup>
import { useLayout } from '@/layout/composables/layout';
import { ref, onMounted, onUnmounted } from 'vue';

const { toggleDarkMode, isDarkTheme } = useLayout();

const nestedMenuitems = ref([
    {
        label: 'Home'
    },
    {
        label: 'À propos'
    },
    {
        label: 'Contact'
    }
]);

const isVisible = ref(true);
let lastScrollTop = 0;

const handleScroll = () => {
    const scrollTop = document.documentElement.scrollTop;
    if (scrollTop > lastScrollTop) {
        // Scroll down
        isVisible.value = false;
    } else {
        // Scroll up
        isVisible.value = true;
    }
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // For Mobile or negative scrolling
};

onMounted(() => {
    window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
});
</script>

<template>
    <div :class="['layout-topbar', { 'translate-y-full': !isVisible, 'transition-transform duration-300 ease-in-out': true }]">
        <div class="layout-topbar-logo-container">
            <router-link to="/" class="layout-topbar-logo">
                <span>Pascal PHAM</span>
            </router-link>
        </div>

        <div class="flex-grow flex justify-center">
            <Menubar :model="nestedMenuitems" />
        </div>

        <div class="layout-topbar-actions">
            <IconField iconPosition="left">
                <InputIcon class="pi pi-search" />
                <InputText type="text" placeholder="Search" />
            </IconField>
            <div class="layout-config-menu">
                <button type="button" class="layout-topbar-action" @click="toggleDarkMode">
                    <i :class="['pi', { 'pi-moon': isDarkTheme, 'pi-sun': !isDarkTheme }]"></i>
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.layout-topbar {
    transform: translateY(0);
}

.layout-topbar.translate-y-full {
    transform: translateY(-100%);
}
</style>
