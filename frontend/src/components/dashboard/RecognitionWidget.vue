<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { VueSignaturePad } from 'vue-signature-pad';

const drawingPad = ref(null);
const recognizedDigit = ref('');

function dataURLtoBlob(dataURL) {
    const arr = dataURL.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], { type: mime });
}

const sendDrawing = async () => {
    const { data } = drawingPad.value.saveSignature();
    const blob = dataURLtoBlob(data);
    const formData = new FormData();
    formData.append('file', blob);

    const response = await axios.post('http://localhost:8000/recognition/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    recognizedDigit.value = response.data.predictied;
};

const clearDrawing = () => {
    drawingPad.value.clearSignature();
    recognizedDigit.value = '';
};
</script>

<template>
    <Card>
        <template #header>
            <div class="flex justify-center text-xl mt-4 mx-4">Reconnaissance d'écriture manuscrite</div>
        </template>
        <template #content>
            <div class="flex flex-col gap-2">
                <div>Dessinez une lettre ou un chiffre:</div>
                <div class="flex flex-col items-center">
                    <VueSignaturePad width="175px" height="175px" ref="drawingPad" class="border" />
                    <div class="flex gap-2">
                        <button @click="sendDrawing" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded">Envoyer</button>
                        <button @click="clearDrawing" class="mt-4 px-4 py-2 bg-red-500 text-white rounded">Effacer</button>
                    </div>
                    <div v-if="recognizedDigit !== ''" class="mt-4 text-xl">Chiffre reconnu : {{ recognizedDigit }}</div>
                </div>
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
