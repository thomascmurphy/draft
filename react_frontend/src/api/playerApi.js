class PlayerApi {
  static getPlayers(email) {
    if (!email) { email = '';}
    return fetch(`${process.env.API_HOST}/api/v1/players?email=` + email).then(response => {
      return response.json();
    }).catch(error => {
      return error;
    });
  }

  static getPack(hash) {
    if (!hash) { hash = '';}
    return fetch(`${process.env.API_HOST}/api/v1/players/` + hash + '/pack').then(response => {
      return response.json();
    }).catch(error => {
      return error;
    });
  }

  static makePick(packCardId) {
    const headers = Object.assign({'Content-Type': 'application/json'}, this.requestHeaders());
    const request = new Request(`${process.env.API_HOST}/api/v1/players/pick`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({pack_card_id: packCardId})
    });

    return fetch(request).then(response => {
      return response.json();
    }).catch(error => {
      return error;
    });
  }
}

export default PlayerApi;
