<template>
  <div class="editpassword">
    <div class="form-title">
      <p>Edit Password</p>
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
              <label class="form-label">Current Password</label>
              <input class="form-control" type="password"
              name="current_password" v-model="editPasswordForm.current_password"
              required placeholder="Enter Current Password"/>
              <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">New Password</label>
              <input class="form-control" type="password"
              name="new_password" v-model="editPasswordForm.new_password"
              required placeholder="Enter New Password"/>
              <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Confirm New Password</label>
              <input class="form-control" type="password"
              name="confirm_new_password" v-model="editPasswordForm.confirm_new_password"
              placeholder="Confirm New Password"/>
              <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-center">
                <input class="btn btn-primary account-form-submit" type="submit"
                 value="Change Password"/>
            </div>
            <div class="form-group d-flex justify-content-center">
                <input class="btn btn-secondary cancel-btn" type="button"
                 value="Back to Edit Profile" @click="cancel"/>
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
      editPasswordForm: {
        current_password: '',
        new_password: '',
        confirm_new_password: '',
      },
    };
  },
  computed: {
    token() { return this.$store.state.userToken; },
  },
  name: 'EditPassword',
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      this.errors = [];
      const successMessageEl = document.getElementById('success-message');
      if (this.editPasswordForm.new_password !== this.editPasswordForm.confirm_new_password) {
        this.editPasswordForm.new_password = '';
        this.editPasswordForm.confirm_new_password = '';
        successMessageEl.style.display = 'none';
        this.errors.push('Passwords do not match');
      } else {
        const payload = {
          current_password: this.editPasswordForm.current_password,
          new_password: this.editPasswordForm.new_password,
        };
        this.updatePassword(payload);
      }
    },
    updatePassword(payload) {
      const path = 'http://localhost:5000/user/password';
      const successMessageEl = document.getElementById('success-message');
      axios.put(path, payload, { headers: { 'x-access-token': this.token } })
        .then(() => {
          this.editPasswordForm.current_password = '';
          this.editPasswordForm.new_password = '';
          this.editPasswordForm.confirm_new_password = '';
          successMessageEl.style.display = 'block';
        })
        .catch((error) => {
          successMessageEl.style.display = 'none';
          if (error.response.status === 401) {
            this.errors.push('Current password is incorrect');
          }
        });
    },
    cancel(evt) {
      evt.preventDefault();
      this.$router.push('/editprofile');
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

</style>
