import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    userToken: '',
  },
  getters: {
  },
  mutations: {
    updateUserToken: (state, newToken) => {
      state.userToken = newToken;
    },
  },
  actions: {
  },
  plugins: [createPersistedState()],
  modules: {
  },
});
