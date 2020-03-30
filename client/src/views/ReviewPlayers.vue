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
                <label class="form-label">Melee Player</label>
                <model-list-select :list="melee"
                    v-model="selectedMelee"
                    option-text="name"
                    option-value="player_id"
                    placeholder="Select Player">
                </model-list-select>
            </div>
          </b-col>
          <b-col sm-4>
              <div class="form-group d-flex justify-content-center">
                <label class="form-label">Ultimate Player</label>
                <model-list-select :list="ultimate"
                    v-model="selectedUltimate"
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
          <h2 class="review-header">Melee</h2>
        </b-col>
        <b-col sm-4>
          <h2 class="review-header">Ultimate</h2>
        </b-col>
        <b-col sm-4>
          <h2 class="review-header">Both</h2>
        </b-col>
      </b-row>
      <b-row align-h="between">
        <b-col sm-4>
          <b-row align-h="between" align-v="center">
            <b-col sm-4>
              <div v-for="player in melee" class="player-name" v-bind:key="player.player_id">
                  {{ player.name }}
              </div>
            </b-col>
          </b-row>
        </b-col>
        <b-col sm-4>
          <b-row align-h="between" align-v="center">
            <b-col sm-4>
              <div v-for="player in ultimate" class="player-name" v-bind:key="player.player_id">
                  {{ player.name }}
              </div>
            </b-col>
          </b-row>
        </b-col>
        <b-col sm-4>
            <b-row align-h="between" align-v="center">
            <b-col sm-4>
              <div v-for="player in both" class="player-name" v-bind:key="player.player_id">
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
      selectedMelee: {},
      selectedUltimate: {},
      melee: [],
      ultimate: [],
      both: [],
      players: [],
    };
  },
  created() {
    const path = `http://localhost:5000/event/players/${this.$store.getters.getEventID}`;
    axios.get(path, { headers: { 'x-access-token': this.token } })
      .then((response) => {
        const keys = Object.keys(response.data);
        this.melee = response.data[keys[0]];
        this.ultimate = response.data[keys[1]];
        this.both = response.data.both_brackets;
        this.player_list = response.data;
      })
      .catch((error, msg) => {
        this.errors.push(error + msg);
      });
  },
  methods: {
    merge() {
      if (this.notEmptyObject(this.selectedMelee) && this.notEmptyObject(this.selectedUltimate)) {
        this.players.push({
          id_1: this.selectedMelee.player_id,
          id_2: this.selectedUltimate.player_id,
        });
        this.both.push({
          bracket_id: this.selectedMelee.bracket_id,
          name: `${this.selectedMelee.name} / ${this.selectedUltimate.name}`,
          player_id: this.selectedMelee.player_id,
        });
        const indexMelee = this.melee.indexOf(this.selectedMelee);
        if (indexMelee > -1) {
          this.melee.splice(indexMelee, 1);
        }
        const indexUlt = this.ultimate.indexOf(this.selectedUltimate);
        if (indexUlt > -1) {
          this.ultimate.splice(indexUlt, 1);
        }
        this.selectedMelee = {};
        this.selectedUltimate = {};
      }
    },
    notEmptyObject(obj) {
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
