<template>
  <div class="gastos-pendientes">
    <h3>Ver Gastos Pendientes</h3>
    <div class="form-group">
      <label for="hasta_mes">Mes:</label>
      <input type="number" v-model="hasta_mes" id="hasta_mes" class="form-control" min="1" max="12" required />
    </div>
    <div class="form-group">
      <label for="hasta_año">Año:</label>
      <input type="number" v-model="hasta_año" id="hasta_año" class="form-control" required />
    </div>
    <button @click="obtenerGastosPendientes" class="btn btn-primary">Obtener Pendientes</button>

    <div v-if="gastos.length" class="mt-3">
      <h4>Gastos Pendientes</h4>
      <ul class="list-group">
        <li v-for="gasto in gastos" :key="gasto.id" class="list-group-item">
          {{ gasto.departamento }} - {{ gasto.periodo }} - ${{ gasto.monto }}
        </li>
      </ul>
    </div>

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
      hasta_mes: '',
      hasta_año: '',
      gastos: [],
      mensaje: '',
    };
  },
  methods: {
    async obtenerGastosPendientes() {
      try {
        const response = await api.get('/gastos_pendientes', {
          params: {
            hasta_mes: this.hasta_mes,
            hasta_año: this.hasta_año,
          },
        });
        this.gastos = response.data.filter(
          (gasto) => gasto.estado === 'pendiente'
        ); // Filtrar por estado pendiente
        if (this.gastos.length === 0) {
          this.mensaje = 'No hay gastos pendientes para el período seleccionado.';
        } else {
          this.mensaje = '';
        }
      } catch (error) {
        console.error('Error obteniendo los gastos pendientes:', error);
        this.mensaje = 'Hubo un error al obtener los gastos pendientes.';
      }
    },
  },
};
</script>

<style scoped>
/* Agrega tus estilos aquí */
</style>