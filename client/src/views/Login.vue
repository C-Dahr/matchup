<template>
  <div class="login">
    <div class="form-title">
      <p>Login</p>
    </div>
    <div class="d-flex justify-content-center">
      <form action="" method="post" class="account-form">
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Username</label>
              <input class="form-control" type="text"
              name="fullname" required placeholder="Enter Username"/>
              <span class="Error"></span>
            </div>
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Password</label>
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


export default {
  name: 'Login',
};

</script>
