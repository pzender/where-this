<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>
<template>
  <div class="w-9/10 max-w-7xl m-auto bg-stone-900">
    <nav class="flex py-2">
      <router-link to="/" class="flex-1 py-1 hover:bg-highlight text-center">
        Play current
      </router-link>
      <router-link to="/previous" class="flex-1 py-1 hover:bg-highlight text-center">
        Previous challenges
      </router-link>
    </nav>
    <router-view :key="$route.fullPath" />
    <div class="text-right text-xs font-thin italic">v.0.3.0</div>
  </div>
</template>
