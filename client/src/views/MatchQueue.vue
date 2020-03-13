<template>
  <div class="match-queue">
    <b-container>
      <b-row id="titleCard" align-h="between" align-v="center">
        <b-col sm="2"/>
        <b-col sm="8">
          <div class="form-title">
            <p>Event Name
              <a v-if=loggedIn href="editEvent"><font-awesome-icon icon="cog" size=""/></a>
            </p>
          </div>
        </b-col>
        <b-col sm="2">
          <input class="btn btn-danger" v-if=loggedIn type="submit" value="End Event"/>
        </b-col>
      </b-row>
    </b-container>
    <b-container>
      <div v-for="data in matchData" class="match" v-bind:key="data">
        <MatchCard :player1="data.player1.name" :player2="data.player2.name"
        :game="data.bracket.game_name">
        </MatchCard>
      </div>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios';
import MatchCard from '../components/MatchCard.vue';

export default {
  name: 'MatchQueue',
  components: {
    MatchCard,
  },
  data() {
    return {
      errors: [],
      loggedIn: this.$store.getters.isLoggedIn,
      token: this.$store.getters.getToken,
      eventID: this.$store.getters.getEventID,
      matchData: [],
    };
  },
  created() {
    const path = `http://localhost:5000/challonge/matches/${this.eventID}`;
    axios.get(path, { headers: { 'x-access-token': this.token } })
      .then((response) => {
        this.matchData = response.data;
      })
      .catch(() => {
        this.errors.push('Invalid Challonge credentials. Ensure API key is correct');
        this.link = true;
      });
  },
};
</script>

<style scoped>

@media only screen and (max-width: 600px) {
  .form-title{
    padding-bottom: 0;
  }

  #titleCard{
    padding-bottom: 1.5em;
  }
}

</style>
