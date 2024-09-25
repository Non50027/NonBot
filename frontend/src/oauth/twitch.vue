<template>
    <div>
        <BButton @click="clickButton">認證</BButton>
    </div>
</template>

<script setup>
import axios from 'axios'
import { onBeforeMount } from 'vue'
onBeforeMount(()=>{
    axios.get(`${import.meta.env.VITE_BACKEND_URL}/oauth/get_csrf_token/`)
    .then(response=>{
        localStorage.setItem('csrfToken', response.data.csrfToken);
    }).catch(error=>{
        console.log('error:', error)
    });
    
});
const client_id= import.meta.env.VITE_TWITCH_BOT_ID
const redirect_uri= encodeURIComponent("https://non.com.tw/oauth/callback")
const scope= encodeURIComponent("chat:read chat:edit")
const clickButton= ()=>{
    const state= localStorage.getItem('csrfToken');
    const url= `https://id.twitch.tv/oauth2/authorize?client_id=${client_id}&redirect_uri=${redirect_uri}&response_type=code&scope=${scope}&state=${state}`
    window.location.href= url;
}
</script>

<style scoped>

</style>