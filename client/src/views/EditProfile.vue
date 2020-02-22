<template>
  <div class="editprofile">
    <div class="form-title">
      <p>Edit Profile</p>
    </div>
    <div>
      <p id="success-message">Updated Successfully</p>
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
                 value="Save Changes"/>
            </div>
            <div class="form-group d-flex justify-content-center">
                <input class="btn btn-secondary cancel-btn" type="button"
                 value="Cancel" @click="cancel"/>
            </div>
        </form>
      </div>
  </div>
</template>

<script>
import axios from 'axios';

function getFieldForErrorMessage(message) {
  let field = message.substring(message.indexOf('(') + 1, message.indexOf(')'));
  field = field.replace('_', ' ');
  field = field.charAt(0).toUpperCase() + field.slice(1);
  return field;
}

export default {
  data() {
    return {
      errors: [],
      editProfileForm: {
        username: '',
        email: '',
        challonge_username: '',
        api_key: '',
      },
    };
  },
  computed: {
    token() { return this.$store.state.userToken; },
  },
  name: 'EditProfile',
  created() {
    const path = 'http://localhost:5000/user';
    axios.get(path, { headers: { 'x-access-token': this.token } })
      .then((response) => {
        this.editProfileForm.username = response.data.username;
        this.editProfileForm.email = response.data.email;
        this.editProfileForm.challonge_username = response.data.challonge_username;
        this.editProfileForm.api_key = response.data.api_key;
      })
      .catch(() => {
        this.errors.push('Error loading profile info');
      });
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      this.errors = [];
      const payload = {
        username: this.editProfileForm.username,
        email: this.editProfileForm.email,
        challonge_username: this.editProfileForm.challonge_username,
        api_key: this.editProfileForm.api_key,
      };
      this.updateUser(payload);
    },
    updateUser(payload) {
      const path = 'http://localhost:5000/user';
      const successMessageEl = document.getElementById('success-message');
      axios.put(path, payload, { headers: { 'x-access-token': this.token } })
        .then(() => {
          successMessageEl.style.display = 'block';
        })
        .catch((error) => {
          successMessageEl.style.display = 'none';
          if (error.response.status === 409) {
            const field = getFieldForErrorMessage(error.response.data.message);
            const message = `${field} already exists`;
            this.errors.push(message);
          }
        });
    },
    cancel(evt) {
      evt.preventDefault();
      this.$router.push('/home');
    },
  },
};

</script>

<style scoped>

#success-message {
  font-size: 1.5em;
  color: rgb(9, 205, 0);
  font-weight: bold;
  display: none;
}

.cancel-btn {
  width: 50%;
}

</style>
