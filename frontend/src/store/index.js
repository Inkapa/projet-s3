import { createStore } from 'vuex'
import createPersistedState from "vuex-persistedstate";
import AuthService from '../services/auth.service.js'
import UserInformation from '../services/userInfo.service'

const initialState = localStorage.getItem('token') ? {isAuthenticated: true, access_token: localStorage.getItem('token'), userInformation: localStorage.getItem('basicInfo')} : {isAuthenticated: false, access_token: null, userInformation: {}}

export default createStore({
  state: initialState,
  mutations: {
    LOGIN (state, access_token){
      state.isAuthenticated = true;
      state.access_token = access_token;
    },
    LOGOUT (state){
      state.isAuthenticated = false;
      state.access_token = null;
      state.userInformation = {};
    },
    SET_BASIC_INFO (state, payload){
      state.userInformation = payload;
    }
  },
  actions: {
    async login({ commit }, userInfo){
      try {
        const data = await AuthService.login(userInfo);
        commit('LOGIN', data.access_token);
        localStorage.setItem('token', data.access_token);
        return await Promise.resolve();
      } catch (error) {
        commit('LOGOUT');
        return await Promise.reject(error);
      }
    },
    logout({ commit }) {
      localStorage.removeItem('token');
      commit('LOGOUT');
    },

    // Avoir les infos de base de l'utilisateur style username, mail et perms
    async setBasicInformation({ commit }) {
      return await UserInformation.getBasicInformation().then((data) => {
        commit('SET_BASIC_INFO', data)
        localStorage.setItem('basicInfo', data);
        return Promise.resolve(data);
      }).catch((error) => {
        return Promise.reject(error);
      })
    }
  },
  modules: {
  },
  plugins: [createPersistedState()]
})