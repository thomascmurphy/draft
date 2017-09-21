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

  static getDeck(hash) {
    if (!hash) { hash = '';}
    return fetch(`${process.env.API_HOST}/api/v1/players/` + hash + '/deck').then(response => {
      return response.json();
    }).catch(error => {
      return error;
    });
  }

  static makePick(packCardId) {
    var formData = new FormData();
    formData.append('pack_card_id', packCardId);
    const request = new Request(`${process.env.API_HOST}/api/v1/players/pick`, {
      method: 'post',
      headers: new Headers({
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }),
      body: JSON.stringify({pack_card_id: packCardId}),
      mode: 'cors'
    });

    return fetch(request).then(response => {
      return response.json();
    }).catch(error => {
      return error;
    });
  }

  static getCardImages(hash) {
    if (!hash) { hash = '';}
    return fetch(`${process.env.API_HOST}/api/v1/players/` + hash + '/card_images').then(response => {
      return response.json();
    }).catch(error => {
      return error;
    });
  }
}

export default PlayerApi;
