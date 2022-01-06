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
      @submit.prevent="changepwd"
    >
      <div>
        <label>
          <i class="fas fa-lock"></i>
          <input
              type="password"
              class="myInput"
              placeholder="Mot de Passe"
              v-model="this.password"
              required
          />
        </label>
        <label>
          <i class="fas fa-lock"></i>
          <input
              type="password"
              class="myInput"
              placeholder="Vérifier votre mot de passe"
              v-model="this.verifpassword"
              required
          />
        </label>
      </div>
      <div>
        <label>
          <button class="form-control button" type="submit">
            Changer son mot de passe
          </button>
        </label>
      </div>
    </form>
    <div v-if="fail" class="alert alert-danger align-items-center" role="alert">
      <strong>{{ this.fail }}</strong>
    </div>
    <div v-if="message" class="alert alert-danger align-items-center" role="alert">
      <strong>{{ this.message }}</strong>
    </div>
    <div v-if="loading" class="align-self-center">
      <SemipolarSpinner
      :animation-duration="2000"
      :size="65"
      color="#ff1d5e"
    />
    </div>
    <footer class="wave">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
        <path fill="#0099ff" fill-opacity="1" d="M0,96L80,117.3C160,139,320,181,480,165.3C640,149,800,75,960,48C1120,21,1280,43,1360,53.3L1440,64L1440,320L1360,320C1280,320,1120,320,960,320C800,320,640,320,480,320C320,320,160,320,80,320L0,320Z"></path>
      </svg>
    </footer>
  </div>
</template>

<script>
import { SemipolarSpinner  } from 'epic-spinners'
import AuthService from "../services/auth.service.js";
export default {
    name: "ChangePwd",
    components: {
        SemipolarSpinner
    },
    data() {
        return {
            loading: false,
            password: "",
            verifpassword: "",
            token: this.$route.query.token,
            fail: "",
            message: "",
        }
    },
    methods:{
        changepwd() {
          if (this.password !== this.verifpassword){
            this.loading = false;
            this.fail = "Les mots de passes ne sont pas identiques";
            setTimeout(() => this.fail = "", 3000);
            return
          }
          this.loading = true;
          const newData = {token: this.token, new_password: this.password}
          AuthService.newpwd(newData).then((data) =>{
            this.loading = false;
            this.message = data;
            setTimeout(() => this.$router.push({name: "Login"}), 3000);
          }).catch((error) => {
            this.loading = false;
            this.fail = error;
          })
        }
    }
}
</script>

<style>
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