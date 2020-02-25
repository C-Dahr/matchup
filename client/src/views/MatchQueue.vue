<template>
  <div class="match-queue">
    <b-container>
      <b-row id="titleCard" align-h="between" align-v="center">
        <b-col sm="2"/>
        <b-col sm="8">
          <div class="form-title">
            <p>Event Name <a href="editEvent"><font-awesome-icon icon="cog" size=""/></a></p>
          </div>
        </b-col>
        <b-col sm="2">
          <input class="btn btn-danger" type="submit" value="End Event"/>
        </b-col>
      </b-row>
    </b-container>
    <b-container>
      <div v-for="matchData in matchData" class="match" v-bind:key="matchData">
        <b-row align-h="center">
          <b-card border-variant="light">
            <div class="card-body">
              <h3 class="card-title">{{ matchData.player1}} vs. {{matchData.player2}}</h3>
              <h4 class="card-title">{{ matchData.game}}</h4>
            </div>
          </b-card>
        </b-row>
        <b-row align-h="center">
          <input class="btn btn-success btn-lg in-progress-submit" type="submit"
          value="Mark In Progress"/>
        </b-row>
      </div>
    </b-container>
  </div>
</template>

<script>
// import axios from 'axios';

export default {
  data() {
    return {
      errors: [],
      maxVisibleMatches: 5,
      matchData: [
        { player1: 'ZachAtk', player2: 'CamBlam', game: 'Game 1' },
        { player1: 'DannyGranE', player2: 'TaylerMailr', game: 'Game 2' },
      ],
    };
  },
};
</script>

<style scoped>
.card {
  background-color: #0066FF;
  width: 50rem;
  margin: 0;
}
.card-title{
    font-weight: bold;
}
.in-progress-submit {
  margin-top: 10px;
  margin-bottom: 20px;
}

@media only screen and (max-width: 600px) {
  .form-title{
    padding-bottom: 0;
  }

  #titleCard{
    padding-bottom: 1.5em;
  }

  .card {
    width: 25rem;
  }
}

</style>
