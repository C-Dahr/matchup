<template>
    <div>
        <b-row align-h="center">
            <b-card border-variant="light">
            <div class="card-body">
                <h3 class="card-title">{{ player1 }} vs. {{ player2 }}</h3>
                <h4 class="card-title">{{ game }}</h4>
            </div>
            </b-card>
            <button v-if=loggedIn class="btn btn-lg in-progress-submit"
            @click="inProgress" type="button">
            Mark In<br/>Progress</button>
        </b-row>
        <b-row align-h="center">
        </b-row>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MatchCard',
  props: ['player1', 'player2', 'game', 'bracket_id', 'match_id'],
  data() {
    return {
      loggedIn: this.$store.getters.isLoggedIn,
      token: this.$store.getters.getToken,
      eventID: this.$store.getters.getEventID,
    };
  },
  methods: {
    inProgress(evt) {
      evt.preventDefault();
      const payload = {
        event_id: this.eventID,
        bracket_id: this.bracket_id,
        match_id: this.match_id,
      };
      const path = 'http://localhost:5000/challonge/match/start';
      axios.put(path, payload, { headers: { 'x-access-token': this.token } })
        .then(() => {
          this.$parent.refresh();
        })
        .catch(() => {
          this.errors.push('Invalid Challonge credentials. Ensure API key is correct');
          this.link = true;
        });
    },
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
