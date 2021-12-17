const API_URL = "http://157.90.237.150/api/v1/";

/*
 * Ici c'est la classe qui gère le login et la création de compte
 * Pour les erreurs c'est fait directement par Liam dans le body.detail
 */
class AuthService {
    // Envoi l'username et le mot de passe pour recevoir un token
    async login(userInfo) {
        //prépare les éléments pour la requete
        const postData = {grant_type: '', username: userInfo.username, password: userInfo.password, scope: '', client_id: '', client_secret: ''}
        const headers = {Accept: "application/json", 'Content-Type': 'application/x-www-form-urlencoded'};
        const requestOptions = {
            body: new URLSearchParams(postData),
            headers: headers,
            method: 'POST',
        };
        const response = await fetch(API_URL + 'login/access-token', requestOptions);
        const data = await response.json();
        // Si réponse 400/500 ou si il n'y a pas de token, cela renvoi une erreur 
        if (!response.ok || !data.access_token) {
            const error = (data) || response.status;
            // gestion de l'erreur ici
            // error.detail donne directement le message de l'api
            return Promise.reject(error.detail);
        }
        localStorage.setItem('access-token', JSON.stringify(data.access_token));
        return await data;
    }
    async register(userInfo) {
        const headers = {Accept: "application/json","Content-Type": "application/json"}
        const requestOptions = {
            body: JSON.stringify(userInfo),
            headers: headers,
            method: 'POST',
        };
        console.log(userInfo);
        const response = await fetch(API_URL + 'register', requestOptions);
        const data = await response.json();
        if (!response.ok){
            const error = (data) || response.status;
            return Promise.reject(error.detail);
        }
        return Promise.resolve(data);
    }
}

export default new AuthService();