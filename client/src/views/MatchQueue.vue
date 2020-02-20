<template>
  <div class="match-queue">
    <div class="form-title">
      <p>Event Name</p>
    </div>
    <b-container class="bv-example-row card-deck">
        <b-row class="card border-light">
            <div class="card-body">
                <h3 class="card-title">Bracket Two</h3>
            </div>
        </b-row>
        <b-row>
            <input class="btn btn-success btn-lg in-progress-submit" type="submit"
                 value="Mark In Progress"/>
        </b-row>
    </b-container>
  </div>
</template>


<style scoped>
.card {
    background-color: #0066FF !important;
    width: 30rem;
}
.card-title{
    font-weight: bold;
}
.card-deck {
  width: 60%;
  min-width: 500px;
  display: flex;
  justify-content: center;
}

</style>
