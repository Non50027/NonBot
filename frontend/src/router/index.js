import { createRouter, createWebHistory } from 'vue-router'
import home from '../components/home.vue'
import oauthTwitch from '../oauth/twitch.vue'
import oauthDiscord from '../oauth/discord.vue'
import callback from '../oauth/callback.vue'
import samoago from '../components/samoago.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
      { 
          path: '/',
          component: home,
      },
      { 
          path: '/oauth',
          children:[
              { 
                  path: 'twitch',
                  name: 'oauthTwitch',
                  component: oauthTwitch,
              },
              { 
                  path: 'discord',
                  name: 'oauthDiscord',
                  component: oauthDiscord,
              },
              { 
                  path: 'callback',
                  name: 'callback',
                  component: callback,
              },
          ]
      },
      { 
          path: '/samoago',
          children: [
              {
                  path: "home",
                  name: 'samoago-home',
                  component: samoago,
              }
          ]
      },
  ],
})

export default router
