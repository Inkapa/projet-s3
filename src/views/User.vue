<template>
    <div class="d-flex flex-column justify-content-between padding">
      <div class="haut mb-3 d-flex flex-column">
        <p class="profil text-center">{{ this.username }}</p>
        <div class="avatar mb-3">
          <img class="profile-picture" :src="this.infos.profile_picture" alt="profile picture">
        </div>
      </div>
      <form class="d-flex flex-column align-self-center flex-grow-1" @submit.prevent="">

        <div class="mb-3">
          <label for="about" class="form-label">Description</label>
          <input type="text" name="about" id="about" v-model="this.infos.about"
                 minlength="0" maxlength="300" class="form-control" disabled/>
        </div>
        <div class="mb-3">
          <label for="last_name" class="form-label">Last Name</label>
          <input type="text" name="last_name" id="last_name"
                 v-model="this.infos.last_name" minlength="4" maxlength="50" size="10" class="form-control" disabled/>
        </div>

        <div class="mb-3">
          <label for="first_name" class="form-label">First Name</label>
          <input type="text" name="first_name" id="first_name"
                 v-model="this.infos.first_name" minlength="4" maxlength="50" size="10" class="form-control" disabled/>
        </div>

        <div class="mb-3">
          <label for="postcode" class="form-label">Postcode</label>
          <input type="text" name="postcode" id="postcode" v-model="this.infos.postcode"
                 minlength="3" maxlength="5" size="10" class="form-control" disabled/>
        </div>

        <div class="age mb-3">{{ this.infos.birthday }}</div>
      </form>
      <LoopingRhombusesSpinner class="align-self-center"
                               v-if="loading"
                               :animation-duration="2500"
                               :rhombus-size="15"
                               color="#ff1d5e"
      />
    </div>
</template>

<script>
import SportivesInformations from "../services/sportives.services.js"
import { LoopingRhombusesSpinner } from 'epic-spinners'
export default {
  name: "User",
  components: {
    LoopingRhombusesSpinner
  },
  data () {
    return {
      username: this.$route.params.username,
      infos: null,
      loading: false,
      error: null,
    }
  },
  methods: {
    getInformations(){
      this.loading = true;
      SportivesInformations.getSportivesWithUsername(this.$route.params.username).then((data) => {
        this.loading = false;
        this.infos = data;
      }).catch((error) => {
        this.loading = false;
        this.error = error;
      })
    },
    eventChangeTitle(){
      const data = {title: "Utilisateur"};
      this.$emit('updateTitleName', data);
    }
  },
  beforeMount(){
    this.getInformations();
  },
  mounted() {
    this.eventChangeTitle();
  }
}
</script>

<style scoped>
.padding {
  padding-bottom: 100px;
}

.haut {
  display: grid;
  grid-template-columns: 25% 50% 25%;
  grid-template-rows: 1fr 1fr 1fr;
  background: linear-gradient(to right, #0084ff, #00f2ff);
}

.gris_haut {
  grid-column-start: 1;
  grid-column-end: 4;
  grid-row-start: 3;
  grid-row-end: 4;
  border-style: none;
  background-color: #fff;
}

.age {
  font-style: italic;
}

.profil {

  color: #FDFAFA;
  font-size: calc(32px + 2vw);
  font-weight: 700;
}

.avatar {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: transparent;
  grid-row-start: 2;
  grid-row-end: 4;
  grid-column-start: 2;
  grid-column-end: 3;
}

.profile-picture {
  width: 90%;
  height: auto;
  max-width: 150px;
  border-radius: 50%;
}
</style>