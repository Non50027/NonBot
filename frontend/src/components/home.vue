<template>
  <div>
    <h1>農農的小烏龜</h1>
    <div v-if="login" class="alert alert-success" role="alert">
        上線中
    </div>
    <div v-else class="alert alert-danger" role="alert">
      離線
    </div>
    <BButton @click="twitchOauth">Twitch bot</BButton>
    <BButton @click="discordOauth">Discord bot</BButton>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onUpdated, onMounted, onBeforeMount } from 'vue'
import axios from 'axios'
const login= reactive({})
// 載入前執行
onBeforeMount(()=>{
    // 提交表單
    console.log('ok')
    axios.get(`${import.meta.env.VITE_BACKEND_DISCORD_URL}/discord/get-bot-state`)
    .then(response => {
      console.log(response.data)
      Object.assign(login, response.data)
    })
    .catch(error => {
        console.log(error.response)
    })
});
// 載入後執行
onMounted(()=>{

});
// 資料更新後執行
onUpdated(()=>{

});

const twitchOauth= ()=>{
    location.href= '/oauth/twitch'
}
const discordOauth= ()=>{
    location.href= '/oauth/discord'
}
</script>

<style scoped>

</style>