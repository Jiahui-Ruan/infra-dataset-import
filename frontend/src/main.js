// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import VueSocketio from 'vue-socket.io'
import VuePaginate from 'vue-paginate'

const HOST = window.location.hostname
const PORT = '5005'
const SOCKET_URL = `${HOST}:${PORT}`

Vue.config.productionTip = false
Vue.component('StatHeader', require('@/components/stat-header'))
Vue.component('BagList', require('@/components/bag-list'))
Vue.component('BagParamList', require('@/components/bag-param-list'))
Vue.component('CtrlBar', require('@/components/ctrl-bar'))
Vue.filter('dir2name', dir => dir.substring(dir.lastIndexOf('/') + 1, dir.length))
Vue.use(VueSocketio, SOCKET_URL)
Vue.use(VuePaginate)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  template: '<App/>',
  components: { App }
})
