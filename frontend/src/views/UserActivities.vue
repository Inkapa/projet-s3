<template>
  <perfect-scrollbar class="flex-grow-1 d-flex flex-column">
      <div v-if="!edit">
        <div class="d-flex justify-content-center align-items-center mt-4">
          <h4>Filters :</h4>
          <div class="form-check form-switch mx-2">
            <input class="form-check-input" type="checkbox" v-on:change="getActivities()"
                   role="switch" id="flexSwitchCheckChecked" v-model="this.activitiesRequestInfo.active">
            <label class="form-check-label" for="flexSwitchCheckChecked">Activités actives</label>
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
        <div class="d-flex flex-column flex-sm-row flex-wrap  mb-5" v-if="activities">
          <Activity
              v-for="activity in activities"
              v-bind:key="activity.id"
              :activity-info="activity"
              :owner="true"
              @remove="removeActivity"
              @edit="toggleEdit"
          />
        </div>
      </div>
      <EditPage
          v-else
          @completed="toggleEdit"
          :activity="editActivity">
      </EditPage>
  </perfect-scrollbar>
</template>
<script>
import Activity from "../components/Activity.vue"
import GestionActivities from '../services/activities.service.js'
import { SwappingSquaresSpinner  } from 'epic-spinners'
import EditPage from "../components/EditPage";
export default {
    name: "UserActivities",
    components: {
        Activity,
        SwappingSquaresSpinner,
        EditPage
    },
    emits: ['updateTitleName'],
    data() {
        return {
            activitiesRequestInfo : {
                active: true,
                offset: 0,
                limit: 10,
            },
            edit: false,
            activities: null,
            message: null,
            error: null,
            loading: false,
            editActivity: {},
        }
    },
    methods: {
        toggleEdit(id){
          if (this.edit){
            this.edit = false
            this.loading = true;
            GestionActivities.getActiveUserActivities(this.activitiesRequestInfo).then((data) => {
              this.loading = false;
              this.activities = data;
            }).catch((error) => {
              this.loading = false;
              this.error = error;
            })

          } else {
            this.editActivity = this.activities.filter(activity => activity.id === id)[0]
            this.edit = true
          }

        },
        getActivities() {
            this.loading = true;
            GestionActivities.getActiveUserActivities(this.activitiesRequestInfo).then((data) => {
                this.loading = false;
                this.activities = data;
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
            const data = {title: "Vos Activités", id: 2};
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
    computed: {
      // Fonction pour savoir si l'utilisateur est connécté pour l'app
      isAuthenticated() {
        return this.$store.state.isAuthenticated;
      },
    },
    beforeMount() {
        if (!this.isAuthenticated) {
          this.logout();
        }
        //récup les activités de l'user et les mets sous forme de card
        this.getActivities()
    },
    mounted() {
        this.eventChangeTitle();
    }
}
</script>