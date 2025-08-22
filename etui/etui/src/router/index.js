import { createRouter, createWebHistory } from 'vue-router'


import UserLoginView from "@/views/etAdmin/UserLoginView.vue";
import RegisterUserView from "@/views/etAdmin/RegisterUserView.vue";
import DocumentListView from "@/views/etDocument/DocumentListView.vue";
import EtIndex from '@/views/EtIndex.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/documents',
      name: 'documentList',
      component: DocumentListView,
    },
    {
      path:'/',
      name: 'userLogin',
      component: UserLoginView,
    },
    {
      path:'/register',
      name: 'registerUser',
      component: RegisterUserView,
    },
    {
      path: '/index',
      name: 'index',
      component: EtIndex
    },
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue'),
    // },
    {
      path: '/testCaseDetail/:id',
      name: 'testCaseDetail',
      component: () => import('../views/etDocument/DocumentDetailView.vue'),
    }
  ],
})

export default router
