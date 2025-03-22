<template>
  <button
    @click="$emit('click')"
    class="border border-solid border-orange-900 rounded-sm p-1 my-1 w-24 hover:bg-orange-900"
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
