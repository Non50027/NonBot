<template>
  <div>
    <h1>農農的小烏龜</h1>
    <div v-if="discord_login" class="alert alert-success" role="alert">
        Discord 上線中
    </div>
    <div v-if="twitch_login" class="alert alert-success" role="alert">
        twitch 上線中
    </div>
    <div v-else class="alert alert-danger" role="alert">
      離線
    </div>
    <BButton @click="twitchOauth">Twitch bot</BButton>
    <BButton @click="discordOauth">Discord bot</BButton>
    <BButton @click="ago_btn">Ago 按鈕</BButton>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onUpdated, onMounted, onBeforeMount } from 'vue'
import axios from 'axios'
const discord_login= reactive({})
const twitch_login= reactive({})
// 載入前執行
onBeforeMount(()=>{
    // 取得 discord 狀態
    axios.get(`${import.meta.env.VITE_BACKEND_DISCORD_URL}/discord/state`)
    .then(response => {
      console.log(response.data)
      Object.assign(discord_login, response.data)
    })
    .catch(error => {
        console.log(error.response)
    })
    // 取得 discord 狀態
    axios.get(`${import.meta.env.VITE_BACKEND_DISCORD_URL}/twitch/state`)
    .then(response => {
      console.log(response.data)
      Object.assign(discord_login, response.data)
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
const ago_btn= ()=>{
    location.href= '/samoago/home'
}
</script>

<style scoped>

</style>