<template>
  <img :src="photoUrl" />
</template>
<script setup>
defineProps({
  photoUrl: { type: String, default: null },
})
</script>
