<template>
  <div class="review-players">
    <b-container>
      <div class="form-title">
        Review Players
        <input class="btn btn-primary btn-lg btn-next"
        onclick="onSubmit()" type="submit" value="Next"/>
      </div>
      <b-row align-h="between" align-v="center">
          <b-col sm-4>
              <div class="form-group d-flex justify-content-center">
                <label class="form-label">Melee Player</label>
                <model-select :options="melee"
                    v-model="selectedMelee"
                    placeholder="Select Player">
                </model-select>
            </div>
          </b-col>
          <b-col sm-4>
              <div class="form-group d-flex justify-content-center">
                <label class="form-label">Ultimate Player</label>
                <model-select :options="ultimate"
                    v-model="selectedUltimate"
                    placeholder="Select Player">
                </model-select>
            </div>
          </b-col>
          <b-col sm-4>
              <div class="form-group d-flex justify-content-center">
                  <input class="btn btn-primary btn-lg merge-form-submit"
                  type="submit" value="Merge"/>
              </div>
          </b-col>
      </b-row>
      <b-row align-h="between" align-v="center">
        <b-col sm-4>
          <h2 class="review-header">Melee</h2>
        </b-col>
        <b-col sm-4>
          <h2 class="review-header">Ultimate</h2>
        </b-col>
        <b-col sm-4>
          <h2 class="review-header">Both</h2>
        </b-col>
      </b-row>
      <b-row align-h="between" align-v="center">
        <b-col sm-4>
          <b-row align-h="between" align-v="center">
            <b-col sm-4>
              <div v-for="player in melee" class="player-name" v-bind:key="player">
                  {{ player.text }}
              </div>
            </b-col>
          </b-row>
        </b-col>
        <b-col sm-4>
          <b-row align-h="between" align-v="center">
            <b-col sm-4>
              <div v-for="player in ultimate" class="player-name" v-bind:key="player">
                  {{ player.text }}
              </div>
            </b-col>
          </b-row>
        </b-col>
        <b-col sm-4>
            <b-row align-h="between" align-v="center">
            <b-col sm-4>
              <div v-for="player in both" class="player-name" v-bind:key="player">
                  {{ player.name_1 }}/{{ player.name_2 }}
              </div>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios';
import { ModelSelect } from 'vue-search-select';

export default {
  name: 'ReviewPlayers',
  components: {
    ModelSelect,
  },
  data() {
    return {
      errors: [],
      token: this.$store.getters.getToken,
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
        { name_1: 'Scoot', name_2: 'Scoot', value: 'CamBlam' },
        { name_1: 'GreenTiger', name_2: 'GrnTgr', value: 'CamBlam' },
      ],
      player_data: {
        event_id: this.$store.getters.getEventID,
        players: [
          {
            id_1: '',
            id_2: '',
          },
        ],
      },
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {
        player_data: this.player_data,
      };
      this.mergePlayers(payload);
    },
    mergePlayers(payload) {
      const path = 'http://localhost:5000/event/players';
      axios.post(path, payload, { headers: { 'x-access-token': this.token } })
        .then(() => {
          this.$router.push('/matches');
        })
        .catch((error, msg) => {
          this.errors.push(error + msg);
        });
    },
  },
};
</script>

<style scoped>

.player-name {
  line-height: 2;
  font-size: 1.15em;;
}

.merge-form-submit {
  width: 30%;
  background-color: #0066FF !important;
  align-content: center;
}

.btn-next {
  background-color: #0066FF !important;
}

.review-header {
    text-decoration: underline;
}


@media only screen and (max-width: 600px) {
  .form-title{
    padding-bottom: 0;
  }

  #titleCard{
    padding-bottom: 1.5em;
  }

  .player-name {
    font-size: 0.85em;
  }

  .review-header {
    font-size: 1.5em;
  }
}

</style>
