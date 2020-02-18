<template>
    <nav class="navbar navbar-expand-sm" id="navbar-main">
      <!-- Brand -->
      <a class="navbar-brand" href="/"></a>

      <!-- Links -->
      <ul class="navbar-nav ml-auto">
        <li class="nav-item" v-if="!isLoggedIn">
          <a class="nav-link" href="/login">Login</a>
        </li>
        <li class="nav-item" v-if="isLoggedIn">
          <div id="welcome-msg" >Welcome, {{ username }}</div>
          <a class="nav-link" @click="logout" href="/login">Sign Out</a>
          <a class="nav-link" @click="logout" href="/editprofile">Edit Profile</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="profile" v-if="isLoggedIn">
            <font-awesome-icon icon="user-circle" size="3x"/>
          </a>
        </li>
      </ul>
    </nav>
</template>

<script>

export default {
  name: 'Navbar',
  computed: {
    isLoggedIn() { return this.$store.getters.isLoggedIn; },
    username() { return this.$store.state.username; },
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
        .then(() => {
          this.$router.push('/login');
        });
    },
  },
};

</script>

<style>

.navbar-brand {
    position: relative;
    background: url(../assets/matchuplogo_outline.png);
    width: 170px;
    left: 15px;
    background-size: contain;
    padding: 0;
}

#navbar-main {
    background-color: #0066FF;
}

.navbar .nav-link {
    color: white;
    font-size: 1.25em;
    padding-top: 0;
    padding-bottom: 0;
    text-align: right;
}

.navbar-nav {
  padding-right: 1em;
}

.nav-item {
  padding-right: 1em;
}

#welcome-msg {
  font-size: 1.5em;
}
</style>
