<template>
  <button
    @click="$emit('click')"
    class="border border-solid border-violet-900 rounded-sm p-1 my-1 w-24 hover:bg-violet-900"
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
