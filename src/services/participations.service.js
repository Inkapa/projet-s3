const API_URL = "http://157.90.237.150/api/v1/";


class GestionParticipations{
    //TO DO:
    async addMyParticipation(requestInfo) {
        const headers = {"Authorization": "Bearer " + localStorage.getItem('token')};
        const requestOptions = {
            headers: headers,
            method: 'POST',
            body: JSON.stringify(requestInfo),
        }
        const response = await fetch(API_URL + 'participation/me', requestOptions);
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
        const response = await fetch(API_URL + 'participation/' + id, requestOptions);
        const data = await response.json();
        if (!response.ok){
            const error = (data) || response.status;
            return Promise.reject(error.detail);
        }
        return data
    }

}

export default new GestionParticipations();