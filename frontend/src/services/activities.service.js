const API_URL = "http://157.90.237.150/api/v1/";

/*
 * class pour gérer toutes les requêtes en lien avec les activités 
*/

class GestionActivities{
    // Recup les activités de l'user courant.
    async getActiveUserActivities(activitiesRequestInfo){
        const headers = {"Authorization": "Bearer " + localStorage.getItem('token')};
        const requestOptions = {
            headers: headers,
            method: 'GET',
        }
        const response = await fetch(API_URL + 'activity/me?' + new URLSearchParams(activitiesRequestInfo).toString(), requestOptions);
        const data = await response.json();
        if (!response.ok){
            const error = (data) || response.status;
            return Promise.reject(error.detail);
        }
        return data
    }

    async getActivitiesBySearch(activitiesRequestInfo) {
        const headers = {"Authorization": "Bearer " + localStorage.getItem('token')};
        const requestOptions = {
            headers: headers,
            method: 'GET',
        }
        const response = await fetch(API_URL + 'activity?' + new URLSearchParams(activitiesRequestInfo).toString(), requestOptions);
        const data = await response.json();
        if (!response.ok){
            const error = (data) || response.status;
            return Promise.reject(error.detail);
        }
        return data
    }

    async getActivityWithId(activityId) {
        const headers = {"Authorization": "Bearer " + localStorage.getItem('token')};
        const requestOptions = {
            headers: headers,
            method: 'GET',
        }
        const response = await fetch(API_URL + 'activity/' + activityId, requestOptions);
        const data = await response.json();
        if (!response.ok){
            const error = (data) || response.status;
            return Promise.reject(error.detail);
        }
        return data
    }

    async updateActivity(activityData) {
        const headers = {"Authorization": "Bearer " + localStorage.getItem('token')};
        const requestOptions = {
            headers: headers,
            method: 'PUT',
            body: JSON.stringify(activityData),
        }
        const response = await fetch(API_URL + 'activity/me', requestOptions);
        const data = await response.json();
        if (!response.ok){
            const error = (data) || response.status;
            return Promise.reject(error.detail);
        }
        return data
    }

    async deleteActivity(activityId) {
        const headers = {"Authorization": "Bearer " + localStorage.getItem('token')};
        const requestOptions = {
            headers: headers,
            method: 'DELETE'
        }
        const response = await fetch(API_URL + 'activity/' + activityId, requestOptions);
        const data = await response.json();
        if (!response.ok){
            const error = (data) || response.status;
            return Promise.reject(error.detail);
        }
        return data
    }

    async createActivity(activitiesInfo) {
        const headers = {"Authorization": "Bearer " + localStorage.getItem('token')};
        const requestOptions = {
            headers: headers,
            method: 'POST',
            body: JSON.stringify(activitiesInfo)
        };
        const response = await fetch(API_URL + 'activity/me', requestOptions);
        const data = await response.json();
        if (!response.ok){
            const error = (data) || response.status;
            return Promise.reject(error.detail);
        }
        return data
    }

    async getSports() {
        const headers = {"Authorization": "Bearer " + localStorage.getItem('token')};
        const requestOptions = {
            headers: headers,
            method: 'GET',
        }
        const response = await fetch(API_URL + 'misc/sports', requestOptions);
        const data = await response.json();
        if (!response.ok){
            const error = (data) || response.status;
            return Promise.reject(error.detail);
        }
        return data
    }

    async getLevels() {
        const headers = {"Authorization": "Bearer " + localStorage.getItem('token')};
        const requestOptions = {
            headers: headers,
            method: 'GET',
        }
        const response = await fetch(API_URL + 'misc/levels', requestOptions);
        const data = await response.json();
        if (!response.ok){
            const error = (data) || response.status;
            return Promise.reject(error.detail);
        }
        return data
    }
}

export default new GestionActivities;