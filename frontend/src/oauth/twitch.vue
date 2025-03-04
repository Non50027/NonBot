<template>
    <div>
        <!-- <BButton @click="clickButton">認證</BButton> -->
        <div>這裡還沒有東西</div>
        <BButton @click="clickButton">回首頁</BButton>

    </div>
    
</template>

<script setup>
import axios from 'axios'
import { onBeforeMount } from 'vue'
onBeforeMount(()=>{
    // axios.get(`${import.meta.env.VITE_BACKEND_URL}/oauth/csrf-token`)
    // .then(response=>{
    //     localStorage.setItem('csrfToken', response.data.csrfToken);
    // }).catch(error=>{
    //     console.log('error:', error)
    // });
    
});

const client_id= import.meta.env.VITE_TWITCH_BOT_ID
const redirect_uri= encodeURIComponent("https://non.com.tw/oauth/callback")
// const scope= encodeURIComponent("channel:manage:broadcast channel:read:editors channel:manage:extensions channel:read:goals channel:read:guest_star channel:manage:guest_star channel:manage:moderators channel:read:polls channel:manage:polls channel:read:predictions channel:manage:predictions channel:manage:raids channel:read:redemptions channel:manage:redemptions channel:manage:schedule channel:read:subscriptions channel:manage:videos channel:read:vips channel:manage:vips clips:edit moderation:read moderator:manage:announcements moderator:manage:automod moderator:read:automod_settings moderator:manage:automod_settings moderator:read:banned_users moderator:manage:banned_users moderator:read:blocked_terms moderator:read:chat_messages moderator:manage:blocked_terms moderator:manage:chat_messages moderator:read:chat_settings moderator:manage:chat_settings moderator:read:chatters moderator:read:followers moderator:read:guest_star moderator:manage:guest_star moderator:read:moderators moderator:read:shield_mode moderator:manage:shield_mode moderator:read:shoutouts moderator:manage:shoutouts moderator:read:suspicious_users moderator:read:vips whispers:read user:write:chat user:read:whispers user:manage:whispers user:read:subscriptions user:read:follows user:read:emotes user:bot channel:bot chat:read chat:edit")
const scope= encodeURIComponent("chat:read chat:edit")
const _clickButton= ()=>{
    // const state= localStorage.getItem('csrfToken');
    // const url= `https://id.twitch.tv/oauth2/authorize?client_id=${client_id}&redirect_uri=${redirect_uri}&response_type=code&scope=${scope}&state=${state}`
    const url= `https://id.twitch.tv/oauth2/authorize?forec_verify=true&client_id=${client_id}&redirect_uri=${redirect_uri}&response_type=code&scope=${scope}`
    window.location.href= url;
}
const clickButton= ()=>{
    location.href= '/'
}
</script>

<style scoped>

</style>