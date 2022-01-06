<template>
  <!-- barre de recherche -->
  <perfect-scrollbar>
      <div class="p-2 pt-4">
        <h2>Rayon autour de vous : {{ this.sportivesRequestInfo.radius }} km</h2>
        <vue3-slider v-model="this.sportivesRequestInfo.radius"
          :min="min"
          :max="max"
          :step="step"
          :tooltip="tooltip"
        />
      </div>
      <div>
        <button type="button" class="btn btn-primary" @click="getSportives">
          Chercher
        </button>
      </div>
      <div class="d-flex flex-column flex-sm-row flex-wrap justify-content-center">
        <ScalingSquaresSpinner class="align-self-center"
                               v-if="loading"
                               :animation-duration="2500"
                               :rhombus-size="15"
                               color="#ff1d5e"
        />
      </div>

      <div class="d-flex flex-column flex-sm-row flex-wrap justify-content-center pb-5" v-if="sportives">

        <Profil v-for="sportive in sportives" v-bind:key="sportive.account.last_name" :profilInfo="sportive"/>
      </div>
      <div v-if="error">
        {{ this.error }}
      </div>
  </perfect-scrollbar>
</template>

<script>
  import Profil from "../components/Profil.vue";
  import SportivesInformations from "../services/sportives.services.js"
  import slider from "vue3-slider"
  import {ScalingSquaresSpinner} from "epic-spinners";
  export default {
    name: "Sportives",
    components: {
      Profil,
      "vue3-slider": slider,
      ScalingSquaresSpinner,
    },
    data() {
      return {
        sportivesRequestInfo: {
            me_excluded: true,
            radius: 50
        },
        min: 5,
        max: 300,
        step: 1,
        tooltip: true,
        error: null,
        sportives: null,
        message: null,
        loading: false,
      };
    },
    computed: {
      // Fonction pour savoir si l'utilisateur est connécté pour l'app
      isAuthenticated() {
        return this.$store.state.isAuthenticated;
      },
    },
    methods: {
      getSportives() {
        this.loading = true;
        SportivesInformations.getSportivesAround(this.sportivesRequestInfo).then((data) => {
            this.loading = false;
            this.sportives = data;
          })
          .catch((error) => {
            this.loading = false;
            this.error = error;
          });
      },
      logout() {
        this.$store.dispatch("logout");
        this.$router.push("/");
      },
      eventChangeTitle(){
            const data = {title: "Les Sportifs", id: 4};
            this.$emit('updateTitleName', data);
        }
    },
    created() {
      if (!this.isAuthenticated) {
        this.logout();
      }
    },
    beforeMount() {
      //récup les activités de l'user et les mets sous forme de card
      this.getSportives();
    },
    mounted() {
        this.eventChangeTitle();
    }
  };
</script>
<style>
</style>
