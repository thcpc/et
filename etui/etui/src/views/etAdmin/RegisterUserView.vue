<script setup>
import {onMounted, ref} from "vue";
import {httpPostJson} from "@/core/http.js";
import {useRouter} from "vue-router";

import {fingerPrint} from "@/core/utils.js";
import { etAdminUrl } from '@/core/const/urls.js'

const username = ref('')
const password = ref('')
const router = useRouter()


onMounted(()=>{
  let finger = fingerPrint()
  console.log(finger)
})

const register = ()=>{
  httpPostJson(etAdminUrl.register, {username:username.value, password:password.value}, ()=>{
    router.replace('/');
  })
}


</script>



<template>
  <div class="card">
    <div class="card-header">
      <h3 class="card-title">用户注册</h3>
    </div>
    <div class="card-body">
      <div class="mb-3">
        <label class="form-label required">Email address</label>
        <div>
          <input type="email" class="form-control" aria-describedby="emailHelp" placeholder="Enter email" v-model="username">
          <small class="form-hint">We'll never share your email with anyone else.</small>
        </div>
      </div>
      <div class="mb-3">
        <label class="form-label required">Password</label>
        <div>
          <input type="password" class="form-control" placeholder="Password" v-model="password">
          <small class="form-hint">
            Your password must be 8-20 characters long, contain letters and numbers, and must not contain
            spaces, special characters, or emoji.
          </small>
        </div>
      </div>
    </div>
    <div class="card-footer text-end">
      <button class="btn btn-primary" @click="register()">注册</button>
    </div>
  </div>
</template>

<style scoped>

</style>
