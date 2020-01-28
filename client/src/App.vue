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
}
</style>
