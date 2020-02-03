<template>
  <div class="signup">
    <div class="form-title">
      <p>Edit Profile</p>
    </div>
    <div class="d-flex justify-content-center">
      <form @submit="onSubmit"  method="put" class="account-form">
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Username:</label>
              <input class="form-control" type="text"
              name="username" required placeholder="Enter Username"/>
              <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Email:</label>
              <input class="form-control" type="text"
              name="email" required placeholder="Enter Email"/>
              <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Password:</label>
              <input class="form-control" type="password"
                 name="password" required placeholder="Enter Password"/>
                <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Confirm Password:</label>
              <input class="form-control" type="password"
                 name="passwordConfirm" required placeholder="Confirm Password"/>
                <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Challonge API Key:</label>
              <input class="form-control" type="password"
                 name="api_key" required placeholder="Enter Challonge API Key"/>
                <span class="Error"></span>
            </div>
            <h4>Generate or find an existing API key for Challonge <b-link href="https://challonge.com/settings/developer" target="_blank">here</b-link></h4>
            <div class="form-group d-flex justify-content-center">
                <input class="btn btn-primary account-form-submit" type="submit"
                 value="Create Account"/>
            </div>
        </form>
      </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      editProfileForm: {
        username: '',
        email: '',
        password: '',
        api_key: '',
      },
    };
  },
  name: 'EditProfile',
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {
        username: this.editProfileForm.username,
        email: this.editProfileForm.email,
        password: this.editProfileForm.password,
        api_key: this.editProfileForm.api_key,
      };
      this.updateUser(payload);
    },
    updateUser(payload) {
      const path = 'http://localhost:5000/auth';// TODO: Fix this path to the user instead of auth
      axios.put(path, payload)
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
