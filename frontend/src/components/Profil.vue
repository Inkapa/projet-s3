<template>
  <div class="d-flex justify-content-center align-items-center m-3">
    <div class="card panic">
      <div class="user text-center">
        <div class="profile">
          <img :src="this.profilInfo.account.profile_picture" class="rounded-circle pt-4" width="80">
        </div>
      </div>
      <div class="mt-3 text-center">
        <h4 class="mb-0">{{this.profilInfo.account.last_name}} {{this.profilInfo.account.first_name}}</h4>
        <span class="text-muted d-block mb-2">{{this.profilInfo.account.postcode}}</span>
        <button class="btn btn-primary btn-sm follow" @click="pushToUserpage">En savoir plus</button>
        <div class="d-flex flex-column justify-content-between align-items-center mt-4 px-4">
          <h6 style="text-decoration: underline;">Sports Pratiqués</h6>
          <p v-for="sport in this.profilInfo.sports" :key="sport.sport.id" class="card-text mb-1">
            <b>{{sport.sport.name}}</b> | {{ sport.level.level }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    name: "Profil",
    props: {
        profilInfo: Object
    },
    methods: {
        pushToUserpage() {
            this.$router.push({ name: 'User', params: { username: this.profilInfo.account.owner_username }});
        }
    }
}
// function getAge(date) { 
//         var diff = Date.now() - date.getTime();
//         var age = new Date(diff); 
//         return Math.abs(age.getUTCFullYear() - 1970);
//     }
    //alert(getAge(new Date(1995, 12, 6))); //Date(année, mois, jour)  


</script>
<style>
.panic {
  width: 60vw;
}
</style>