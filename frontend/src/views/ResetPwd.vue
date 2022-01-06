<template>
    <div class="flex-grow-1 d-flex flex-column">
        <header class="myHed mt-3">
            <p>Réinitialiser votre mot de passe</p>
            <img src="/images/tpms.ico" alt="logo">
        </header>
        <!-- formulaire de connexion -->
        <form
            class="container flex-grow-1 d-flex flex-column justify-content-around mt-5"
            name="loginForm"
            @submit.prevent="resetPassword"
        >
            <div>
                <label>
                <input
                    v-model="this.email"
                    class="myInput"
                    type="email"
                    name="email"
                    id="email"
                    placeholder="Email"
                    required
                />
                </label>
                <p class="text mt-2">Entrer votre email ici</p>
            </div>
            <div>
                <button class="form-control button" type="submit">
                    Envoyer
                </button>
            </div>
        </form>
        <div v-if="message" class="alert alert-info align-items-center" role="alert">
            <strong>{{ this.message }}</strong>
        </div>
        <div v-if="fail" class="alert alert-danger align-items-center" role="alert">
            <strong>{{ this.fail }}</strong>
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
import AuthService from "../services/auth.service.js";
import { SemipolarSpinner  } from 'epic-spinners'
export default {
    name: "ResetPwd",
    components: {
        SemipolarSpinner
    },
    data() {
        return {
            email: "",
            loading: false,
            fail: "",
            message: ""
        }
    },
    methods: {
        resetPassword() {
            this.loading = true;
            AuthService.resetpwd(this.email).then((data) => {
                this.loading = false;
                this.message = data
                setTimeout(() =>{
                    this.$router.push({ name: "Login" });
                    this.message = ""
                    }, 3000);
            }).catch((error) => {
                this.loading = false;
                this.fail = error;
                setTimeout(() =>{
                    this.fail = ""
                    }, 3000);
            })
        }
    }
}
</script>

<style>

</style>