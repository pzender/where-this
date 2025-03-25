<template>
  <div class="text-center text-xs font-thin italic bg-stone-800 py-1">
    Photo by
    <a :href="authorLink" class="underline hover:text-highlight">
      {{ authorName }}
    </a>
    on
    <a :href="unsplashLink" class="underline hover:text-highlight"> Unsplash</a>
  </div>
</template>
<script setup>
import { computed } from 'vue'

const props = defineProps({
  authorName: { type: String, default: null },
  authorUrl: { type: String, default: null },
})

const authorLink = computed(() => appendUtms(props.authorUrl))
const unsplashLink = computed(() => appendUtms('https://unsplash.com'))

function appendUtms(src_url) {
  let url = new URL(src_url)
  url.searchParams.set('utm_source', 'where-is-this')
  url.searchParams.set('utm_medium', 'referral')
  return url
}
</script>
