<template>
  <div class="gastos-pago">
    <h3>Registrar Pago</h3>
    <div class="form-group">
      <label for="departamento">Departamento:</label>
      <input type="number" v-model="departamento" id="departamento" class="form-control" required />
    </div>
    <div class="form-group">
      <label for="periodo">Periodo:</label>
      <input type="text" v-model="periodo" id="periodo" class="form-control" required />
    </div>
    <div class="form-group">
      <label for="fecha_pago">Fecha de Pago:</label>
      <input type="date" v-model="fecha_pago" id="fecha_pago" class="form-control" required />
    </div>
    <button @click="registrarPago" class="btn btn-primary">Registrar Pago</button>

    <div v-if="mensaje" class="alert alert-info mt-3">
      {{ mensaje }}
    </div>
  </div>
</template>

<script>
import api from '../axios'; // Importa Axios

export default {
  data() {
    return {
      departamento: '',
      periodo: '',
      fecha_pago: '',
      mensaje: '',
    };
  },
  methods: {
    async registrarPago() {
      // Enviar los datos al backend
      try {
        const response = await api.post('/pago', {
          departamento: this.departamento,
          periodo: this.periodo,
          fecha_pago: this.fecha_pago,
        });
        this.mensaje = response.data.estado;
      } catch (error) {
        console.error('Error registrando el pago:', error);
        this.mensaje = 'Hubo un error al registrar el pago.';
      }
    },
  },
};
</script>

<style scoped>
/* Agrega tus estilos aquí */
</style>
