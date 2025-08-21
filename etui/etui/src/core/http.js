import axios from 'axios'
import {userAuthStore} from "@/stores/tokenManager.js";
import eventBus from "@/core/eventBus.js";
import { GlobalConst } from '@/core/const/enums.js'
import Cookies from 'js-cookie';
import { globalEvent } from '@/core/const/events.js'

const backendURI = import.meta.env.VITE_API_BASE_URL

const api = axios.create({
  baseURL: backendURI,  // 替换为你的 Django 后端地址
  withCredentials: true,  // 允许跨域请求携带 Cookie
});


api.interceptors.request.use(
  (config) => {
    // 在发送请求之前做些什么
    let user = userAuthStore()

    const csrfToken = Cookies.get('csrftoken');
    // console.log(Cookies)
    if(user.token){
      config.headers['Authorization'] = `Bearer ${user.token}`;
    }
    config.headers['X-CSRFToken'] = csrfToken;
    // config.headers['credentials'] = "include";
    document.getElementById('overlay').classList.remove('d-none')
    return config
  },
  (error) => {
    // 对请求错误做些什么
    document.getElementById('overlay').classList.add('d-none')
    return Promise.reject(error)
  },
)

api.interceptors.response.use(
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
  api
    .get(url, {
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
  api
    .delete(url, {
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
  api.defaults.headers.post['Content-Type'] = 'application/json'
  api
    .post(url, data)
    .then((response) => {
      httpResponse(response, callBack, errCallBack)
    })
    .catch((error) => {

      alert(error)
    })
}

export function httpPostForm(url, formData, callBack, errCallBack) {
  api
    .post(url, formData, {
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
  } else if(response.data.code===GlobalConst.ErrCode.InvalidToken || response.data.code===GlobalConst.ErrCode.TokenTimeOut){
      if(errCallBack){ errCallBack() }
      eventBus.$emit(globalEvent.JwtTokenException, { config: response.config, callBack: callBack, errCode: response.data.code })
  }
  else {
    alert(response.data.err)
  }

}

export function httpRetry(config, callBack){
  api.request(config).then(response=>{
    httpResponse(response, callBack)
  }).catch(error=>{
    alert(error)
  })
}
