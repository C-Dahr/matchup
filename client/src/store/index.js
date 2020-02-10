import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    status: '',
    userToken: localStorage.getItem('user-token') || '',
  },
  getters: {
    isLoggedIn: state => !!state.userToken,
    authStatus: state => state.status,
  },
  mutations: {
    auth_request(state) {
      state.status = 'loading';
    },
    auth_success(state, token) {
      state.status = 'success';
      state.userToken = token;
    },
    auth_error(state) {
      state.status = 'error';
    },
    logout(state) {
      state.status = '';
      state.userToken = '';
    },
  },
  actions: {
    login({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('auth_request');
        const path = 'http://localhost:5000/auth';
        const headerInfo = Buffer.from(`${user.username}:${user.password}`, 'utf8').toString('base64');
        axios.post(path, '', { headers: { Authorization: `Basic ${headerInfo}` } })
          .then((response) => {
            const { token } = response.data;
            localStorage.setItem('user-token', token);
            axios.defaults.headers.common.authorization = token;
            commit('auth_success', token);
            resolve(response);
          })
          .catch((err) => {
            commit('auth_error');
            localStorage.removeItem('user-token');
            reject(err);
          });
      });
    },
    logout({ commit }) {
      return new Promise((resolve) => {
        commit('logout');
        localStorage.removeItem('user-token');
        delete axios.defaults.headers.common.authorization;
        resolve();
      });
    },
  },
  plugins: [],
  modules: {
  },
});
