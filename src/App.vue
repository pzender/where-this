<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>
<template>
  <div class="w-9/10 max-w-7xl m-auto bg-stone-900">
    <nav class="flex">
      <RouterLink to="/" class="flex-1 py-1 hover:bg-orange-900 text-center">Play</RouterLink>
      <RouterLink to="/" class="flex-1 py-1 hover:bg-orange-900 text-center"
        >Previous challenges</RouterLink
      >
    </nav>
    <RouterView />
  </div>
</template>

<style scoped></style>
