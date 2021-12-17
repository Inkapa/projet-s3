<template>

  <div class="h-100 d-flex flex-column justify-content-between">
    <div v-if="isAuthenticated" id="nav-top"
        class="sticky-top d-flex text-center justify-content-around align-items-center text-white p-1 color">
      <router-link to="/profile" class="text-white fw-bold p-2">Profil</router-link>
      <span class="size-title">{{ this.actualPage }}</span>
      <router-link to="/home" class="text-white fw-bold p-2">Home</router-link>
    </div>
  <!--    <nav v-else class="fixed-top border border-black d-flex align-items-center justify-content-center">-->
  <!--      <router-link to="/">Accueil</router-link>-->
  <!--    </nav>-->

    <div id="application" class="h-100 d-flex flex-column justify-content-between">
      <router-view
        @update-title-name="updateTitleName"
      />
    </div>
    <!-- Affiche la NavBar que quand la personne est loggedin -->
    <nav id="nav-bottom" v-if="isAuthenticated" class="navbar fixed-bottom navbar-light bg-light">
      <VueBottomNavigation foregroundColor="#FFFFFF" :badgeColor="color" :value="selected" :options="options" v-model="selected" />
    </nav>
  </div>

</template>

<script>
import VueBottomNavigation from "bottom-navigation-vue";
export default {
  name: "App",
  components: {
    VueBottomNavigation,
  },
  data: () => ({
      color: "#000000",
      actualPage: "Home",
      selected: 1,
      options: [
        {
          id: 1,
          icon: "fa fa-home",
          title: "Home",
          path: {name: "Home"}
        },
        {
          id: 2,
          icon: "fa fa-coffee",
          title: "Activités",
          childs: [
            {
              id: 201,
              icon: "fa fa-calendar-check",
              title: "Vos Activités",
              path: {name: "UserActivities"}
            },
            {
              id: 202,
              icon: "fa fa-calendar",
              title: "Créer votre activité",
              path: {name: "CreateActivity"}
            }
          ]
        },
        { id: 3, icon: "fa fa-user", title: "Les gens", path: {name: "Sportives"}},
        // { id: 4, icon: "fa fa-bell", title: "Messages" },
      ],
  }),
  computed: {
    isAuthenticated() {
      return this.$store.state.isAuthenticated;
    }
  },
  methods: {
    updateTitleName(data) {
      this.actualPage = data.title;
    }
  }
};
</script>

<style>

a {
  text-decoration: none !important;
}

#application {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #fff;
  overflow-y:hidden;
}

.color {
  background: linear-gradient(to right, #0084ff, #00f2ff);
}
.size-title {
  font-size: calc(25px + 2vw);
  font-weight: 700;
}

#nav-top{
  border-bottom: rgba(0, 0, 0, 0.5);
  box-shadow: -3px 9px 20px rgba(0, 0, 0, 0.3), 0 3px 6px rgba(0, 0, 0, 0.0);
}
#nav-bottom{
  border-top: rgba(0, 0, 0, 0.5);
  box-shadow: -3px 9px 20px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
}

nav{
  height: 50px;
  box-sizing: border-box;
}

.wave {
  position: relative;
  background: #ffffff;
  color: #FFF;
  text-align: center;
  overflow: hidden;
}

@keyframes animateWave {
  0% {
    transform: scale(1,0);
  }
  100% {
    transform: scale(1,1);
  }
}

.wave > svg {
  display: block;
  transform-origin: bottom;
  animation: animateWave 1000ms cubic-bezier(0.23, 1, 0.32, 1) forwards;
}

.myHed {

  font-size: 40px;
  margin-bottom: 10px;
  font-weight: 900;
  background-image: linear-gradient(to right, #0084ff, #00f2ff);
  color: transparent;
  -webkit-background-clip: text;
  background-clip: text;
}

.fas {
  position: relative;
  display: block;
  left: -20vw;
  top: 30px;
  color: rgb(255, 255, 255);
}

.myInput {
  padding: 10px 10px 10px 40px;
  border-radius: 25px;
  background-image: linear-gradient(to right, #0084ff, #00f2ff);
  color: #fff;
  border: none;
  display: block;
  width: 60vw;
}
.check_1 {
  font-weight: bold;
  color: rgb(36, 79, 134);
  font-size: 18px;
  margin: 15px auto;
  cursor: pointer;
}


</style>