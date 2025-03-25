import { createRouter, createWebHashHistory } from 'vue-router'
import GameView from '../views/GameView.vue'
import ListView from '@/views/ListView.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/:date?',
      name: 'game',
      component: GameView,
    },
    {
      path: '/previous',
      name: 'previous-challenges',
      component: ListView,
    },
  ],
})

export default router
