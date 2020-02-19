<template>
  <div>
    <b-navbar toggleable="lg" id="navbar-main">
      <b-navbar-brand  href="/"></b-navbar-brand>
      <b-navbar-nav class="ml-auto" id="navbar-right">
        <b-collapse id="nav-collapse" is-nav>
          <b-nav-text id="welcome-msg">Welcome, {{ username }}</b-nav-text>
        </b-collapse>
        <b-nav-item-dropdown right>
          <template v-slot:button-content>
            <font-awesome-icon icon="user-circle" size="3x" style="color: white;"/>
          </template>
          <b-dropdown-item href="/editprofile">Profile</b-dropdown-item>
          <b-dropdown-item @click="logout" href="/login">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>
  </div>
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

#welcome-msg {
  color: white;
  font-size: 1.5em;
}

#navbar-right {
  padding-right: 2em;
}

.dropdown-toggle::after {
  content: none !important;
}

.navbar-collapse.collapse {
  padding: 0;
}

</style>
