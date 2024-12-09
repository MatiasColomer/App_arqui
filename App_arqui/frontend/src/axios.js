import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000',  // URL de tu API Flask
  timeout: 10000,  // Tiempo de espera de la solicitud (10 segundos)
});

export default api;
