<script setup>
import { onMounted, ref, watch } from 'vue'
import eventBus from '@/core/eventBus.js'
import { Constant, ErrCode, UnKnown } from '@/core/enums.js'
import router from '@/router/index.js'

import {httpGet, httpPostJson, httpResponse, httpRetry} from '@/core/http.js'
import {fingerPrint} from "@/core/utils.js";
import {userAuthStore} from "@/stores/tokenManager.js";
const authStore = userAuthStore()
const code = ref(UnKnown.Int)
const canClose = ref(false)
const password = ref('')
const userOpHis = ref({})

onMounted(() => {
  eventBus.$on('JwtTokenException', (userOp) => {
    code.value = userOp.errCode
    canClose.value = false
    userOpHis.value = userOp
    $('#jwtModal').css('z-index', 2000);
    $('#jwtModal').modal({
      backdrop: 'static',
    })
    $('#jwtModal').modal('show')
  })
  // const modal = document.getElementById('jwtModal')
  // modal.addEventListener('hide.bs.modal', (e) => {
  //   if (code.value === ErrCode.InvalidToken) {
  //     code.value = UnKnown.Int
  //     canClose.value = true
  //     router.replace('/')
  //   } else if (code.value === ErrCode.TokenTimeOut) {
  //     fingerPrint().then(finger=>{
  //       httpPostJson('/user/api/login', { password: password.value, fingerPrint: finger }, (resp) => {
  //         authStore.login(resp.token)
  //         userOpHis.value.config.headers['Authorization'] = `Bearer ${resp.token}`
  //         httpRetry(userOpHis.value.config, (response) => {
  //           userOpHis.value.callBack(response)
  //           canClose.value = true
  //           code.value = UnKnown.Int
  //         })
  //       })
  //     })
  //   }
  //   if(!canClose.value){e.preventDefault()}
  //
  //   return canClose.value
  // })
  // modal.addEventListener('shown.bs.modal', () => {
  //
  //
  // })
})


const goLogin = ()=>{
  $('#jwtModal').modal('hide')
  code.value = UnKnown.Int
  canClose.value = true
  router.replace('/')
}

const reLogin = ()=>{
  fingerPrint().then(finger=>{
    httpPostJson('/user/api/login', { password: password.value, fingerPrint: finger }, (resp) => {
      authStore.login(resp.token)
      userOpHis.value.config.headers['Authorization'] = `Bearer ${resp.token}`
      httpRetry(userOpHis.value.config, (response) => {
        userOpHis.value.callBack(response)
        canClose.value = true
        code.value = UnKnown.Int
        $('#jwtModal').modal('hide')
      })
    })
  })
}

// watch(()=>canClose.value,
//   (newValue, oldValue)=>{
//     if(newValue === true){
//       $('#jwtModal').modal('hide')
//     }
//   })
</script>

<template>
  <div class="modal modal-blur fade" id="jwtModal" tabindex="-1" role="dialog" aria-hidden="true">
    <div class="modal-dialog modal-sm modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-body">
          <div class="modal-title">
            <span v-show="code === ErrCode.InvalidToken">请点击重新登录</span>
            <span v-show="code === ErrCode.TokenTimeOut">超时间未操作,请重新输入密码</span>
          </div>

          <div v-show="code === ErrCode.InvalidToken"></div>
          <div v-show="code === ErrCode.TokenTimeOut">
            <div>
              <input
                type="password"
                class="form-control"
                placeholder="Password"
                v-model="password"
              />
              <small class="form-hint">
                Your password must be 8-20 characters long, contain letters and numbers, and must
                not contain spaces, special characters, or emoji.
              </small>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button
            v-show="code === ErrCode.InvalidToken"
            class="btn btn-danger"
            @click="goLogin()"
          >
            重新登录
          </button>
          <button
            v-show="code === ErrCode.TokenTimeOut"
            class="btn btn-danger"
            @click="reLogin()"
          >
            确认
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
