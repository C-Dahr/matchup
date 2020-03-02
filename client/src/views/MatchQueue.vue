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
        <MatchCard :player1="data.player1" :player2="data.player2" :game="data.game">
        </MatchCard>
      </div>
    </b-container>
  </div>
</template>

<script>
import MatchCard from '../components/MatchCard.vue';

export default {
  name: 'MatchQueue',
  components: {
    MatchCard,
  },
  data() {
    return {
      errors: [],
      maxVisibleMatches: 5,
      loggedIn: this.$store.getters.isLoggedIn,
      matchData: [
        { player1: 'ZachAtk', player2: 'CamBlam', game: 'Game 1' },
        { player1: 'DannyGranE', player2: 'TaylerMailr', game: 'Game 2' },
        { player1: 'ZachAtk', player2: 'TaylerMailr', game: 'Game 2' },
      ],
    };
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
