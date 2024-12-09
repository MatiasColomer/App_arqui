<script setup>
defineProps({
  msg: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div>
    <h1>¡Hola, mundo!</h1>
    <p>Este es tu primer componente en Vue 3 🚀</p>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
};
</script>

<style scoped>
h1 {
  color: #42b983;
}
</style>
