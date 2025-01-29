<script setup>
import PresentationWidget from '@/components/dashboard/PresentationWidget.vue';
import SkillsWidget from '@/components/dashboard/SkillsWidget.vue';
import LetterRecognitionWidget from '@/components/dashboard/LetterRecognitionWidget.vue';
</script>

<template>
    <div class="grid grid-cols-12 gap-8">
        <PresentationWidget class="col-span-6" />
        <SkillsWidget class="col-span-4" />
        <LetterRecognitionWidget class="col-span-2" />
        <!-- <StatsWidget />

        <div class="col-span-12 xl:col-span-6">
            <RecentSalesWidget />
            <BestSellingWidget />
        </div>
        <div class="col-span-12 xl:col-span-6">
            <RevenueStreamWidget />
            <NotificationsWidget />
        </div> -->
    </div>
</template>
