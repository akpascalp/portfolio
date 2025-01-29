<script setup>
import { ref } from 'vue';
import { VueSignaturePad } from 'vue-signature-pad';

const signaturePad = ref(null);
const recognizedLetter = ref('');

const sendDrawing = async () => {
    const dataUrl = signaturePad.value.toDataURL();
    const response = await fetch('YOUR_API_ENDPOINT', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: dataUrl })
    });
    const result = await response.json();
    recognizedLetter.value = result.letter;
};
</script>

<template>
    <Card>
        <template #header>
            <div class="flex justify-center text-xl mt-4 mx-4">Reconnaissance de lettres</div>
        </template>
        <template #content>
            <div class="flex flex-col items-center">
                <VueSignaturePad width="175px" height="300px" ref="signaturePad" class="border" />
                <button @click="sendDrawing" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded">Envoyer</button>
                <div v-if="recognizedLetter" class="mt-4 text-xl">Lettre reconnue : {{ recognizedLetter }}</div>
            </div>
        </template>
    </Card>
</template>

<style scoped>
.vue-signature-pad {
    width: 100px;
    height: 300px;
}
</style>
