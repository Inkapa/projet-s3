<template>
  <div class="flex-grow-1 d-flex flex-column">
    <header class="myHed mt-3">
      <p>Connexion</p>
      <img src="/images/tpms.ico" alt="logo">
    </header>
    <!-- formulaire de connexion -->
    <form
      class="container flex-grow-1 d-flex flex-column justify-content-around mt-5"
      name="loginForm"
      @submit.prevent="login"
    >
      <div>
        <label>
          <i class="fas fa-user"></i>
          <input
            v-model="this.user.username"
            class="myInput"
            type="text"
            name="login"
            id="login"
            placeholder="Identifiant"
            required
          />
        </label>
        <p class="text mt-2">Email ou pseudonyme.</p>
      </div>
      <div>
        <label>
          <i class="fas fa-lock"></i>
          <input
              type="password"
              class="myInput"
              placeholder="Mot de Passe"
              v-model="this.user.password"
              required
          />
        </label>
      </div>
      <div>
        <label>
          <button class="form-control button" type="submit">
            Se connecter
          </button>
        </label>
      </div>
      <span class="check_1">Mot de passe oublié ?</span>
    </form>
    <div v-if="authFail" class="alert alert-danger align-items-center" role="alert">
      <strong>{{ this.message }}</strong>
    </div>
    <div v-if="loading" class="align-self-center">
      <SemipolarSpinner
      :animation-duration="2000"
      :size="65"
      color="#ff1d5e"
    />
    </div>
  </div>
  <footer class="wave">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
      <path fill="#0099ff" fill-opacity="1" d="M0,96L80,117.3C160,139,320,181,480,165.3C640,149,800,75,960,48C1120,21,1280,43,1360,53.3L1440,64L1440,320L1360,320C1280,320,1120,320,960,320C800,320,640,320,480,320C320,320,160,320,80,320L0,320Z"></path>
    </svg>
  </footer>
</template>

<script>
import { SemipolarSpinner  } from 'epic-spinners'
export default {
  name: "Login",
  components: {
    SemipolarSpinner
  },
  data() {
    return {
      loading: false,
      user: {
        username: "",
        password: "",
      },
      authFail: false,
      message: "",
    };
  },
  computed: {
    isAuthenticated() {
      return this.$store.state.isAuthenticated;
    },
  },
  created() {
    if (this.isAuthenticated) {
      this.$router.push({ name: "Home" });
    }
  },
  methods: {
    login() {
      this.loading = true;
      this.authFail = false;
      const userData = {
        username: this.user.username,
        password: this.user.password,
      };
      this.$store
        .dispatch("login", userData)
        .then(() => {
          this.$router.push({ name: "Home" });
        })
        .catch((error) => {
          this.loading = false;
          this.authFail = true;
          this.message = error.message || error;
          setTimeout(() => this.authFail = false, 3000)
        });
    },
  },
};
</script>

<style scoped>

input {
  display: block;
  text-align: center;
  left: 50%;
}

.text {
  font-size: 15px;
  color: #746f6f;
}

.button {
  margin-top: 10px;
  width: 250px;
  border-radius: 25px;
  background-image: linear-gradient(to right, #0084ff, #00f2ff);
  color: #fff;
  font-weight: 700;
  cursor: pointer;
}


</style>