class PodApi {
  static getAllPods() {
    return fetch('http://localhost:5000/api/v1/pods').then(response => {
      return response.json();
    }).catch(error => {
      return error;
    });
  }

export default PodApi;
