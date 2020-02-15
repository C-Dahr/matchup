<template>
  <div class="signup">
    <div class="form-title">
      <p>Edit Profile</p>
    </div>
    <div class="form-error-list" v-if="errors.length">
      <ul class="form-error">
        <li v-for="error in errors" v-bind:key="error">{{ error }}</li>
      </ul>
    </div>
    <div class="d-flex justify-content-center">
      <form @submit="onSubmit"  method="post" class="account-form">
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Username <span class="required-star">*</span></label>
              <input class="form-control" type="text"
              name="username" v-model="editProfileForm.username"
              required placeholder="Enter Username"/>
              <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Email <span class="required-star">*</span></label>
              <input class="form-control" type="text"
              name="email" v-model="editProfileForm.email"
              required placeholder="Enter Email"/>
              <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Password <span class="required-star">*</span></label>
              <input class="form-control" type="password"
                 name="password" v-model="editProfileForm.password"
                 required placeholder="Enter Password"/>
                <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">
                Confirm Password
                <span class="required-star">*</span>
              </label>
              <input class="form-control" type="password"
                 name="passwordConfirm" v-model="editProfileForm.confirm_password"
                 required placeholder="Confirm Password"/>
                <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Challonge Username</label>
              <input class="form-control" type="text"
              name="challonge_username" v-model="editProfileForm.challonge_username"
              placeholder="Enter Challonge Username"/>
              <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Challonge API Key</label>
              <input class="form-control" type="password"
                 name="api_key" v-model="editProfileForm.api_key"
                 placeholder="Enter Challonge API Key"/>
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
      errors: [],
      editProfileForm: {
        username: '',
        email: '',
        password: '',
        confirm_password: '',
        challonge_username: '',
        api_key: '',
      },
    };
  },
  name: 'EditProfile',
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      this.errors = [];
      if (this.editProfileForm.password !== this.editProfileForm.confirm_password) {
        this.editProfileForm.password = '';
        this.editProfileForm.confirm_password = '';
        this.errors.push('Passwords do not match');
      } else {
        const payload = {
          username: this.editProfileForm.username,
          email: this.editProfileForm.email,
          password: this.editProfileForm.password,
          challonge_username: this.editProfileForm.challonge_username,
          api_key: this.editProfileForm.api_key,
        };
        this.createUser(payload);
      }
    },
    updateUser(payload) {
      const path = 'http://localhost:5000/user';
      axios.put(path, payload)
        .then(() => {
          this.$router.push('/');
        })
        .catch((error) => {
          if (error.response.status === 409) {
            this.errors.push('Username already exists');
          }
        });
    },
  },
};

</script>
