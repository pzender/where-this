<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>
<template>
  <nav>
    <RouterLink to="/">Home</RouterLink>
  </nav>
  <div class="w-9/10 m-auto bg-stone-900">
    <RouterView />
  </div>
</template>

<style scoped></style>
