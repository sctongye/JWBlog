import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

URLSearchParams.prototype.appendIfExists = function (key, value) {
    if (value !== null && value !== undefined) {
        this.append(key, value)
    }
};

const app = createApp(App)
app.config.globalProperties.$axios = axios
app.use(router).mount('#app');