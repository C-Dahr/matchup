<template>
  <div class="home">
    Welcome {{ token }}
  </div>
</template>

<script>

export default {
  computed: {
    token() {
      return this.$store.state.userToken;
    },
  },
};
</script>
