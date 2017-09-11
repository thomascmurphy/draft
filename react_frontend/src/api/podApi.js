class PodApi {
  static getAllPods() {
    return fetch('http://localhost:5000/api/v1/pods').then(response => {
      return response.json();
    }).catch(error => {
      return error;
    });
  }

  static updatePod(pod) {
    const request = new Request(`http://localhost:5000/api/v1/pods/${pod.id}`, {
      method: 'PUT',
      headers: new Headers({
        'Content-Type': 'application/json'
      }),
      body: JSON.stringify({pod: pod})
    });
  }
}

export default PodApi;
