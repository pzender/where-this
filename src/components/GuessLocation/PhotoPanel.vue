<template>
  <img :src="urlWithParams" />
</template>
<script setup>
import { computed } from 'vue'

const props = defineProps({
  photoUrl: { type: String, default: null },
})

const urlWithParams = computed(() => appendParams(props.photoUrl))

function appendParams(src_url) {
  let url = new URL(src_url)
  url.searchParams.set('w', '1280')
  url.searchParams.set('h', '720')
  url.searchParams.set('fit', 'crop')
  return url
}
</script>
