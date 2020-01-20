<template>
  <div class="login">
    <h1><b>Login</b></h1>
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
  </div>
</template>

<script>


export default {
  name: 'Login',
  components: {},
};

</script>

<style>

h1 {
  padding: 1em;
}
.form-label {
  width: 10em;
  font-size: 1.25em;
}
#login-submit {
  width: 50%;
  background-color: #0066FF;
}
.form-group {
  display: flex;
  align-items: center;
  padding: 0.5em;
}
#login-form {
  width: 30%;
}

</style>
