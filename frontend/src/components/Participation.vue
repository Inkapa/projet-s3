<template>
  <div v-if="this.message" class="alert alert-success mt-3" role="alert">
    {{ this.message }}
  </div>
  <div v-if="this.error" class="alert alert-danger mt-3" role="alert">
    {{ this.error }}
  </div>
  <div class="card text-center m-3 flex-grow-1 activity">
    <div class="card-header">{{ this.participationInfo.activity.title }}</div>
    <div class="card-body">
      <h5 class="card-title">{{ this.participationInfo.activity.sport.name }}</h5>
      <p class="card-text">
        {{ this.participationInfo.activity.description }}
      </p>
      <p class="card-text">
        <strong>Se déroule le :</strong> {{ this.participationInfo.activity.event_date }}
      </p>
      <p class="card-text">
        <strong>Niveau : </strong>
        <span class="badge rounded-pill bg-success mx-1">{{  this.participationInfo.level.level }}</span>
      </p>
      <!--Div pour pouvoir annuler la participation-->
      <div v-if="this.participationInfo.activity.active">
        <button @click="removeMyParticipation" class="btn btn-danger"> Annuler </button>
      </div>
      <p v-if="!loading" class="pt-2">Il y a déjà {{ this.participationInfo.activity.participant_count }} participants !</p>
    </div>
    <div class="card-footer text-light">{{ this.participationInfo.activity.postcode }} - {{ this.participationInfo.activity.address }}</div>
  </div>
</template>

<script>
import GestionParticipations from "../services/participations.service.js";
export default {
  name: "Participation",
  props: {
    participationInfo: Object
  },
  emits: ['remove'],
  data() {
    return {
      id: this.participationInfo.activity.id,
      loading: false,
      error: null,
      message: null,
    }
  },
  computed: {
  },
  methods: {
    // viewParticipation() {
    //   this.$router.push({ name: 'ParticipationPage', params: { id: this.id }});
    // },
    removeMyParticipation() {
      GestionParticipations.removeMyParticipation(this.id).then(() => {
        this.message = "Vous êtes bien désinscrit de cette activité !";
        this.$emit('remove', this.id);
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
  background-color: rgba(48, 80, 148, 0.97);
  color: white;
  margin: 2em;
}
</style>
