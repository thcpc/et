// stores/auth.js
import { defineStore } from 'pinia';
import {getToken, removeToken, setToken} from "@/core/auth.js";


export const userAuthStore = defineStore('auth', {
  state: () => ({
    token: getToken() || null, // 初始化时从缓存读取
  }),
  actions: {
    login(token) {
      this.token = token;
      setToken(token); // 存储到 localStorage
    },
    logout() {
      this.token = null;
      removeToken(); // 清除缓存
    },
  },
});
