<script setup>
import { ref, nextTick } from 'vue';
import axios from '@/service/axios';
import { marked } from 'marked';

const messages = ref([{ text: 'Posez-moi une question sur Pascal', fromUser: false }]);

const newMessage = ref('');
const loading = ref(false);
const scrollPanelRef = ref(null);

const sendMessage = () => {
    if (newMessage.value.trim()) {
        messages.value.push({ text: newMessage.value, fromUser: true });
        const params = { user_input: newMessage.value };
        newMessage.value = '';
        loading.value = true;
        axios
            .post('/chatbot', params)
            .then((response) => {
                if (response.data && response.data.response) {
                    receiveMessage(response.data.response);
                }
            })
            .finally(() => {
                loading.value = false;
                scrollToBottom();
        });
    }
};

const scrollToBottom = () => {
    const scrollPanel = scrollPanelRef.value.$el.querySelector('.p-scrollpanel-content');
    scrollPanel.scrollTop = scrollPanel.scrollHeight;
};

const receiveMessage = (message) => {
    messages.value.push({ text: marked(message), fromUser: false });
    nextTick(() => {
        scrollToBottom();
    });
};
</script>

<template>
    <Card>
        <template #header>
            <div class="flex justify-between mt-4 mx-4">
                <h1>Chat - A propos...</h1>
            </div>
        </template>
        <template #content>
            <div class="flex flex-col justify-between">
                <ScrollPanel ref="scrollPanelRef" style="width: 100%; height: 275px">
                    <div class="flex flex-col gap-2 p-4">
                        <div v-for="message in messages" :key="message.text" class="p-2 rounded-lg inline-block max-w-max" :class="message.fromUser ? 'bg-blue-500 text-white ml-auto text-right' : 'bg-gray-200 text-left'">
                            <span v-html="message.text"></span>
                        </div>
                    </div>
                </ScrollPanel>
                <div class="flex flex-row gap-2 p-4">
                    <InputText v-model="newMessage" @keydown.enter="sendMessage" placeholder="Ecrivez un message..."
                        class="flex-grow" />
                    <Button @click="sendMessage" :loading="loading" icon="pi pi-send" />
                </div>
            </div>
        </template>
    </Card>
</template>
