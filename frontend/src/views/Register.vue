<template>
    <div class="flex-grow-1 d-flex flex-column">
      <header class="myHed mt-3">
        <p>Inscription</p>
        <img src="/images/tpms.ico" alt="logo">
      </header>

      <form @submit.prevent="register" class="container flex-grow-1 d-flex flex-column justify-content-between">
        <div v-if="suite" class="flex-grow-1 d-flex flex-column justify-content-around">
          <div>
            <label>
              <i class="fas fa-user"></i>
              <input
                class="myInput"
                type="contact"
                name="username"
                id="username"
                placeholder="Pseudo * "
                v-model="this.userInformation.account_in.username"
                required
              />
            </label>
            <p class="text mt-2">Vous ne pourrez pas changer votre pseudo.</p>
          </div>
          <div>
            <label>
              <i class="fas fa-envelope"></i>
              <input
                class="myInput"
                type="email"
                name="email"
                placeholder="Adresse e-mail *"
                id="email"
                v-model="this.userInformation.account_in.email"
              />
            </label>
            <p class="text mt-2">Un e-mail de confirmation vous sera envoyé.</p>
          </div>

          <div>
            <label>
              <i class="fas fa-lock"></i>
              <input
                class="myInput"
                type="password"
                name="password"
                id="password"
                placeholder="Mot de passe *"
                v-model="this.userInformation.account_in.password"
              />
            </label>
          </div>
        </div>
        <!-- Div qui gère la seconde partie de l'inscription -->
        <div v-else class="flex-grow-1 d-flex flex-column justify-content-around">
          <div>
            <label>
              <i class="fas fa-user"></i>
              <input
                class="myInput"
                name="first_name"
                id="first_name"
                placeholder="Prénom"
                v-model="this.userInformation.data_in.first_name"
                required
              />
            </label>
          </div>
          <div>
            <label>
              <i class="fas fa-user"></i>
              <input
                class="myInput"
                name="last_name"
                id="last_name"
                placeholder="Nom"
                v-model="this.userInformation.data_in.last_name"
                required
              />
            </label>
          </div>
          <div>
            <label>
                <i class="fas fa-user"></i>
              <input
                class="myInput"
                type="number"
                name="postcode"
                id="postcode"
                placeholder="code postal"
                v-model="this.userInformation.data_in.postcode"
                required
              />
            </label>
          </div>
          <div >
            <label>
                <i class="fas fa-user"></i>
              <input
                class="myInput"
                type="date"
                name="birthdate"
                id="birthdate"
                pattern="[0-9]{4}-[0-9]{2}-[0-9]{2}"
                placeholder="Date de naissance"
                v-model="this.userInformation.data_in.birthday"
                required
              />
            </label>
          </div>
          <div>
            <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" name="gender" id="man" value="m" v-model="this.userInformation.data_in.gender">
            <label class="form-check-label" for="inlineRadio1">Homme</label>
          </div>
          <div class="form-check form-check-inline ">
            <input class="form-check-input" type="radio" name="gender" id="women" value="f" v-model="this.userInformation.data_in.gender">
            <label class="form-check-label" for="inlineRadio1">Femme</label>
          </div>
          </div>
        </div>
        <!-- Fin de la seconde partie de l'inscription -->

        <!-- bouton pour aller à la 2e partie du formulaire -->
        <div class="m-4">
          <div class="form-group" v-if="suite">
            <label>
              <input
                @click="this.suite = false"
                type="button"
                class="form-control button"
                value="Continuer"
              />
            </label>
          </div>
          <!-- bouton pour s'inscrire -->
          <div class="form-group" v-else>
            <label>
              <input
                type="submit"
                class="form-control button"
                value="S'inscrire !"
              />
            </label>
          </div>
          <!-- bouton retour -->
          <div class="form-group" v-if="!suite">
            <label>
              <input
                @click="this.suite = true"
                type="button"
                class="form-control button"
                value="Retour"
              />
            </label>
          </div>
        </div>
        <router-link class="check_1" to="/login"
          >Déjà un compte ?
      </router-link>
        <SemipolarSpinner class="align-self-center"
                          v-if="loading"
                          :animation-duration="2000"
                          :size="65"
                          color="#ff1d5e"
        />
      </form>
      <div>
        {{ this.message }}
      </div>
    </div>



    <div v-if="inscriptionValide" class="alert alert-success align-self-center" role="alert">
        Vous vous êtes bien inscrit, mais vous devez vérifier votre email avant de pouvoir vous connecter.
      </div>

  <footer class="wave">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
      <path fill="#0099ff" fill-opacity="1" d="M0,96L80,117.3C160,139,320,181,480,165.3C640,149,800,75,960,48C1120,21,1280,43,1360,53.3L1440,64L1440,320L1360,320C1280,320,1120,320,960,320C800,320,640,320,480,320C320,320,160,320,80,320L0,320Z"></path>
    </svg>
  </footer>
</template>

<script>
import AuthService from "../services/auth.service.js";
import { SemipolarSpinner  } from 'epic-spinners'


export default {
  name: "Register",
  components: {
    SemipolarSpinner,
  },
  data() {
    return {
      suite: true,
      loading: false,
      inscriptionValide: false,
      // L'objet qui va contenir toutes les infos de l'utilisateur
      userInformation: {
        account_in: {
          username: "",
          email: "",
          password: "",
        },
        data_in: {
          first_name: "",
          last_name: "",
          postcode: "",
          profile_picture:
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/ISO_C%2B%2B_Logo.svg/800px-ISO_C%2B%2B_Logo.svg.png",
          birthday: "",
          about: "",
          gender: "m",
        },
      },
      authFail: false,
      message: "",
    };
  },
  computed: {
    // Fonction pour savoir si le mec est connécté pour l'app
    isAuthenticated() {
      return this.$store.state.isAuthenticated;
    },
  },
  // à la création de la page (quand la page s'affiche en gros)
  created() {
    // si le mec est connécté il est redirigé vers la page profile
    if (this.isAuthenticated) {
      this.$router.push({ name: "Home" });
    }
  },
  methods: {
    // Fonction pour register l'utilisateur
    register() {
      this.loading = true;
      this.authFail = false;
      // si le register se passe bien, redirige vers la page login
      let data = JSON.parse(JSON.stringify(this.userInformation));
      AuthService.register(data)
        .then(() => {
          this.inscriptionValide = true;
          this.loading = false;
        })
        .catch((error) => {
          // sinon indique qu'il y a eu une erreur
          this.loading = false;
          this.authFail = true;
          this.message = error.message || error;
          this.suite = true;
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

.fas {
    position: relative;
    display: block;
    left: -20vw;
    top: 30px;
    color: rgb(255, 255, 255);
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



.text {
    font-size: 15px;
    color: #746f6f;
}


.grey option {
    background-color: rgb(115, 115, 119);
}

</style>