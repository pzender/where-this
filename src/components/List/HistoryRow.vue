<template>
  <div class="flex my-1">
    <img :src="urlWithParams" class="flex-none" />
    <div class="flex-grow p-2 h-full">playable on {{ date }}</div>
    <div class="flex-none p-2 h-full align-middle">
      <router-link :to="date" class="base-button">try! </router-link>
    </div>
  </div>
</template>
<script setup>
import { computed } from 'vue'

const props = defineProps({
  date: { type: String, default: null },
  photoUrl: { type: String, default: null },
  previousGuesses: { type: Array, default: [] },
})

const urlWithParams = computed(() => appendParams(props.photoUrl))

function appendParams(src_url) {
  let url = new URL(src_url)
  url.searchParams.set('w', '128')
  url.searchParams.set('h', '72')
  url.searchParams.set('fit', 'crop')
  return url
}
</script>
