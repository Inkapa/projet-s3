import { createRouter, createWebHashHistory } from 'vue-router'
import Accueil from '../views/Accueil.vue'
import Login from '../views/Login.vue'
import Profile from '../views/Profile.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import UserActivities from '../views/UserActivities.vue'
import CreateActivity from '../views/CreateActivity.vue'
import ActivityPage from '../views/ActivityPage.vue'
import User from '../views/User.vue'
import Sportives from '../views/Sportives.vue'
import UserParticipations from '../views/UserParticipations.vue'
import ResetPwd from '../views/ResetPwd.vue'
import ChangePwd from '../views/ChangePwd.vue'

const routes = [{
        path: '/',
        name: 'Accueil',
        component: Accueil
    },
    {
        path: '/home',
        name: 'Home',
        component: Home
    },
    {
        path: '/sportives',
        name: 'Sportives',
        component: Sportives
    },
    {
        path: '/userActivities',
        name: 'UserActivities',
        component: UserActivities
    },
    {
        path: '/userParticipations',
        name: 'UserParticipations',
        component: UserParticipations
    },
    {
        path: '/createActivity',
        name: 'CreateActivity',
        component: CreateActivity
    },
    {
        path: '/activityPage/:id',
        name: 'ActivityPage',
        component: ActivityPage
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
    },
    {
        path: '/profile',
        name: 'Profile',
        component: Profile
    },
    {
        path: '/user/:username',
        name: 'User',
        component: User
    },
    {
        path: '/resetpwd',
        name: 'ResetPwd',
        component: ResetPwd
    },
    {
        path: '/reset-password',
        name: 'ChangePwd',
        component: ChangePwd
    }
]
const router = createRouter({
    history: createWebHashHistory(),
    routes
})

// router.beforeEach((to, from, next) => {
//     if ((to.path !== 'Accueil' && to.path !== '/login' && to.path !== '/register' && to.path !== '/' && to.path !== '/resetpwd' && to.name !== 'ChangePwd') 
//     && !localStorage.getItem('token')) next({ name: 'Login' })
//     else next()
// })


export default router