<template>
  <perfect-scrollbar>
    <div class="d-flex flex-column justify-content-between padding">
        <div class="haut mb-3">
            <div class="gris_haut"></div>
            <button @click="disableEdit = !disableEdit" type="button" class="btn  modifier m-3" :class="{'editing' : !disableEdit }">Edit</button>
            <button v-on:click="logout" class="btn  deconnexion m-3 p-1">Logout</button>
            <div class="profil">{{ this.userInfo.username }}</div>
            <div class="avatar">
                <img class="profile-picture" :src="this.updatableData.profile_picture" alt="profile picture">
            </div>
        </div>
        <div v-if="infoUpdated" class="alert alert-success align-self-center" role="alert">
            Vos informations ont bien été mise à jour.
        </div>
        <div v-if="error" class="alert alert-danger align-self-center" role="alert">
            {{ this.message }}
        </div>
        <div v-if="this.userInfo.is_superuser" class="alert alert-primary align-self-center" role="alert">
                Vous êtes administrateur de cette application. &lsaquo;3
        </div>
        <form class="d-flex flex-column align-self-center flex-grow-1" @submit.prevent="updateData">
            <div class="mb-3">
                <label for="formFile" class="form-label">Nouvelle photo de profil ?</label>
                <img :src="remoteUrl" style="width: 80px" class="rounded">
                <input class="form-control" type="file" accept="image/*" id="formFile" @change="handleImage" :disabled="disableEdit">
            </div>
            <div class="mb-3">
                <label for="about" class="form-label">Description</label>
                <input type="text" name="about" id="about" v-model="this.updatableData.about"
                minlength="0" maxlength="300" class="form-control" :disabled="disableEdit"/>
            </div>
            <div class="mb-3">
                <label for="last_name" class="form-label">Last Name</label>
                <input type="text" name="last_name" id="last_name" 
                v-model="this.updatableData.last_name" minlength="4" maxlength="50" size="10" class="form-control" :disabled="disableEdit"/>
            </div>

            <div class="mb-3">
                <label for="first_name" class="form-label">First Name</label>
                <input type="text" name="first_name" id="first_name" 
                v-model="this.updatableData.first_name" minlength="4" maxlength="50" size="10" class="form-control" :disabled="disableEdit"/>
            </div>

            <div class="mb-3">
                <label for="postcode" class="form-label">Postcode</label>
                <input type="text" name="postcode" id="postcode" v-model="this.updatableData.postcode"
                minlength="3" maxlength="5" size="10" class="form-control" :disabled="disableEdit"/>
            </div>

            <div class="age mb-3">{{ this.updatableData.birthday }}</div>
        </form>
        <button data-bs-toggle="modal" data-bs-target="#exampleModal" type="button" class="btn btn-primary align-self-center" v-on:click="updateData" v-if="!disableEdit">
            Edit information
        </button>
        <LoopingRhombusesSpinner class="align-self-center"
            v-if="loading"
            :animation-duration="2500"
            :rhombus-size="15"
            color="#ff1d5e"
            />
    </div>
  </perfect-scrollbar>
</template>

<script>
import UserInformation from '../services/userInfo.service.js';
import { LoopingRhombusesSpinner } from 'epic-spinners'
export default {
    name: 'Profile',
    components: {
        LoopingRhombusesSpinner
    },
    data() {
        return {
            userInfo: {
                username: '',
                email: '',
                is_superuser: false,
                sign_up_data: ''
            },
            updatableData: {},
            newImage: '',
            remoteUrl: '',
            postcode: '',
            error: false,
            infoUpdated: false,
            message: "",
            loading: false,
            disableEdit: true
        }
    },
    computed: {
        isAuthenticated() {
            return this.$store.state.isAuthenticated;
        }
    },
    methods: {
        logout() {
            this.$store.dispatch('logout');
            this.$router.push('/');
        },
        handleImage(e) {
            const selectedImage = e.target.files[0];
            this.createBase64Image(selectedImage);
        },
        uploadImage() {
            this.loading = true;
            fetch('https://i.tpms.host/api/1/upload', {
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    key: 'c4118a8b942a7e4f1c89260c441e52eb', // ICI
                    source: this.newImage
                })
            }).then((resp) => resp.json()).then(json => {
                console.log(json);
                this.remoteUrl = json.image.url;
                this.loading = false;
            }).catch((err) => {
                this.message = err;
                console.log(err);
                this.loading = false;
            })
        },
        createBase64Image(fileObject){
            const oui = this;
            var btoa = require('btoa')
            const reader = new FileReader();
            reader.onload = function(event) {
                oui.newImage = btoa(event.target.result);
                oui.uploadImage()
            };
            reader.readAsBinaryString(fileObject);
        },
        updateData() {
            this.loading = true;
            this.updatableData.profile_picture = this.remoteUrl
            UserInformation.updateProfileInformation(this.updatableData).then((data) => {
                this.updatableData = data;
                this.infoUpdated = true;
                this.loading = false;
                setTimeout(() => this.infoUpdated = false, 3000);
            }).catch((error) => {
                this.error = true;
                this.message = error;
                this.loading = false;
            });
        },
        eventChangeTitle(){
            const data = {title: "Profil"};
            this.$emit('updateTitleName', data);
        }
    },
    beforeCreate() {
        if (!this.isAuthenticated) {
            this.logout;
        }
    },
    beforeMount() {
        if (!this.isAuthenticated) {
            this.logout;
        }
        this.$store.dispatch('setBasicInformation').then((data) => {
            this.userInfo = data;
            UserInformation.getMoreInformation().then((info) => {
                this.updatableData = info;
            }).catch((error) => {
                this.error = true;
                this.message = error;
            })
        }).catch((error) => {
            this.error = true;
            this.message = error;
        })
    },
    mounted() {
        this.eventChangeTitle();
    }
}
</script>

<style scoped>

.padding {
  padding-bottom: 100px;
}

.haut {
    display: grid;
    grid-template-columns: 25% 50% 25%;
    grid-template-rows: 1fr 1fr 1fr;
    background: linear-gradient(to right, #0084ff, #00f2ff);
}

.gris_haut {
    grid-column-start: 1;
    grid-column-end: 4;
    grid-row-start: 3;
    grid-row-end: 4;
    border-style: none;
    background-color: #fff;
}

.age {
    font-style: italic;
}

.modifier {
    color: #000000;
    background-color: white;
    font-size: calc(10px + 1vw);
}

.editing {
    background-color: red;
    color: white;
}

.deconnexion {
    color: #000000;
    background-color: white;
    grid-row-start: 1;
    grid-column-end: 4;
    font-size: calc(10px + 1vw);
    cursor: pointer;
}

.profil {
    display: inline-flex;
    justify-content: center;
    align-items: flex-end;
    color: #FDFAFA;
    font-size: calc(32px + 2vw);
    font-weight: 700;
}

.avatar {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: transparent;
    grid-row-start: 2;
    grid-row-end: 4;
    grid-column-start: 2;
    grid-column-end: 3;
}

.profile-picture {
    width: 90%;
    height: auto;
    max-width: 150px;
    border-radius: 50%;
}

.button {
    flex-basis: 0;
    flex-grow: 1;
    display: flex;
    justify-content: center;
    align-items: center;
}

@media (min-height: 700px) {
    .image {
        max-width: 200px;
    }
}

@media (min-width: 800px) and (min-height: 950px) {
    .image {
        max-width: 250px;
    }
}
</style>