import Vue from 'vue'
import Router from 'vue-router'
import Layout from '@/layout'

Vue.use(Router)

const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path*',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/',
    component: Layout,
    redirect: '/sql',
    children: []
  },
  {
    path: '/sql',
    component: Layout,
    name: 'SqlTest',
    meta: {
      title: 'Sql注入测试',
      icon: 'users'
    },
    children: [
      {
        path: 'bool',
        component: () => import('@/views/sql/bool'),
        name: 'BoolTest',
        meta: { title: '布尔注入', noCache: true }
      }
    ]
  }
]

const router = new Router({
  routes: constantRoutes
})

export {
  constantRoutes,
  router
}
