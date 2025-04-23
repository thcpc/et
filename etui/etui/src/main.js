import './assets/main.css'
// import 'codemirror/lib/codemirror.css';
// import 'codemirror/mode/javascript/javascript';
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import { EventBus } from "@/core/eventBus.js";
import '@toast-ui/editor/dist/toastui-editor.css'; // Editor's Style
import '@toast-ui/editor/dist/toastui-editor-viewer.css';

const app = createApp(App)
app.provide('eventBus', EventBus);
app.use(createPinia())
app.use(router)

app.mount('#app')
