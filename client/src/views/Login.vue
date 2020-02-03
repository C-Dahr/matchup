<template>
  <div class="login">
    <div class="form-title">
      <p>Login</p>
    </div>
    <div class="d-flex justify-content-center">
      <form action="" method="post" class="account-form">
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Username:</label>
              <input class="form-control" type="text"
              name="username" required placeholder="Enter Username"/>
              <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Password:</label>
              <input class="form-control" type="password"
                 name="password" required placeholder="Enter Password"/>
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
    createUser(payload) {
      const path = 'http://localhost:5000/user';
      axios.post(path, payload)
        .then(() => {
          this.$router.push('/');
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
      // this.$router.push('/');
    },
  },
};

</script>
