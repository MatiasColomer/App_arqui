<template>
  <div id="app">
    <header class="text-center py-3 bg-primary text-white">
      <h1>Gestión de Gastos Comunes</h1>
    </header>
    <nav class="d-flex justify-content-center bg-light py-2">
      <button 
        @click="setView('generar')" 
        class="btn btn-outline-primary btn-sm mx-2"
      >
        Generar Gastos
      </button>
      <button 
        @click="setView('pago')" 
        class="btn btn-outline-primary btn-sm mx-2"
      >
        Registrar Pago
      </button>
      <button 
        @click="setView('pendientes')" 
        class="btn btn-outline-primary btn-sm mx-2"
      >
        Ver Pendientes
      </button>
    </nav>
    <main class="container mt-4">
      <GastosGenerar v-if="view === 'generar'" />
      <GastosPago v-if="view === 'pago'" />
      <GastosPendientes v-if="view === 'pendientes'" />
    </main>
  </div>
</template>

<script>
import GastosGenerar from './components/GastosGenerar.vue';
import GastosPago from './components/GastosPago.vue';
import GastosPendientes from './components/GastosPendientes.vue';

export default {
  data() {
    return {
      view: 'generar',
    };
  },
  methods: {
    setView(view) {
      this.view = view;
    },
  },
  components: {
    GastosGenerar,
    GastosPago,
    GastosPendientes,
  },
};
</script>

<style>
/* Elimina cualquier margen extra del body */
body {
  margin: 0;
}
</style>
