<template>
    <div>
        <div>這裡還沒有東西</div>
        <BButton @click="clickButton">回首頁</BButton>
    </div>
</template>

<script setup>
import { ref, reactive, computed, onUpdated, onMounted, onBeforeMount } from 'vue'
// 載入前執行
onBeforeMount(()=>{

});
// 載入後執行
onMounted(()=>{

});
// 資料更新後執行
onUpdated(()=>{

});
const clickButton= ()=>{
    location.href= '/'
}
</script>

<style scoped>

</style>