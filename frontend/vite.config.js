import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import dotenv from 'dotenv';
import dotenvExpand from 'dotenv-expand';
import path from 'path';

// 改變預設 .env 路徑為根目錄下
const myEnv = dotenv.config({ path: path.resolve(__dirname, '../.env') });
dotenvExpand.expand(myEnv);
// 只提取 VITE_ 開頭的變數
const viteEnv = {};
for (const key in myEnv.parsed) {
  if (key.startsWith('VITE_')) {
    viteEnv[key] = myEnv.parsed[key];
  }
}

// 初始化
export default defineConfig({
  plugins: [vue()],
  define: {
    'process.env': viteEnv, // 只傳遞 VITE_ 開頭的變數給 Vite
  },
  server: {
    hmr: {
      host: 'non.com.tw',  // 網域名稱
      port: 5615,  // Vite 運行的端口
    },
    https: {
      key: 'D:\\DiscordBot\\NonBot\\key\\origin.key',
      cert: 'D:\\DiscordBot\\NonBot\\key\\origin.pem',
    },
  }
})
