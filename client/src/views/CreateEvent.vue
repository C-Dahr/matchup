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
            <div class="form-group d-flex justify-content-left">
              <label class="form-label">Event Name</label>
              <input class="form-control" type="text"
              name="eventname" v-model="eventForm.event_name"
              required placeholder="Enter Event Name"/>
              <span class="Error"></span>
            </div>
            <div class="card-deck">
                <div class="card border-light " text-white>
                    <div class="card-body">
                        <h3 class="card-title">Bracket One</h3>
                        <div class="form-group d-flex justify-content-left">
                            <label class="form-label">Select Bracket</label>
                            <div class="dropdown">
                                <button class="btn btn-secondary dropdown-toggle" type="button"
                                id="dropdownMenuButton" data-toggle="dropdown"
                                aria-haspopup="true" aria-expanded="false">
                                    Bracket
                                </button>
                                <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                    <a class="dropdown-item" href="#">Action</a>
                                    <a class="dropdown-item" href="#">Another action</a>
                                    <a class="dropdown-item" href="#">Something else here</a>
                                </div>
                            </div>
                        </div>
                        <div class="form-group d-flex justify-content-left">
                            <label class="form-label">Number of setups</label>
                            <input class="form-control" type="text"
                            name="setups1" v-model="eventForm.setups1"
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
                            <div class="dropdown">
                                <button class="btn btn-secondary dropdown-toggle" type="button"
                                id="dropdownMenuButton" data-toggle="dropdown"
                                aria-haspopup="true" aria-expanded="false">
                                    Bracket
                                </button>
                                <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                    <a class="dropdown-item" href="#">Action</a>
                                    <a class="dropdown-item" href="#">Another action</a>
                                    <a class="dropdown-item" href="#">Something else here</a>
                                </div>
                            </div>
                        </div>
                        <div class="form-group d-flex justify-content-left">
                            <label class="form-label">Number of setups</label>
                            <input class="form-control" type="text"
                            name="setups1" v-model="eventForm.setups1"
                            required placeholder="Enter Number of Setups"/>
                            <span class="Error"></span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="form-group d-flex justify-content-center">
                <input class="btn btn-primary account-form-submit" type="submit"
                 value="Next"/>
            </div>
        </form>
      </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      errors: [],
      eventForm: {
        event_name: '',
        bracket1: '',
        setups1: '',
        bracket2: '',
        setups2: '',
      },
    };
  },
  name: 'CreateEvent',
};
</script>

<style>
.card {
    background-color: #0066FF !important;
    width: 30rem;
}
.card-title{
    font-weight: bold;
}

</style>
