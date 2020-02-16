<template>
  <div class="home">
    Welcome {{ username }}
  </div>
</template>

<script>

export default {
  name: 'home',
  computed: {
    username() {
      return this.$store.state.username;
    },
  },
};
</script>
