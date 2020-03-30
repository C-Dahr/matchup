<template>
  <div class="review-players">
    <b-container>
      <div class="form-title">
        Review Players
        <button class="btn btn-primary btn-lg btn-next"
            v-on:click="onSubmit()">
            Next
        </button>
      </div>
      <b-row align-h="between">
          <b-col sm-4>
              <div class="form-group d-flex justify-content-center">
                <label class="form-label">{{ bracket_1_name }}:</label>
                <model-list-select :list="bracket_1_players"
                    v-model="selected_bracket_1"
                    option-text="name"
                    option-value="player_id"
                    placeholder="Select Player">
                </model-list-select>
            </div>
          </b-col>
          <b-col sm-4>
              <div class="form-group d-flex justify-content-center">
                <label class="form-label">{{ bracket_2_name }}:</label>
                <model-list-select :list="bracket_2_players"
                    v-model="selected_bracket_2"
                    option-text="name"
                    option-value="player_id"
                    placeholder="Select Player">
                </model-list-select>
            </div>
          </b-col>
          <b-col sm-4>
              <div class="form-group d-flex justify-content-center">
                <button type="button" v-on:click="merge()"
                class="btn btn-primary btn-lg merge-form-submit">
                  Merge
                </button>
              </div>
          </b-col>
      </b-row>
      <b-row align-h="between">
        <b-col sm-4>
          <h2 class="review-header">{{ bracket_1_name }}</h2>
        </b-col>
        <b-col sm-4>
          <h2 class="review-header">{{ bracket_2_name }}</h2>
        </b-col>
        <b-col sm-4>
          <h2 class="review-header">Both</h2>
        </b-col>
      </b-row>
      <b-row align-h="between">
        <b-col sm-4>
          <b-row align-h="between" align-v="center">
            <b-col sm-4>
              <div v-for="player in bracket_1_players"
              class="player-name" v-bind:key="player.player_id">
                  {{ player.name }}
              </div>
            </b-col>
          </b-row>
        </b-col>
        <b-col sm-4>
          <b-row align-h="between" align-v="center">
            <b-col sm-4>
              <div v-for="player in bracket_2_players"
              class="player-name" v-bind:key="player.player_id">
                  {{ player.name }}
              </div>
            </b-col>
          </b-row>
        </b-col>
        <b-col sm-4>
            <b-row align-h="between" align-v="center">
            <b-col sm-4>
              <div v-for="player in both_players" class="player-name" v-bind:key="player.player_id">
                  {{ player.name }}
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
import { ModelListSelect } from 'vue-search-select';

export default {
  name: 'ReviewPlayers',
  components: {
    ModelListSelect,
  },
  data() {
    return {
      errors: [],
      token: this.$store.getters.getToken,
      bracket_1_name: {},
      bracket_2_name: {},
      selected_bracket_1: {},
      selected_bracket_2: {},
      bracket_1_players: [],
      bracket_2_players: [],
      both_players: [],
      players: [],
    };
  },
  created() {
    const path = `http://localhost:5000/event/players/${this.$store.getters.getEventID}`;
    axios.get(path, { headers: { 'x-access-token': this.token } })
      .then((response) => {
        const keys = Object.keys(response.data);
        const bracketName1 = keys[0];
        this.bracket_1_name = bracketName1;
        const bracketName2 = keys[1];
        this.bracket_2_name = bracketName2;
        this.bracket_1_players = response.data[keys[0]];
        this.bracket_2_players = response.data[keys[1]];
        this.both_players = response.data.both_brackets;
      })
      .catch((error, msg) => {
        this.errors.push(error + msg);
      });
  },
  methods: {
    merge() {
      if (this.notEmpty(this.selected_bracket_1) && this.notEmpty(this.selected_bracket_2)) {
        this.players.push({
          id_1: this.selected_bracket_1.player_id,
          id_2: this.selected_bracket_2.player_id,
        });
        this.both_players.push({
          bracket_id: this.selected_bracket_1.bracket_id,
          name: `${this.selected_bracket_1.name} / ${this.selected_bracket_2.name}`,
          player_id: this.selected_bracket_1.player_id,
        });
        const index1 = this.bracket_1_players.indexOf(this.selected_bracket_1);
        if (index1 > -1) {
          this.bracket_1_players.splice(index1, 1);
        }
        const index2 = this.bracket_2_players.indexOf(this.selected_bracket_2);
        if (index2 > -1) {
          this.bracket_2_players.splice(index2, 1);
        }
        this.selected_bracket_1 = {};
        this.selected_bracket_2 = {};
      }
    },
    notEmpty(obj) {
      return Object.keys(obj).length > 0;
    },
    onSubmit() {
      const payload = {
        players: this.players,
      };
      this.mergePlayers(payload);
    },
    mergePlayers(payload) {
      const path = `http://localhost:5000/event/players/${this.$store.getters.getEventID}`;
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
