import { createRouter, createWebHistory } from 'vue-router'
import home from './components/home.vue'
import oauthTwitch from './oauth/twitch.vue'
import oauthDiscord from './oauth/discord.vue'
import callback from './oauth/callback.vue'

const routes=[
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
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
