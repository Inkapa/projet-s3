<template>
  <perfect-scrollbar>
    <div class="d-flex justify-content-center align-items-center mt-4">
      <h4>Filters :</h4>
      <div class="form-check form-switch mx-2">
        <input class="form-check-input" type="checkbox" v-on:change="getParticipations()"
               role="switch" id="flexSwitchCheckChecked" v-model="this.participationRequestInfo.active">
        <label class="form-check-label" for="flexSwitchCheckChecked">Participation actives</label>
      </div>
    </div>
    <div class="d-flex flex-column justify-content-center align-items-center mt-4">
      <SwappingSquaresSpinner
          v-if="loading"
          :animation-duration="1000"
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
    <div class="d-flex flex-column flex-sm-row flex-wrap  mb-5" v-if="participations">
      <Participation
          v-for="participation in participations"
          v-bind:key="participation.activity.id"
          :participation-info="participation"
          @remove="removeParticipation"
      />
    </div>
  </perfect-scrollbar>
</template>
<script>
import Participation from "../components/Participation.vue"
import GestionParticipation from '../services/participations.service.js'
import { SwappingSquaresSpinner  } from 'epic-spinners'
export default {
  name: "UserParticipation",
  components: {
    Participation,
    SwappingSquaresSpinner
  },
  data() {
    return {
      participationRequestInfo : {
        active: true,
        offset: 0,
        limit: 10,
      },
      participations: null,
      message: null,
      error: null,
      loading: false
    }
  },
  methods: {
    getParticipations() {
      this.loading = true;
      GestionParticipation.getActiveUserParticipations(this.participationRequestInfo).then((data) => {
        this.loading = false;
        this.participations = data;
      }).catch((error) => {
        this.loading = false;
        this.error = error;
      })
    },
    logout() {
      this.$store.dispatch('logout');
      this.$router.push('/');
    },
    eventChangeTitle(){
      const data = {title: "Participations", id: 2};
      this.$emit('updateTitleName', data);
    },
    removeParticipation(id, message){
      this.message = message
      this.participations = this.participations.filter(participation => participation.activity.id !== id)
      this.$refs.alert.classList.add('fade-out')
      this.$refs.alert.onanimationend = () => {
        this.message = null
        this.$refs.alert.classList.remove('fade-out')
      }
    }
  },
  computed: {
    // Fonction pour savoir si l'utilisateur est connécté pour l'app
    isAuthenticated() {
      return this.$store.state.isAuthenticated;
    },
  },
  created() {
    if (!this.isAuthenticated) {
      this.logout();
    }
  },
  beforeMount() {
    //récup les activités de l'user et les mets sous forme de card
    this.getParticipations()
  },
  mounted() {
    this.eventChangeTitle();
  }
}
</script>