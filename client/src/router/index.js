import Vue from 'vue';
import VueRouter from 'vue-router';
import Login from '../views/Login.vue';
import SignUp from '../views/SignUp.vue';
import Home from '../views/Home.vue';
import store from '../store';
import EditProfile from '../views/EditProfile.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'login',
    component: Login,
    meta: {
      requiresNotLoggedIn: true,
    },
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: {
      requiresNotLoggedIn: true,
    },
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUp,
    meta: {
      requiresNotLoggedIn: true,
    },
  },
  {
    path: '/home',
    name: 'home',
    component: Home,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/editprofile',
    name: 'editprofile',
    component: EditProfile,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next();
      return;
    }
    next('/login');
  } else if (to.matched.some(record => record.meta.requiresNotLoggedIn)) {
    if (!store.getters.isLoggedIn) {
      next();
      return;
    }
    next('/home');
  }
  next();
});

export default router;
