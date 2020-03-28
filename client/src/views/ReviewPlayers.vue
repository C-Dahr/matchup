<template>
  <div class="review-players">
    <b-container>
      <div class="form-title">
        <p>Review Players</p>
      </div>
      <b-row align-h="between" align-v="center">
        <b-col sm-4>
          <h2>Melee</h2>
        </b-col>
        <b-col sm-4>
          <h2>Ultimate</h2>
        </b-col>
        <b-col sm-4>
          <h2>Both</h2>
        </b-col>
      </b-row>
    </b-container>
    <b-container>
      <b-row align-h="between" align-v="center">
        <b-col sm-4>
          <b-row align-h="between" align-v="center">
            <b-col sm-4></b-col>
            <b-col sm-4>
              <b-form-checkbox
                size="lg"
                v-for="player in melee"
                v-model="selectedMelee"
                :key="player.value"
                :value="player.value"
                name="melee-player"
              >
              {{ player.text }}
              </b-form-checkbox>
            </b-col>
            <b-col sm-4></b-col>
          </b-row>
        </b-col>
        <b-col sm-4>
          <b-row align-h="between" align-v="center">
            <b-col sm-4></b-col>
            <b-col sm-4>
              <b-form-checkbox
                size="lg"
                v-for="player in ultimate"
                v-model="selectedUltimate"
                :key="player.value"
                :value="player.value"
                name="ultimate-player"
              >
              {{ player.text }}
              </b-form-checkbox>
            </b-col>
            <b-col sm-4></b-col>
          </b-row>
        </b-col>
        <b-col sm-4>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>

// import draggable from 'vuedraggable';

export default {
  name: 'ReviewPlayers',
  components: {
    // draggable,
  },
  data() {
    return {
      errors: [],
      loggedIn: this.$store.getters.isLoggedIn,
      selectedMelee: [],
      selectedUltimate: [],
      melee: [
        { text: 'DannyGranE', value: 'DannyGranE' },
        { text: 'ZachAtk', value: 'ZachAtk' },
      ],
      ultimate: [
        { text: 'CamBlam', value: 'CamBlam' },
        { text: 'TaylerMailr', value: 'TaylerMailr' },
      ],
      both: [
      ],
    };
  },
  computed: {
    meleeCount() {
      return this.selectedMelee.length === 1;
    },
    UltCount() {
      return this.selectedUltimate.length === 1;
    },
  },
};
</script>

<style scoped>

.custom-checkbox.b-custom-control-lg, .input-group-lg .custom-checkbox {
  text-align: left !important;
  line-height: 2;
}

.custom-checkbox {
  display: flex;
  align-items: center;
}

@media only screen and (max-width: 600px) {
  .form-title{
    padding-bottom: 0;
  }

  #titleCard{
    padding-bottom: 1.5em;
  }
}

</style>
