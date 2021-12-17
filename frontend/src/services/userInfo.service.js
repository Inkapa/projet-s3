const API_URL = "http://157.90.237.150/api/v1/";

/*
 * Classe pour récupérer les données de l'utilisateur 
 */
class UserInformation{
    // récupère les infos sur l'utilisateur courant
    async getBasicInformation() {
        const headers = {"Authorization": "Bearer " + localStorage.getItem('token')};
        const requestOptions = {
            headers: headers,
            method: 'GET',
        }
        const response = await fetch(API_URL + 'account/me', requestOptions);
        const data = await response.json();
        if (!response.ok || !data.username || !data.email){
            const error = (data) || response.status;
            return Promise.reject(error);
        }
        return data
    }

    // Récupère les détails sur l'utilisateur courant (firstName, lastName, about, postcode)
    async getMoreInformation() {
        const headers = {"Authorization": "Bearer " + localStorage.getItem('token')};
        const requestOptions = {
            headers: headers,
            method: 'GET'
        };
        const response = await fetch(API_URL + 'account_data/me', requestOptions);
        const data = await response.json();
        if (!response.ok){
            const error = (data) || response.status;
            return Promise.reject(error);
        }
        return Promise.resolve(data);
    }

    // Met à jour les informations de l'utilisateur
    async updateProfileInformation(newInformation) {
        const headers = {"Authorization": "Bearer " + localStorage.getItem('token'), "Content-Type": "application/json"};
        const requestOptions = {
            headers: headers,
            method: 'PUT',
            body: JSON.stringify(newInformation)
        };
        return await fetch(API_URL + 'account_data/me', requestOptions).then((response) => {
            const data = response.json();
            if (!response.ok){
                const error = (data) || response.status;
                return Promise.reject(error);
            }
            return Promise.resolve(data);
        });
    }
}

export default new UserInformation();