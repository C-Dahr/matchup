<template>
  <div class="create-event">
    <div class="form-title">
      <p>Create Event</p>
    </div>
    <div class="form-error-list" v-if="errors.length">
      <ul class="form-error">
        <li v-for="error in errors" v-bind:key="error">{{ error }}</li>
      </ul>
    </div>
    <div class="d-flex justify-content-center">
      <form @submit="onSubmit" method="post" class="event-form">
            <div id ="event-input" class="form-group d-flex justify-content-center">
              <label class="form-label">Event Name</label>
              <input class="form-control" type="text"
              name="eventname" v-model="eventForm.event_name"
              required placeholder="Enter Event Name"/>
              <span class="Error"></span>
            </div>
            <div class="card-deck">
                <div class="card border-light">
                    <div class="card-body">
                        <h3 class="card-title">Bracket One</h3>
                        <div class="form-group d-flex justify-content-left">
                            <label class="form-label">Select Bracket</label>
                            <b-form-select v-model="eventForm.brackets[0].bracket_id"
                            :options="options"></b-form-select>
                        </div>
                        <div class="form-group d-flex justify-content-left">
                            <label class="form-label">Number of setups</label>
                            <input class="form-control" type="text"
                            v-model="eventForm.brackets[0].number_of_setups"
                            required placeholder="Enter Number of Setups"/>
                            <span class="Error"></span>
                        </div>
                    </div>
                </div>
                <div class="card border-light " text-white>
                    <div class="card-body">
                        <h3 class="card-title">Bracket Two</h3>
                        <div class="form-group d-flex justify-content-left">
                            <label class="form-label">Select Bracket</label>
                            <b-form-select v-model="eventForm.brackets[1].bracket_id"
                            :options="options"></b-form-select>
                        </div>
                        <div class="form-group d-flex justify-content-left">
                            <label class="form-label">Number of setups</label>
                            <input class="form-control" type="text"
                            v-model="eventForm.brackets[1].number_of_setups"
                            required placeholder="Enter Number of Setups"/>
                            <span class="Error"></span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="form-group d-flex justify-content-center">
                <input class="btn btn-primary btn-lg event-form-submit" type="submit"
                 value="Next"/>
            </div>
        </form>
      </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      errors: [],
      eventForm: {
        event_name: '',
        brackets: [
          {
            bracket_id: '',
            number_of_setups: '',
          },
          {
            bracket_id: '',
            number_of_setups: '',
          },
        ],
      },
      tournaments: [],
      options: [],
      token: this.$store.getters.getToken,
    };
  },
  name: 'CreateEvent',
  created() {
    const path = 'http://localhost:5000/challonge';
    axios.get(path, { headers: { 'x-access-token': this.token } })
      .then((response) => {
        this.tournaments = response.data.tournaments;
        this.tournaments.forEach(
          tournament => this.options.push({ value: tournament.id, text: tournament.name }),
        );
      })
      .catch(() => {
        this.errors.push('Invalid Challonge credentials. Ensure API key is correct');
      });
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      this.errors = [];
      if (this.eventForm.brackets[0].bracket_id === this.eventForm.brackets[1].bracket_id) {
        this.errors.push('Can not choose the same bracket twice');
      } else {
        const payload = {
          event_name: this.eventForm.event_name,
          brackets: [
            {
              bracket_id: this.eventForm.brackets[0].bracket_id,
              number_of_setups: this.eventForm.brackets[0].number_of_setups,
            },
            {
              bracket_id: this.eventForm.brackets[1].bracket_id,
              number_of_setups: this.eventForm.brackets[1].number_of_setups,
            },
          ],
        };
        this.createEvent(payload);
      }
    },
    createEvent(payload) {
      const path = 'http://localhost:5000/event';
      axios.post(path, payload, { headers: { 'x-access-token': this.token } })
        .then(() => {
          this.$router.push('/home');
        })
        .catch((error) => {
          if (error.response.status === 400) {
            this.errors.push('Form is missing fields');
          } else if (error.response.status === 401) {
            this.errors.push('Invalid bracket ID');
          }
        });
    },
  },
};
</script>

<style scoped>
.card {
    background-color: #0066FF !important;
    width: 30rem;
}
.card-title{
    font-weight: bold;
}
.event-form {
  width: 60%;
  min-width: 500px;
}
@media only screen and (max-width: 600px) {
  .event-form {
    width: 95%;
    min-width: auto;
  }
  .card {
    width: auto;
}
}
.event-form-submit {
  width: 30%;
  background-color: #0066FF !important;
  align-content: center;
  margin-top: 10px;
}
#event-input {
  max-width: 800px;
}

</style>
