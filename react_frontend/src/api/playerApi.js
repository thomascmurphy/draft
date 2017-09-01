class PlayerApi {
  static getAllHobbies() {
    return fetch('http://localhost:5000/api/v1/players').then(response => {
      return response.json()
    }).catch(error => {
      return error
    });
  }
};

export default PlayerApi;
