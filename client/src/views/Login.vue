<template>
  <div class="login">
    <div class="form-title">
      <p>Login</p>
    </div>
    <div class="form-error-list d-flex
    justify-content-center" v-if="errors.length">
      <ul class="form-error form-group d-flex justify-content-center">
        <div v-for="error in errors" v-bind:key="error">{{ error }}</div>
      </ul>
    </div>
    <div class="d-flex justify-content-center">
      <form @submit="onSubmit" method="post" class="account-form">
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Username:</label>
              <input class="form-control" type="text"
              name="username" v-model="loginForm.username"
              required placeholder="Enter Username"/>
              <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Password:</label>
              <input class="form-control" type="password"
                 name="password" v-model="loginForm.password"
                 required placeholder="Enter Password"/>
                <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-center">
                <input class="btn btn-primary account-form-submit" type="submit"
                 value="Sign in"/>
            </div>
        </form>
      </div>
      <h3>Don't have an account? <router-link to="/signup">Sign Up</router-link></h3>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      errors: [],
      loginForm: {
        username: '',
        password: '',
      },
    };
  },
  name: 'Login',
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {
        username: this.loginForm.username,
        password: this.loginForm.password,
      };
      this.loginUser(payload);
    },
    loginUser(payload) {
      const path = 'http://localhost:5000/auth';
      const token = Buffer.from(`${payload.username}:${payload.password}`, 'utf8').toString('base64');
      axios.post(path, '', { headers: { Authorization: `Basic ${token}` } })
        .then((response) => {
          const newToken = response.data;
          this.$store.commit('updateUserToken', newToken);
          this.$router.push('/home');
        })
        .catch((error) => {
          if (error.response.status === 404) {
            this.errors.push('Login Failed');
          }
        });
    },
  },
};

</script>
