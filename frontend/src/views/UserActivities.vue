<template>
  <perfect-scrollbar>
      <div class="d-flex justify-content-center align-items-center mt-4">
          <h4>Filters :</h4>
          <div class="form-check form-switch mx-2">
              <input class="form-check-input" type="checkbox" v-on:change="getActivities()"
                  role="switch" id="flexSwitchCheckChecked" v-model="this.activitiesRequestInfo.active">
              <label class="form-check-label" for="flexSwitchCheckChecked">Activités actives</label>
          </div>
      </div>
      <SwappingSquaresSpinner class="align-self-center"
          v-if="loading"
          :animation-duration="1000"
          :size="65"
          color="#ff1d5e"
      />
      <div class="d-flex flex-column flex-sm-row flex-wrap  mb-5" v-if="activities">
          <Activity v-for="activity in activities" v-bind:key="activity.id" :activity-info="activity" :owner="true"/>
      </div>
      <div v-if="this.message" class="alert alert-danger" role="alert">
          {{this.message}}
      </div>
  </perfect-scrollbar>
</template>
<script>
import Activity from "../components/Activity.vue"
import GestionActivities from '../services/activities.service.js'
import { SwappingSquaresSpinner  } from 'epic-spinners'
export default {
    name: "UserActivities",
    components: {
        Activity,
        SwappingSquaresSpinner
    },
    data() {
        return {
            activitiesRequestInfo : {
                active: true,
                offset: 0,
                limit: 10,
            },
            activities: null,
            message: null,
            loading: false
        }
    },
    methods: {
        getActivities() {
            this.loading = true;
            GestionActivities.getActiveUserActivities(this.activitiesRequestInfo).then((data) => {
                this.loading = false;
                this.activities = data;
            }).catch((error) => {
                this.loading = false;
                this.message = error;
            })
        },
        logout() {
            this.$store.dispatch('logout');
            this.$router.push('/');
        },
        eventChangeTitle(){
            const data = {title: "Vos Activités"};
            this.$emit('updateTitleName', data);
        }
    },
    beforeCreate() {
        if (!this.isAuthenticated) {
            this.logout;
        }
    },
    beforeMount() {
        //récup les activités de l'user et les mets sous forme de card
        this.getActivities()
    },
    mounted() {
        this.eventChangeTitle();
    }
}
</script>