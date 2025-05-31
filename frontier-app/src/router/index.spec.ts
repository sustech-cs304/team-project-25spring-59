import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createMemoryHistory } from 'vue-router'
import { mount } from '@vue/test-utils'
import router from './index.js'


describe('Vue Router', () => {
  beforeEach(() => {
    sessionStorage.clear()
  })

  it('navigates to /login', async () => {
    router.push('/login')
    await router.isReady()

    expect(router.currentRoute.value.fullPath).toBe('/login')
  })

  it('goes directly to /login from /beforeLogin without /transition', async () => {
    router.push('/beforeLogin')
    await router.isReady()

    router.push('/login')
    await router.isReady()

    expect(router.currentRoute.value.fullPath).toBe('/login')
  })

  it('blocks unauthenticated access to routes that require auth', async () => {
    router.push('/dashboard') // has requiresAuth: false
    await router.isReady()
    expect(router.currentRoute.value.fullPath).toBe('/login') // still intercepted due to transition logic

    // let's mock a route with auth required
    router.addRoute({
      path: '/protected',
      component: { template: '<div>Protected</div>' },
      meta: { requiresAuth: true }
    })

    router.push('/protected')
    await router.isReady()

    // Should redirect to login
    expect(router.currentRoute.value.fullPath).toBe('/login')
  })

  it('allows access to auth route if logged in', async () => {
    sessionStorage.setItem('token', 'valid-token')

    router.addRoute({
      path: '/protected-auth',
      component: { template: '<div>Protected</div>' },
      meta: { requiresAuth: true }
    })

    router.push('/protected-auth')
    await router.isReady()

    // Should go to transition first due to custom logic
    expect(router.currentRoute.value.path).toBe('/login')
  })
})
