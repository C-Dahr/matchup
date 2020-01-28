<template>
  <div class="login">
    <div class="form-title">
      <p>Login</p>
    </div>
    <div class="d-flex justify-content-center">
      <form action="" method="post" id="login-form">
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Username:</label>
              <input class="form-control" type="text"
              name="fullname" required placeholder="Enter Username"/>
              <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Password:</label>
              <input class="form-control" type="password"
                 name="password" required placeholder="Enter Password"/>
                <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-center">
                <input class="btn btn-primary" type="submit"
                 value="Sign in" id="login-submit"/>
            </div>
        </form>
      </div>
      <h2>Don't have an account? <router-link to="/signup">Sign Up</router-link></h2>
  </div>
</template>

<script>


export default {
  name: 'Login',
  components: {},
};

</script>

<style>

#login-submit {
  width: 50%;
  background-color: #0066FF;
}
#login-form {
  width: 30%;
  min-width: 300px;
}


</style>
