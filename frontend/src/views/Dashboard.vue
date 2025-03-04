<script setup>
import PresentationWidget from '@/components/dashboard/PresentationWidget.vue';
import SkillsWidget from '@/components/dashboard/SkillsWidget.vue';
import RecognitionWidget from '@/components/dashboard/RecognitionWidget.vue';
import ChatbotWidget from '@/components/dashboard/ChatbotWidget.vue';
import SimulationWidget from '@/components/dashboard/SimulationWidget.vue';
</script>

<template>
    <div class="grid grid-cols-12 gap-8">
        <PresentationWidget class="col-span-6" />
        <SkillsWidget class="col-span-3" />
        <ChatbotWidget class="col-span-3" />
        <RecognitionWidget class="col-span-2" />
        <SimulationWidget class="col-span-5" />
    </div>
</template>
