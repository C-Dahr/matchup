import Vue from 'vue';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faUserCircle } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import App from './App.vue';
import router from './router';
import store from './store';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

library.add(faUserCircle);

Vue.component('font-awesome-icon', FontAwesomeIcon);

// Install BootstrapVue
Vue.use(BootstrapVue);
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);

Vue.config.productionTip = false;

Vue.mixin({
  methods: {
    getFieldForErrorMessage(message) {
      let field = message.substring(message.indexOf('(') + 1, message.indexOf(')'));
      field = field.replace('_', ' ');
      field = field.charAt(0).toUpperCase() + field.slice(1);
      return field;
    },
  },
});

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app');
