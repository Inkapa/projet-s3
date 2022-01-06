class GestionParticipations{

    async getActiveUserParticipations(participationRequestInfo){
        const headers = {"Authorization": "Bearer " + localStorage.getItem('token')};
        const requestOptions = {
            headers: headers,
            method: 'GET',
        }
        const response = await fetch(process.env.VUE_APP_API_URL + 'participation/me?' + new URLSearchParams(participationRequestInfo).toString(), requestOptions);
        const data = await response.json();
        if (!response.ok){
            const error = (data) || response.status;
            return Promise.reject(error.detail);
        }
        return data
    }

    //TO DO:
    async addMyParticipation(requestInfo) {
        const headers = {"Authorization": "Bearer " + localStorage.getItem('token')};
        const requestOptions = {
            headers: headers,
            method: 'POST',
            body: JSON.stringify(requestInfo),
        }
        const response = await fetch(process.env.VUE_APP_API_URL + 'participation/me', requestOptions);
        const data = await response.json();
        if (!response.ok){
            const error = (data) || response.status;
            return Promise.reject(error.detail);
        }
        return data
    }

    async removeMyParticipation(id) {
        const headers = {"Authorization": "Bearer " + localStorage.getItem('token')};
        const requestOptions = {
            headers: headers,
            method: 'DELETE',
        }
        const response = await fetch(process.env.VUE_APP_API_URL + 'participation/' + id, requestOptions);
        const data = await response.json();
        if (!response.ok){
            const error = (data) || response.status;
            return Promise.reject(error.detail);
        }
        return data
    }

}

export default new GestionParticipations();