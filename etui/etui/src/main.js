import "./assets/draggable/draggable.bundle.js"
import "./assets/tabler/js/demo-theme.min.js"
import "./assets/tabler/js/tom-select.base.min.js"
import "./assets/tabler/js/nouislider.min.js"
import "./assets/tabler/js/litepicker.js"
import "./assets/tabler/js/tabler.min.js"
import "./assets/tabler/js/demo.min.js"
import "./assets/summernote/jquery-3.4.1.slim.min.js"
import "./assets/summernote/summernote-lite.min.js"

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
