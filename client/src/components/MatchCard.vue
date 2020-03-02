<template>
    <div>
        <b-row align-h="center">
            <b-card border-variant="light">
            <div class="card-body">
                <h3 class="card-title">{{ player1 }} vs. {{ player2 }}</h3>
                <h4 class="card-title">{{ game }}</h4>
            </div>
            </b-card>
        </b-row>
        <b-row align-h="center">
            <input class="btn btn-success btn-lg in-progress-submit" type="submit"
            value="Mark In Progress"/>
        </b-row>
    </div>
</template>

<script>
export default {
  name: 'MatchCard',
  props: ['player1', 'player2', 'game'],
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
  .card {
    width: 25rem;
  }
}
</style>
