<template>
  <div v-if="loading" class="flex-grow-1 d-flex flex-column justify-content-center">
    <SwappingSquaresSpinner
        :animation-duration="1000"
        :size="150"
        color="#ff1d5e"
        class="align-self-center"
    />
  </div>
  <div v-if="!loading" class="d-flex flex-column justify-content-center align-content-center m-4">
    <h1>{{ activity.title }}</h1>
    <div class="hr-sect mb-2">{{ activity.sport.name }}</div>
    <div class="d-flex justify-content-center">
      <span class="badge rounded-pill bg-success mx-2" v-for="level in activity.levels" v-bind:key="level.id">{{ level.level }}</span>
    </div>
    <div class="mt-3">
      <textarea type="text" name="description" v-text="activity.description"
                minlength="0" maxlength="300" class="form-control" disabled/>
    </div>
    <div class="mt-3">
      <label for="date" class="form-label">Date</label>
      <input type="text" name="date" id="date"
             :placeholder="activity.event_date" size="10" class="form-control text-center" disabled/>
    </div>
    <div class="mt-3">
      <label for="address" class="form-label">Adresse</label>
      <input type="text" name="address" id="address"
             :placeholder="address" size="10" class="form-control text-center" disabled/>
    </div>

  </div>
  <MapPath v-if="!loading" :address="address">
  </MapPath>
  <perfect-scrollbar v-if="!loading" class="d-flex flex-column">
    <h3 class="m-4">Participants ({{ activity.participant_count }})</h3>

    <ul class="list-group mx-3">
      <router-link class="list-group-item d-flex justify-content-between align-items-center"
          v-for="user in activity.participants"
          :key="user"
          :to="{name: 'User', params: {username: user.user.username}}">
        {{ user.user.data.first_name }} {{ user.user.data.last_name }}
        <span class="badge rounded-pill bg-success mx-2">{{ user.level.level }}</span>
        <img :src="user.user.data.profile_picture" class="pp img-fluid" alt="profile picture">
      </router-link>
    </ul>
  </perfect-scrollbar>
</template>

<script>
import MapPath from "../components/MapPath.vue"
import GestionActivities from "../services/activities.service.js";
import { SwappingSquaresSpinner } from 'epic-spinners'

import {computed, onMounted, ref} from "vue";
export default {
  name: "ActivityDetails",
  emits: ['updateTitleName'],
  components: {
    MapPath,
    SwappingSquaresSpinner
  },
  props: {
    id: String
  },
  setup(props){
    const activity = ref({})
    const loading = ref(true)
    const error = ref('')
    const address = computed(() => activity.value.address + ', ' + activity.value.postcode + ', France')

    onMounted(() => {
      GestionActivities.getActivityWithId(props.id)
          .then((data) => {
            loading.value = false;
            activity.value = data;
          })
          .catch((error) => {
            loading.value = false;
            error.value = error;
          });
    })

    return {activity, loading, error, address}


  }
}
</script>

<style scoped>
.ps {
  padding-bottom: 80px;
  max-height: 250px;
}
.pp {
  height: 4vh;
  width: auto;
  border-radius: 50%;
}

h1, h3 {
  font-weight: bold;
}

.hr-sect {
  display: flex;
  flex-basis: 100%;
  align-items: center;
  color: rgba(0, 0, 0, 0.4);
  font-size: 1.5em;
  text-transform: uppercase;
}
.hr-sect::before,
.hr-sect::after {
  content: "";
  flex-grow: 1;
  background: rgba(0, 0, 0, 0.4);
  height: 2px;
  font-size: 0px;
  line-height: 0px;
  margin: 0px 16px;
}
</style>