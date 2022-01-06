<template>
  <div id="logo" >
    <header class="myHed header" >
    </header>
    <img src="images/tpms.ico" alt="logo" class="logo">
    <p class="title">Bienvenue</p>
  </div>
  <div class="mx-4">
    <p class="citation">
      Rencontrez des sportifs, organisez des activités,
      et trouvez votre prochaine passion.
      <br>
      Le monde du sport n'attends que vous!
    </p>
  </div>

  <router-link
      to="/login"
      v-slot="{href, navigate}">
    <button
        type="button"
        :href="href" @click="navigate"
        class="btn btn-outline-primary btn-lg mx-auto">
      Se connecter
    </button>
  </router-link>
  <router-link
      to="/register"
      v-slot="{href, navigate}">
      <button
          type="button"
          class="btn btn-outline-success btn-lg mx-auto"
          :href="href" @click="navigate">
        S'inscrire
      </button>
    </router-link>

  <div class="mx-3">
    En vous inscrivant vous acceptez nos
    <br>
    <a href="">Conditions générales d'utilisation</a>
  </div>
  <footer class="wave">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
      <path fill="#0099ff" fill-opacity="1" d="M0,96L80,117.3C160,139,320,181,480,165.3C640,149,800,75,960,48C1120,21,1280,43,1360,53.3L1440,64L1440,320L1360,320C1280,320,1120,320,960,320C800,320,640,320,480,320C320,320,160,320,80,320L0,320Z"></path>
    </svg>
  </footer>
</template>

<script>
export default {
  name: "Accueil",
  emits: ['updateTitleName']
}
</script>

<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;600&display=swap');

button {
  width: 60vw;
}

button:hover a {
  color:white;
}

.citation {
  font-family: 'Rubik', sans-serif;
  font-style: italic;
  font-size: 1em;
}

.title {
  margin-top: 8vh;
  font-size: 40px;
  font-weight: 900;
  background-image: linear-gradient(to right, #0084ff, #00f2ff);
  color: transparent;
  -webkit-background-clip: text;
  background-clip: text;
}

.logo {
  position:absolute;
  border-radius:50%;
  border:3px solid white;
  left:50%;
  margin-left:-55px;
  margin-top: -8vh;
}

.header {
  position:relative;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  padding-bottom: 10vh;
}

</style>

