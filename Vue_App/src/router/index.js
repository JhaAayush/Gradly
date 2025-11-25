import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  },
  {
    path: '/profile/:userId?',
    name: 'Profile',
    component: () => import('../views/Profile.vue')
  },
  {
    path: '/feed',
    name: 'Feed',
    component: () => import('../views/Feed.vue')
  },
  {
    path: '/resources',
    name: 'Resources',
    component: () => import('../views/Resources.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
