<template>
  <perfect-scrollbar>
    <form class="m-3 padding" @submit.prevent="createActivity">
      <div class="mb-3">
        <label for="titre" class="form-label">Titre</label>
        <input
          type="text"
          class="form-control"
          placeholder="Nom de l'activité"
          id="titre"
          name="titre"
          v-model="this.activitiesRequestInfo.title"
          required
        />
      </div>
      <div class="mb-3">
        <label class="form-label">Sport</label>
        <select
          class="form-select"
          aria-label="Select pour le sport"
          v-model="this.activitiesRequestInfo.sport_id"
        >
          <option
            v-for="sport in this.sports"
            v-bind:key="sport.id"
            :value="sport.id"
          >
            {{ sport.name }}
          </option>
        </select>
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
          v-model="this.activitiesRequestInfo.description"
          required
        >
        "Decrivez votre activité (300 caractères maximum)"
        </textarea>
      </div>

      <div class="mb-3">
        <label for="cdPost" class="form-label">Code Postal</label>
        <input
          type="text"
          class="form-control"
          maxlength="5"
          pattern="[0-9]{5}"
          placeholder="ex : 75012"
          id="cdPost"
          name="cdPost"
          v-model="this.activitiesRequestInfo.postcode"
          required
        />
      </div>

      <div class="mb-3">
        <label for="adresse" class="form-label">Adresse</label>
        <input
          type="text"
          class="form-control"
          maxlength="45"
          placeholder="ex : 267 Rue de Neufchâtel"
          id="adresse"
          name="adresse"
          v-model="this.activitiesRequestInfo.address"
          required
        />
      </div>

      <div class="mb-3">
        <label for="dateDeb" class="form-label">Date</label>
        <input
          type="date"
          class="form-control"
          id="dateDeb"
          name="dateDeb"
          pattern="[0-9]{4}-[0-9]{2}-[0-9]{2}"
          placeholder="Date de l'acitvité"
          v-model="this.activitiesRequestInfo.event_date"
          required
        />
      </div>

      <div class="mb-3">
        <div class="form-check form-check-inline">
          <input
            class="form-check-input"
            type="checkbox"
            id="débutant"
            value="débutant"
            v-model="this.activitiesRequestInfo.levels"
          />
          <label class="form-check-label" for="débutant">débutant</label>
        </div>
        <div class="form-check form-check-inline">
          <input
            class="form-check-input"
            type="checkbox"
            id="amateur"
            value="amateur"
            v-model="this.activitiesRequestInfo.levels"
          />
          <label class="form-check-label" for="amateur">amateur</label>
        </div>
        <div class="form-check form-check-inline">
          <input
            class="form-check-input"
            type="checkbox"
            id="intermédiaire"
            value="intermédiaire"
            v-model="this.activitiesRequestInfo.levels"
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
            v-model="this.activitiesRequestInfo.levels"
          />
          <label class="form-check-label" for="confirmé">confirmé</label>
        </div>
        <div class="form-check form-check-inline">
          <input
            class="form-check-input"
            type="checkbox"
            id="expert"
            value="expert"
            v-model="this.activitiesRequestInfo.levels"
          />
          <label class="form-check-label" for="expert">expert</label>
        </div>
      </div>

      <!-- <div class="mb-3">
        <label for="imageFile" class="form-label">Illustration</label>
        <input class="form-control" type="file" id="imageFile" />
      </div> -->

      <div class="d-flex justify-content-center mt-1">
        <button type="submit" class="btn btn-primary" :disabled="loading">
          Créer cette activité
        </button>
      </div>
      <SwappingSquaresSpinner class="mt-3"
        v-if="loading"
        :animation-duration="1000"
        :size="65"
        color="#ff1d5e"
      />
      <div v-if="this.message" class="alert alert-success mt-3" role="alert">
        L'activité a bien été créée !
      </div>
      <div v-if="this.error" class="alert alert-danger mt-3" role="alert">
        {{ this.error }}
      </div>
    </form>
    

  </perfect-scrollbar>
</template>

<script>
import GestionActivities from "../services/activities.service.js";
import { SwappingSquaresSpinner  } from 'epic-spinners'
export default {
  name: "CreateActivity",
  components: {
    SwappingSquaresSpinner
  },
  data() {
    return {
      activitiesRequestInfo: {
        title: "",
        description: "",
        event_date: "2021-12-12",
        postcode: "",
        address: "",
        image: "",
        sport_id: 0,
        levels: [],
      },
      message: null,
      error: null,
      loading: false,
      sports: null,
      levels: ["débutant", "amateur", "intermédiaire", "confirmé", "expert"],
    };
  },
  methods: {
    createActivity() {
      this.loading = true;
      GestionActivities.createActivity(this.activitiesRequestInfo)
        .then((message) => {
          this.loading = false;
          this.message = message;
          // pour remettre à 0 une fois l'activité créer
          this.activitiesRequestInfo = {
            title: "",
            description: "",
            event_date: "2021-12-12",
            postcode: "",
            address: "",
            image: "",
            sport_id: 0,
            levels: [],
          };
        }).catch((error) => {
          this.loading = false;
          this.error = error;
        });
    },
    logout() {
      this.$store.dispatch("logout");
      this.$router.push("/");
    },
    eventChangeTitle(){
      const data = {title: "Creér votre Activité"};
      this.$emit('updateTitleName', data);
    }
  },
  beforeCreate() {
    if (!this.isAuthenticated) {
      this.logout;
    }
  },
  beforeMount() {
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
div i {
  font-size: 30px;
}

.padding {
  padding-bottom: 80px;
}
</style>