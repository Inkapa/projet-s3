<template>
  <perfect-scrollbar class="flex-grow-1 d-flex flex-column">

  </perfect-scrollbar>
</template>

<script>
import GestionActivities from "../services/activities.service.js";
export default {
  name: "ActivityPage",
  props: {
    id: String,
    activity: Object
  },
  data() {
    return {
      updatableData: {
        title: "",
        description: "",
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
        activity_id: this.id,
        data_in: {
          title: this.updatableData.title,
          description: this.updatableData.description,
          levels: this.updatableData.levels,
        }
      };
      GestionActivities.updateActivity(requestData).then((message) => {
        this.loading = false;
        this.message = message;
        this.$router.push("/userActivities");
      }).catch((error) => {
        this.loading = false;
        this.error = error;
      })
    },
    eventChangeTitle(){
      const data = {title: "Activité", id: 2};
      this.$emit('updateTitleName', data);
    }
  },
  beforeCreate() {
    if (!this.isAuthenticated) {
      this.logout;
    }
  },
  created() {
    this.updatableData = {...this.activity, ...this.updatableData}
    this.eventChangeTitle();
  },
  mounted() {
  }
}
</script>