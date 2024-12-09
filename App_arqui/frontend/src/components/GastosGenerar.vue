<template>
  <div class="gastos-generar">
    <h3>Generar Gastos Comunes</h3>
    <div class="form-group">
      <label for="mes">Mes:</label>
      <input type="number" v-model="mes" id="mes" class="form-control" min="1" max="12" required />
    </div>
    <div class="form-group">
      <label for="año">Año:</label>
      <input type="number" v-model="año" id="año" class="form-control" required />
    </div>
    <button @click="generarGastos" class="btn btn-primary">Generar</button>

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
      mes: '',
      año: '',
      mensaje: '',
    };
  },
  methods: {
    async generarGastos() {
      // Enviar los datos al backend
      try {
        const response = await api.post('/gastos', {
          mes: this.mes,
          año: this.año,
        });
        this.mensaje = response.data.mensaje;
      } catch (error) {
        console.error('Error generando los gastos:', error);
        this.mensaje = 'Hubo un error al generar los gastos.';
      }
    },
  },
};
</script>

<style scoped>
/* Agrega tus estilos aquí */
</style>
