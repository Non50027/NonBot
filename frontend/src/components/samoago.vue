<template>
    <BContainer style="max-width: 70%;">
        <div class="text-center">
            <div class="h1">Ago 的按鈕</div>
            <div>
                <div>這裡是粉絲創作的網頁</div>
                <div>語主播沒有關聯</div>
                <div>網頁作者為農農</div>
                <div>有問題都可以回饋給我</div>
                <div>畫面還沒有排版...因為我前端弄得有點遭</div>
                <div>其他想要的功能都可以說</div>
                <div>所以如果有遇到BUG的請跟我說</div>

            </div>
        </div>
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
                
                    <div v-if="loading" class="spinner-border text-success"></div>
                    <div v-else>
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
                    </div>
                </b-modal>
            </div>
                
            <BCol v-for="(sound, sound_index) in soundData" :key="sound_index">
                <BButton 
                    pill 
                    variant="outline-light"
                    @click= "playSound(selfUrl + sound.file_name, sound_index)" 
                    class= "text-nowrap vo-btn"
                    :class= "{ playing: isPlayButton === sound_index }"
                    :style="{ 
                        '--progress': isPlayButton === sound_index ? progress + '%' : '0%' , 
                        '--start-percent': isPlayButton === sound_index ? (progress - 5 ) + '%' : '100%' }">
                    <div class="btn-content">{{ sound.name }}</div>
                </BButton>
            </BCol>
        </BRow>
    </BContainer>
</template>

<script setup>
import { ref, reactive, onBeforeMount, inject } from 'vue'
import axios from 'axios'

const selfUrl= `${inject('selfUrl')}/static/sounds/`
const soundName= ref('')
const isFormOpen = ref(false);
const loading = ref(false);
const uploadedFile = ref(null);
const isPlayButton= ref(null); // 紀錄正在播放中的按鈕
const progress = ref(0); // 追蹤播放進度

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

const playSound = (soundUrl, index) => {
    const audio = new Audio(soundUrl);
    isPlayButton.value = index; // 記錄正在播放的按鈕
    progress.value= 0; // 播放前進度歸零
    
    audio.play();

    // 監聽音樂播放進度
    const updateProgress = setInterval(() => {
        if (audio.duration) {
            progress.value = (audio.currentTime / audio.duration) * 100; // 計算百分比
        }
    }, 100); // 每 100ms 更新一次

    // 當音樂結束時，清除播放狀態
    audio.onended = () => {
        isPlayButton.value = null;
        progress.value = 0;
        clearInterval(updateProgress);
    };
};

// 上傳的檔案存入 selectedFile
const onFileChange = (event) => {
    uploadedFile.value = event.target.files[0]
    console.log('file size: ', event.target.files[0].size)
}
// 方法
const openModal = () => {
    isFormOpen.value = true;
};

const closeModal = () => {
    isFormOpen.value = false;
};

const submit = () => {
    loading.value= true

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
        loading.value= false
        console.log(error)
        alert('提交失敗！');
    })

};
</script>

<style scoped>
.vo-btn {
    background: linear-gradient(to right, #19a77c var(--start-percent), #45c79b var(--progress));
    color: white !important;
} 

/* 播放時的抖動動畫 */
.playing div {
    animation: shake 3s linear infinite;
}

/* 抖動動畫 */
@keyframes shake {
  0%, 100% {
    transform: translateY(0px);
  }
  25%, 35% {
    transform: translateY(-3px);
  }
  30%, 40% {
    transform: translateY(0px);
  }
}

</style>