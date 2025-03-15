<template>
  <button
    @click="$emit('click')"
    class="border border-solid border-orange-400 rounded-sm p-1 my-1 w-24 hover:bg-orange-400"
  >
    {{ text }}
  </button>
</template>
<script setup>
defineEmits(['click'])
defineProps({
  text: { type: String, default: null },
})
</script>
