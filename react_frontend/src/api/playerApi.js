class PlayerApi {
  static getPlayers(email) {
    if (!email) { email = '';}
    return fetch('http://localhost:5000/api/v1/players?email=' + email).then(response => {
      return response.json();
    }).catch(error => {
      return error;
    });
  }

  static getPack(hash) {
    if (!hash) { hash = '';}
    return fetch('http://localhost:5000/api/v1/players/' + hash + '/pack').then(response => {
      return response.json();
    }).catch(error => {
      return error;
    });
  }
}

export default PlayerApi;
