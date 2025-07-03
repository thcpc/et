import axios from 'axios'
import {userAuthStore} from "@/stores/tokenManager.js";
import eventBus from "@/core/eventBus.js";
import {ErrCode} from "@/core/enums.js";

// const dev = 'http://127.0.0.1:8080'
const dev = import.meta.env.VITE_API_BASE_URL
const root = dev
axios.interceptors.request.use(
  (config) => {
    // 在发送请求之前做些什么
    let user = userAuthStore()
    if(user.token){
      config.headers['Authorization'] = `Bearer ${user.token}`;
    }
    document.getElementById('overlay').classList.remove('d-none')
    return config
  },
  (error) => {
    // 对请求错误做些什么
    document.getElementById('overlay').classList.add('d-none')
    return Promise.reject(error)
  },
)

axios.interceptors.response.use(
  (response) => {
    // 对响应数据做些什么
    document.getElementById('overlay').classList.add('d-none')
      return response
  },
  (error) => {
    // 对响应错误做些什么
    document.getElementById('overlay').classList.add('d-none')
    return Promise.reject(error)
  },
)

export function httpGet(url, params, callBack, errCallBack) {
  axios
    .get(root + url, {
      params: params,
    })
    .then((response) => {
      httpResponse(response, callBack, errCallBack)
    })
    .catch((error) => {
      // console.error(error)
      alert(error)
    })
    .finally(() => {})
}

export function httpDelete(url, params, callBack, errCallBack) {
  axios
    .delete(root + url, {
      params: params,
    })
    .then((response) => {
      httpResponse(response, callBack, errCallBack)
    })
    .catch((error) => {

      alert(error)
    })
}

export function httpPostJson(url, data, callBack, errCallBack) {
  axios.defaults.headers.post['Content-Type'] = 'application/json'
  axios
    .post(root + url, data)
    .then((response) => {
      httpResponse(response, callBack, errCallBack)
    })
    .catch((error) => {

      alert(error)
    })
}

export function httpPostForm(url, formData, callBack, errCallBack) {
  axios
    .post(root + url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data', // 必须设置
      },
    })
    .then((response) => {
      httpResponse(response, callBack, errCallBack)
    })
    .catch((error) => {

      alert(error)
    })
}

export function httpResponse(response, callBack, errCallBack) {
  if (response.data.code === 200) {
    callBack(response.data.payload)
  } else if(response.data.code===ErrCode.InvalidToken || response.data.code===ErrCode.TokenTimeOut){
      if(errCallBack){ errCallBack() }
      eventBus.$emit('JwtTokenException', { config: response.config, callBack: callBack, errCode: response.data.code })
    }
}

export function httpRetry(config, callBack){
  axios.request(config).then(response=>{
    httpResponse(response, callBack)
  }).catch(error=>{
    alert(error)
  })
}
