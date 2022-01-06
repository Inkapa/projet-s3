<template>
  <!-- barre de recherche -->
  <perfect-scrollbar>
    <div class="d-flex flex-column justify-content-center align-items-center pt-3">
      <h4 class="fw-bold">Filtres : </h4>
      <div class="d-flex mb-3 align-items-center">
        <label class="form-label">Code Postal</label>
        <input class="form-control" type="text" v-model="this.activitiesRequestInfo.postcode">
      </div>
      <div class="d-flex mb-3 justify-content-center justify-content-between align-items-center">
        <label class="form-label px-3">Sport</label>
        <select class="form-select" aria-label="Select pour le sport" v-model="this.activitiesRequestInfo.sport_id">
          <option v-for="sport in this.sports" v-bind:key="sport.id" :value="sport.id">
            {{ sport.name }}
          </option>
        </select>
      </div>
      <button @click="getActivities()" class="btn btn-primary m-3">Chercher</button>
      <button @click="resetSearch()" class="btn btn-danger">Reset</button>
      <ScalingSquaresSpinner class="align-self-center m-5"
         v-if="loading"
         :animation-duration="2500"
         :size="65"
         color="#ff1d5e"
      />
    </div>

    <div v-show="this.message" class="alert alert-success mt-3" ref="alert" role="alert">
      {{ this.message }}
    </div>
    <div v-show="this.error" class="alert alert-danger mt-3" role="alert">
      {{ this.error }}
    </div>
    <div class="d-flex flex-column flex-wrap padding" v-if="activities">

        <Activity
            v-for="activity in activities"
            v-bind:key="activity.id"
            :activity-info="activity"
            :participant="true"
            @remove="removeActivity"

        />
    </div>
  </perfect-scrollbar>
</template>

<script>
import Activity from "../components/Activity.vue";
import GestionActivities from "../services/activities.service.js";
import { ScalingSquaresSpinner  } from 'epic-spinners'
export default {
  name: "Home",
  components: {
    Activity,
    ScalingSquaresSpinner,
  },
  emits: ['updateTitleName'],
  data() {
    return {

      activitiesRequestInfo: {
        active: true,
        postcode: "51100",
        offset: 0
      },
      activities: null,
      message: null,
      error: null,
      loading: false,
      sports: null,
      levels: ["débutant", "amateur", "intermédiaire", "confirmé", "expert"],
    };
  },
  methods: {
    getActivities() {
      this.loading = true;
      this.activities = {};
      GestionActivities.getActivitiesBySearch(this.activitiesRequestInfo).then((data) => {
          // setTimeout(() => {}, 2000);
          this.loading = false; this.activities = data;
        })
        .catch((error) => {
          this.loading = false;
          this.error = error;
        });
    },
    resetSearch() {
      this.activitiesRequestInfo = {postcode: "51100",offset: 0, limit: 10,};
      this.getActivities();
    },
    logout() {
      this.$store.dispatch("logout");
      this.$router.push("/");
    },
    eventChangeTitle(){
      const data = {title: "Home", id: 1};
      this.$emit('updateTitleName', data);
    },
    removeActivity(id, message){
      this.message = message
      this.activities = this.activities.filter(activity => activity.id !== id)
      this.$refs.alert.classList.add('fade-out')
      this.$refs.alert.onanimationend = () => {
        this.message = null
        this.$refs.alert.classList.remove('fade-out')
      }
    }
  },
  beforeCreate() {
    if (!this.isAuthenticated) {
      this.logout;
    }
  },
  beforeMount() {
    //récup les activités de l'user et les mets sous forme de card
    this.loading = true;
    this.getActivities();

    GestionActivities.getSports()
      .then((sports) => {
        this.sports = sports;
      })
      .catch((error) => {
        this.message = error;
    });
  },
  mounted() {
    this.eventChangeTitle();
  }
};
</script>
<style scoped>
.padding {
  padding-bottom: 50px;
}
</style>