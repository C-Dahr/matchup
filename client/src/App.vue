<template>
  <div id="app">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <Navbar/>
    <router-view/>
  </div>
</template>

<script>

import Navbar from './components/Navbar.vue';

export default {
  name: 'Login',
  components: {
    Navbar,
  },
};

</script>
<style>

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
}
.form-title {
  font-weight: bold;
  font-size: 3em;
  padding: 1em;
}
.form-group {
  display: flex;
  align-items: center;
  padding: 0.5em;
}
.form-label {
  width: 10em;
  font-size: 1.25em;
  text-align: right;
  margin-right: 1em;
}
.form-error-list {
  font-size: 1.5em;
  color: rgb(253, 72, 72);
  font-weight: bold;
}
.form-error {
  text-align: center;
  list-style-position: inside;
}
.account-form-submit {
  width: 50%;
  background-color: #0066FF !important;
}
.account-form {
  width: 30%;
  min-width: 300px;
}
</style>
