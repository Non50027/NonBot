<template>
    <div>
        <h1>Twitch 農農的小烏龜 授權結果</h1>
        <div v-if="code">
            <p>授權成功</p>
            <p>code : {{ code }}</p>
            <p>權限範圍 : {{ scope }}</p>
            <BButton @click="clickButton">確認</BButton>
        </div>
        <!-- <div v-if="verification">
            <div v-if="code">
                <p>授權成功</p>
                <p>code : {{ code }}</p>
                <p>權限範圍 : {{ scope }}</p>
                <BButton @click="clickButton">確認</BButton>
            </div>
            <p v-if="error">授權失敗，錯誤信息: {{ errorDescription }}</p>
        </div>
        <div v-else>
            <p>Verification Code Error</p>
        </div> -->
    </div>
</template>

<script setup>
import axios from 'axios';
import { useRoute } from 'vue-router'
import { ref, reactive, computed, onUpdated, onMounted, onBeforeMount } from 'vue'

const code = ref()
const scope = ref()

const error = ref()
const errorDescription = ref()

const state= ref()

const verification= ref(false)
// 載入前執行
onBeforeMount(()=>{
    // URL 參數接收
    const route = useRoute()
    
    code.value = route.query.code
    scope.value = route.query.scope

    // 驗證 CSRF
    // const verificationCode= localStorage.getItem('csrfToken')
    // state.value= route.query.state
    // if (state.value===verificationCode){
    //     // 驗證 Oauth
    //     if (route.query.code){  // 驗證成功
    //         code.value = route.query.code
    //         scope.value = route.query.scope
    //     }else{                  // 驗證失敗
    //         error.value = route.query.error
    //         errorDescription.value = route.query.error_description
    //     }
    //     verification.value= true
    // }else{
    //     verification.value= false
    // }
});
const clickButton= ()=>{
    const url= `${import.meta.env.VITE_BACKEND_URL}/oauth/twitch-user-token`
    axios.post(url, {'code':code.value}
    )
    location.href= '/'
}
</script>

<style scoped>

</style>