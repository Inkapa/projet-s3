<template>
  <form class="flex-grow-1 d-flex flex-column m-3 justify-content-between padding" @submit.prevent="updateActivity">
    <div class="mt-5">
      <label for="titre" class="form-label">
        <h2>Titre</h2>
      </label>
      <input
          type="text"
          class="form-control"
          placeholder="Nom de l'activité"
          id="titre"
          name="titre"
          v-model="updatableData.title"
          required
      />
    </div>
    <label for="description" class="form-label">Description</label>
    <textarea
        class="form-control"
        id="description"
        maxlength="300"
        cols="30"
        rows="6"
        name="description"
        v-model="updatableData.description"
        required
    >
    </textarea>
    <div>
      <div class="form-check form-check-inline">
        <input
            class="form-check-input"
            type="checkbox"
            id="débutant"
            value="débutant"
            v-model="updatableData.levels"
        />
        <label class="form-check-label" for="débutant">débutant</label>
      </div>
      <div class="form-check form-check-inline">
        <input
            class="form-check-input"
            type="checkbox"
            id="amateur"
            value="amateur"
            v-model="updatableData.levels"
        />
        <label class="form-check-label" for="amateur">amateur</label>
      </div>
      <div class="form-check form-check-inline">
        <input
            class="form-check-input"
            type="checkbox"
            id="intermédiaire"
            value="intermédiaire"
            v-model="updatableData.levels"
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
            v-model="updatableData.levels"
        />
        <label class="form-check-label" for="confirmé">confirmé</label>
      </div>
      <div class="form-check form-check-inline">
        <input
            class="form-check-input"
            type="checkbox"
            id="expert"
            value="expert"
            v-model="updatableData.levels"
        />
        <label class="form-check-label" for="expert">expert</label>
      </div>
    </div>
    <button type="submit" class="btn btn-primary">
      Modifier
    </button>
    <div v-if="message" class="alert alert-success" role="alert">
      L'activité a bien été modifiée !
    </div>
    <div v-if="error" class="alert alert-danger" role="alert">
      {{ this.error }}
    </div>
    <p>Il y a {{activity.participant_count}} participants</p>
  </form>
</template>

<script>
import GestionActivities from "../services/activities.service.js";

export default {
  name: "EditPage",
  emits: ['completed'],
  props: {
    activity: {
      type: Object,
      default: () => ({}),
    }
  },
  data() {
    return {
      updatableData: {
        levels: []
      },
      message: null,
      error: null,
      levels: null,
    };
  },
  methods: {
    logout() {
      this.$store.dispatch("logout");
      this.$router.push("/");
    },
    updateActivity() {
      let requestData = {
        activity_id: this.activity.id,
        data_in: {
          title: this.updatableData.title,
          description: this.updatableData.description,
          levels: this.updatableData.levels,
        }
      };

      GestionActivities.updateActivity(requestData).then((message) => {
        this.loading = false;
        this.message = message;
        this.$emit('completed')
      }).catch((error) => {
        this.loading = false;
        this.error = error;
      })
    },
  },
  computed: {
    // Fonction pour savoir si l'utilisateur est connécté pour l'app
    isAuthenticated() {
      return this.$store.state.isAuthenticated;
    },
  },
  mounted() {
    if (!this.isAuthenticated) {
      this.logout();
    }
  },
  created() {
    this.updatableData = {...this.activity, ...this.updatableData}
    console.log(this.updatableData)
  }
}
</script>

<style scoped>
.padding {
  padding-bottom: 80px;
}
</style>