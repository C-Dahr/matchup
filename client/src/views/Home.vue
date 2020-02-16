<template>
  <div class="home">
    <div class="col d-flex justify-content-center">
      <div class="card border-none border-0">
        <div class="card-body">
          <h1 class="card-title">Hi {{ username }}! Welcome to MatchUp</h1>
          <p class="card-text">
            To get started and make your own events,
            first you need to create brackets on Challonge.
            Once you’ve finished creating all the brackets you want for your event,
            just click the button below and we can get started!
          </p>
          <a href="createEvent" class="btn btn-primary btn-create btn-lg">Create Event</a>
        </div>
      </div>
    </div>
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

<style scoped>

.card {
  background-color: #404040;
  font-size: 2em;
  max-width: 50%;
  min-width: 300px;
}

.card-text {
  padding-top: 1em;
  padding-bottom: 1em;
}

.btn-create{
  background-color: #0066FF;
  color: white;
  border-color: white;
}

</style>
