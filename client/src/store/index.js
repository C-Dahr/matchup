import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    status: '',
    username: localStorage.getItem('username') || '',
    userToken: localStorage.getItem('user-token') || '',
    eventID: localStorage.getItem('event-id') || '',
    eventName: localStorage.getItem('event-name') || '',
  },
  getters: {
    isLoggedIn: state => !!state.userToken,
    getToken: state => state.userToken,
    authStatus: state => state.status,
    getEventID: state => state.eventID,
    getEventName: state => state.eventName,
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
    updateUser(state, newUsername) {
      state.username = newUsername;
      localStorage.setItem('username', newUsername);
    },
    setEventID(state, eventID) {
      state.eventID = eventID;
      localStorage.setItem('event-id', eventID);
    },
    setEventName(state, eventName) {
      state.eventName = eventName;
      localStorage.setItem('event-name', eventName);
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
            localStorage.setItem('username', user.username);
            this.state.username = user.username;
            localStorage.setItem('user-token', token);
            this.state.userToken = token;
            axios.defaults.headers.common.authorization = token;
            commit('auth_success', token);
            resolve(response);
          })
          .catch((err) => {
            commit('auth_error');
            localStorage.removeItem('username');
            localStorage.removeItem('user-token');
            reject(err);
          });
      });
    },
    logout({ commit }) {
      return new Promise((resolve) => {
        commit('logout');
        localStorage.removeItem('username');
        localStorage.removeItem('user-token');
        delete axios.defaults.headers.common.authorization;
        resolve();
      });
    },
    update_user({ commit }, username) {
      return new Promise((resolve) => {
        commit('updateUser', username);
        resolve();
      });
    },
  },
  plugins: [],
  modules: {
  },
});
