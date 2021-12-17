<template>
  <div v-if="this.message" class="alert alert-success mt-3" role="alert">
    {{ this.message }}
  </div>
  <div v-if="this.error" class="alert alert-danger mt-3" role="alert">
    {{ this.error }}
  </div>
  <div class="card text-center m-3 flex-grow-1 activity">
    <div class="card-header">{{ this.activityInfo.title }}</div>
    <div class="card-body">
      <h5 class="card-title">{{ this.activityInfo.sport.name }}</h5>
      <p class="card-text">
        {{ this.activityInfo.description }}
      </p>
      <p class="card-text">
        <strong>Se déroule le :</strong> {{ this.activityInfo.event_date }}
      </p>
      <p class="card-text">
        <strong>Niveau : </strong>
        <span class="badge rounded-pill bg-success mx-1" v-for="level in this.activityInfo.levels" v-bind:key="level.id">{{ level.level }}</span>
      </p>
      <!--Div pour pouvoir participer-->
      <div v-if="participant && !userParticipe">
        <button @click="addMyParticipation" class="btn btn-light float-center mt-1 mb-1" :disabled="userParticipe">Participer</button>
        <select name="levels" id="levels" v-model="this.levelSelected" class="form-select mb-3 mt-3" required :disabled="userParticipe">
          <option v-for="level in this.activityInfo.levels" :value="level.level" v-bind:key="level.id">{{ level.level }}</option>
        </select>
      </div>
      <div v-else class="mb-3">
        <p>Vous participez à cette activité.</p>
        <button v-if="!owner" @click="removeMyParticipation" class="btn btn-danger"> Annuler ? </button>
      </div>
      <p v-if="!loading" class="pt-2">Il y a déjà {{ this.activityInfo.participant_count }} participants !</p>

      <!--Div pour modifier/supprimer l'activité-->
      <div v-if="owner">
        <button @click="modifActivity" class="btn btn-primary float-start">Modifier</button>
        <button @click="deleteActivity" class="btn btn-danger float-end">Supprimer</button>
      </div>
    </div>
    <div class="card-footer text-light">{{ this.activityInfo.postcode }} - {{ this.activityInfo.address }}</div>
  </div>
</template>

<script>
import GestionActivities from "../services/activities.service.js";
import GestionParticipations from "../services/participations.service.js";
export default {
  name: "Activity",
  props: {
    activityInfo: Object,
    participant: {default: false, type: Boolean},
    owner: {default: false, type: Boolean},
  },
  data() {
    return {
      id: this.activityInfo.id,
      loading: false,
      error: null,
      message: null,
      levelSelected: null,
      userParticipe: false
    }
  },
  computed: {
  },
  methods: {
    modifActivity() {
      this.$router.push({ name: 'ActivityPage', params: { id: this.id }});
    },
    deleteActivity() {
      GestionActivities.deleteActivity(this.id).then(() => {
        this.message = "L'activité a bien été supprimée.";
      }).catch((error) => {
        this.error = error;
      });
    },
    addMyParticipation() {
      let reqData = {level: this.levelSelected, activity_id: this.activityInfo.id};
      GestionParticipations.addMyParticipation(reqData).then(() => {
        this.message = "Vous êtes bien inscrit à cette activité !";
        this.userParticipe = true;
      }).catch(() =>{
        this.error = "Veuillez chosir votre niveau";
      })
    },
    removeMyParticipation() {
      GestionParticipations.removeMyParticipation(this.id).then(() => {
        this.message = "Vous êtes bien désinscrit de cette activité !";
        this.$forceUpdate();
      }).catch((error) =>{
        this.error = error;
      });
    }
  },
  beforeMount() {

  }
};
</script>
<style scoped>
.activity{
  box-shadow: -3px 9px 20px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
  background-color: rgb(74, 152, 255);
  color: white;
  margin: 2em;
}
</style>
