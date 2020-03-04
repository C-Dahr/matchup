<template>
    <div>
        <b-row align-h="center">
            <b-card border-variant="light">
            <div class="card-body">
                <h3 class="card-title">{{ player1 }} vs. {{ player2 }}</h3>
                <h4 class="card-title">{{ game }}</h4>
            </div>
            </b-card>
            <button v-if=loggedIn class="btn btn-lg in-progress-submit" type="submit">
            Mark In<br/>Progress</button>
        </b-row>
        <b-row align-h="center">
        </b-row>
    </div>
</template>

<script>
export default {
  name: 'MatchCard',
  props: ['player1', 'player2', 'game'],
  data() {
    return {
      loggedIn: this.$store.getters.isLoggedIn,
    };
  },
};
</script>

<style scoped>
.card {
  background-color: #0066FF;
  width: 50rem;
  margin: 0;
  margin-bottom: 20px;
  margin-right: 10px;
}
.card-title{
    font-weight: bold;
}
.in-progress-submit {
  margin-bottom: 20px;
  background-color: rgb(98, 187, 120);
  color: white;
}
.in-progress-submit:hover {
  background-color: rgb(67, 182, 96);
  color: white;
}
.in-progress-submit:focus {
  color: white;
}
@media only screen and (max-width: 600px) {
  .card {
    width: 25rem;
  }
}
</style>
