<template>
  <perfect-scrollbar>
    <form class="m-3 pb-4 d-flex flex-column align-items-center padding" @submit.prevent="updateActivity">
      <div class="mb-3">
        <label for="titre" class="form-label"><h2>Titre</h2></label>
        <input
            type="text"
            class="form-control"
            placeholder="Nom de l'activité"
            id="titre"
            name="titre"
            v-model="this.updatableData.title"
            required
        />
      </div>
      <div class="mb-3" hidden>
        <label for="sport" class="form-label">Sport</label>
        <input type="text" name="sport" id="sport" v-model="this.activity.sport.name" disabled>
      </div>
      <div class="mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea
            class="form-control"
            id="description"
            maxlength="300"
            cols="30"
            rows="6"
            name="description"
            v-model="this.updatableData.description"
            required
        >
            </textarea>
      </div>
      <div class="mb-3" hidden>
        <label for="date" class="form-label">Date</label>
        <input type="text" name="date" id="date" :value="this.activity.event_date" disabled>
      </div>
      <div class="mb-3">
        <div class="form-check form-check-inline">
          <input
              class="form-check-input"
              type="checkbox"
              id="débutant"
              value="débutant"
              v-model="this.updatableData.levels"
          />
          <label class="form-check-label" for="débutant">débutant</label>
        </div>
        <div class="form-check form-check-inline">
          <input
              class="form-check-input"
              type="checkbox"
              id="amateur"
              value="amateur"
              v-model="this.updatableData.levels"
          />
          <label class="form-check-label" for="amateur">amateur</label>
        </div>
        <div class="form-check form-check-inline">
          <input
              class="form-check-input"
              type="checkbox"
              id="intermédiaire"
              value="intermédiaire"
              v-model="this.updatableData.levels"
          />
          <label class="form-check-label" for="intermédiaire"
          >intermédiaire</label
          >
        </div>
        <div class="form-check form-check-inline">
          <input
              class="form-check-input"
              type="checkbox"
              id="confirmé"
              value="confirmé"
              v-model="this.updatableData.levels"
          />
          <label class="form-check-label" for="confirmé">confirmé</label>
        </div>
        <div class="form-check form-check-inline">
          <input
              class="form-check-input"
              type="checkbox"
              id="expert"
              value="expert"
              v-model="this.updatableData.levels"
          />
          <label class="form-check-label" for="expert">expert</label>
        </div>
      </div>
      <div class="mb-3">
        <p>Se déroule : {{ this.activity.postcode }} | {{ this.activity.address }}</p>
      </div>
      <button type="submit" class="btn btn-primary">
        Modifier
      </button>
      <intersecting-circles-spinner
          v-if="loading"
          :animation-duration="1200"
          :size="70"
          color="#ff1d5e"
      />
    </form>
    <div v-if="this.message" class="alert alert-success" role="alert">
      L'activité a bien été modifiée !
    </div>
    <div v-if="this.error" class="alert alert-danger" role="alert">
      {{ this.error }}
    </div>
    <div>
      <p>Il y a {{this.activity.participants.length}} participants</p>
      <p v-for="participant in this.activity.participants" v-bind:key="participant.user.id">{{ participant.user.username }}</p>
    </div>
  </perfect-scrollbar>
</template>

<script>
import GestionActivities from "../services/activities.service.js";
import { IntersectingCirclesSpinner } from 'epic-spinners'
export default {
  name: "AcitityPage",
  components: {
    IntersectingCirclesSpinner
  },
  data() {
    return {
      updatableData: {
        title: "",
        description: "",
        levels: []
      },
      message: null,
      error: null,
      loading: false,
      activity: null,
      levels: null,
    };
  },
  methods: {
    logout() {
      this.$store.dispatch("logout");
      this.$router.push("/");
    },
    updateActivity() {
      this.loading = true;
      let requestData = {
        activity_id: this.$route.params.id,
        data_in: {
          title: this.updatableData.title,
          description: this.updatableData.description,
          event_date: this.activity.event_date,
          postcode: this.activity.postcode,
          address: this.activity.address,
          image: this.activity.image,
          sport_id: this.activity.sport.id,
          levels: this.updatableData.levels,
        }
      };
      GestionActivities.updateActivity(requestData).then((message) => {
        this.loading = false;
        this.message = message;
      }).catch((error) => {
        this.loading = false;
        this.error = error;
      })
    },
    eventChangeTitle(){
      const data = {title: "Activité"};
      this.$emit('updateTitleName', data);
    }
  },
  beforeCreate() {
    if (!this.isAuthenticated) {
      this.logout;
    }
  },
  beforeMount() {
    this.loading = true;
    GestionActivities.getActivityWithId(this.$route.params.id)
        .then((data) => {
          this.loading = false;
          this.activity = data;

          this.updatableData.title = this.activity.title;
          this.updatableData.description = this.activity.description;
          this.levels = JSON.stringify(this.activity.levels);
        })
        .catch((error) => {
          this.loading = false;
          this.error = error;
        });
  },
  mounted() {
    this.eventChangeTitle();
  }
}
</script>