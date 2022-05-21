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
        meta: { title: '布尔盲注', noCache: true }
      },
      {
        path: 'time',
        component: () => import('@/views/sql/time'),
        name: 'TimeTest',
        meta: { title: '时间盲注', noCache: true }
      },
      {
        path: 'union',
        component: () => import('@/views/sql/union'),
        name: 'UnionTest',
        meta: { title: '联合注入', noCache: true }
      },
      {
        path: 'error',
        component: () => import('@/views/sql/error'),
        name: 'ErrorTest',
        meta: { title: '报错注入', noCache: true }
      },
      {
        path: 'wide_char',
        component: () => import('@/views/sql/wide_char'),
        name: 'WideCharTest',
        meta: { title: '宽字节注入', noCache: true }
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
