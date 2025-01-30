<script setup>
import PresentationWidget from '@/components/dashboard/PresentationWidget.vue';
import SkillsWidget from '@/components/dashboard/SkillsWidget.vue';
import RecognitionWidget from '@/components/dashboard/RecognitionWidget.vue';
import OptimizerWidget from '@/components/dashboard/OptimizerWidget.vue';
import SimulationWidget from '@/components/dashboard/SimulationWidget.vue';
</script>

<template>
    <div class="grid grid-cols-12 gap-8">
        <PresentationWidget class="col-span-6" />
        <SkillsWidget class="col-span-4" />
        <RecognitionWidget class="col-span-2" />
        <OptimizerWidget class="col-span-4" />
        <SimulationWidget class="col-span-4" />
    </div>
</template>
