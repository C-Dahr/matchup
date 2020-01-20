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

.navbar-brand {
    position: relative;
    background: url(./assets/matchuplogo_outline.png);
    width: 170px;
    left: 15px;
    background-size: contain;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
}
</style>
