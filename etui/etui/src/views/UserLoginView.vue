<script setup>
import { onMounted, ref } from 'vue'
import { httpGet, httpPostJson } from '@/core/http.js'
import router from '@/router/index.js'
import { userAuthStore } from '@/stores/tokenManager.js'

import FingerprintJS2 from 'fingerprintjs2'
import { fingerPrint } from '@/core/utils.js'

const username = ref('')
const password = ref('')
const authStore = userAuthStore()

onMounted(() => {
  fingerPrint().then((finger) => {
    httpGet('/user/api/device', { fingerPrint: finger }, (resp) => {
      username.value = resp.username
    })
  })
})

const login = () => {
  fingerPrint().then((finger) => {
    httpPostJson(
      '/user/api/login',
      {
        username: username.value,
        password: password.value,
        fingerPrint: finger,
      },
      (resp) => {
        authStore.login(resp.token)
        router.replace('/documents')
      },
    )
  })
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      <h3 class="card-title">用户登录</h3>
    </div>
    <div class="card-body">
      <div class="mb-3">
        <label class="form-label required">Email address</label>
        <div>
          <input
            type="email"
            class="form-control"
            aria-describedby="emailHelp"
            placeholder="Enter email"
            v-model="username"
          />
          <small class="form-hint">We'll never share your email with anyone else.</small>
        </div>
      </div>
      <div class="mb-3">
        <label class="form-label required">Password</label>
        <div>
          <input type="password" class="form-control" placeholder="Password" v-model="password" />
          <small class="form-hint">
            Your password must be 8-20 characters long, contain letters and numbers, and must not
            contain spaces, special characters, or emoji.
          </small>
        </div>
      </div>
    </div>
    <div class="card-footer text-end">
      <button class="btn btn-primary" @click="login()">登录</button>
      <a href="/register" class="btn btn-primary">注册</a>
    </div>
  </div>
</template>

<style scoped></style>
