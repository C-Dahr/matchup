<template>
  <div class="signup">
    <div class="form-title">
      <p>Sign Up</p>
    </div>
    <div class="d-flex justify-content-center">
      <form action="" method="post" id="signup-form">
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
                 name="apikey" required placeholder="Enter Challonge API Key"/>
                <span class="Error"></span>
            </div>
            <h4>Generate or find an existing API key for Challonge <b-link href="https://challonge.com/settings/developer" target="_blank">here</b-link></h4>
            <div class="form-group d-flex justify-content-center">
                <input class="btn btn-primary" type="submit"
                 value="Create Account" id="signup-submit"/>
            </div>
        </form>
      </div>
  </div>
</template>

<script>


export default {
  name: 'SignUp',
  components: {},
};

</script>

<style>

#signup-submit {
  width: 50%;
  background-color: #0066FF;
}
#signup-form {
  width: 30%;
  min-width: 300px;
}

</style>
