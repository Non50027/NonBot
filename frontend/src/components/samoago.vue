<template>
    <BContainer style="max-width: 70%;">
        <BRow>
            <div class="text-center mt-4">
                <!-- 按鈕觸發懸浮窗 -->
                <BButton pill variant="primary" @click="openModal">上傳音效</BButton>

                <!-- 懸浮窗 -->
                <b-modal
                v-model="isFormOpen"
                hide-footer
                size="lg"
                centered
                >
                <!-- 文字方塊 -->
                <BInputGroup prepend="名稱">
                    <BFormInput v-model="soundName" placeholder="輸入名稱"></BFormInput>
                </BInputGroup>

                <!-- 檔案上傳 -->
                <div class="input-group mt-3">
                    <input class="form-control" type="file" @change="onFileChange">
                </div>

                <!-- 按鈕 -->
                <div class="d-flex justify-content-end mt-3">
                    <BButton variant="success" @click="submit" :disabled="!uploadedFile" class="me-2">提交</BButton>
                    <BButton variant="secondary" @click="closeModal">取消</BButton>
                </div>
                </b-modal>
            </div>
                
            <BCol v-for="(sound, sound_index) in soundData" :key="sound_index">
                <BButton pill variant="outline-primary" @click="playSound(selfUrl + sound.file_name)" class="text-nowrap">{{ sound.name }}</BButton>
            </BCol>
        </BRow>
    </BContainer>
</template>

<script setup>
import { ref, reactive, computed, onUpdated, onMounted, onBeforeMount, inject } from 'vue'
import axios from 'axios'

const selfUrl= `${inject('selfUrl')}/static/sounds/`
// const optionsData= inject('optionsData')
// const soundData= computed(() => optionsData?.sound|| [])
const soundName= ref('')
const isFormOpen = ref(false);
const textInput = ref('');
const uploadedFile = ref(null);

const soundData= reactive([])
//取得所有音效檔案資料
onBeforeMount(async () => {
    axios.get(`${import.meta.env.VITE_BACKEND_URL}/sounds/all`)
    .then(response => {
        Object.assign(soundData, response.data)
    })
    .catch(error => {
        console.log('error', error)
    })
});

const playSound = (soundUrl) => {
    const audio = new Audio(soundUrl);
    audio.play();
};

// 上傳的檔案存入 selectedFile
const onFileChange = (event) => {
    uploadedFile.value = event.target.files[0]
}
// 方法
const openModal = () => {
    isFormOpen.value = true;
};

const closeModal = () => {
    isFormOpen.value = false;
};

const submit = () => {
    if (!soundName.value || !uploadedFile.value) {
    alert('請填寫名稱並選擇檔案！');
    return;
    }

    // 提交邏輯
    console.log('名稱：', soundName.value);
    console.log('上傳檔案：', uploadedFile.value);
    axios.post(`${import.meta.env.VITE_BACKEND_URL}/sounds/${soundName.value}`, {
        file: uploadedFile.value
    }, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
    .then(response => {
        closeModal();
        console.log(response.data)
        alert('提交成功！');
        location.reload()
    })
    .catch(error => {
        closeModal();
        console.log(error)
        alert('提交失敗！');
    })

};
</script>
