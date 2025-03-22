<template>
  <h2 class="font-stretch-expanded font-bold py-1 text-lg bg-orange-900 text-center">
    Where this?
  </h2>
  <photo-panel v-if="locationData" :photo-url="locationData.photo_url" />
  <photo-attribution
    v-if="locationData"
    :author-name="locationData?.author_name"
    :author-url="locationData?.author_url"
  />
  <div class="flex flex-col lg:flex-row">
    <div class="flex-1 order-1 lg:order-2">
      <leaflet-map v-if="locationData" />
    </div>
    <div class="flex-1 order-2 lg:order-1">
      <info-panel v-if="locationData" v-bind="infoPanelModel" />
    </div>
  </div>
  <div class="order-last text-right text-xs font-thin italic">v.0.2.0</div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { store } from '@/utils/store'
import { ref } from 'vue'

import LeafletMap from '@/components/GuessLocation/LeafletMap.vue'
import PhotoAttribution from '@/components/GuessLocation/PhotoAttribution.vue'
import PhotoPanel from '@/components/GuessLocation/PhotoPanel.vue'
import InfoPanel from '@/components/GuessLocation/InfoPanel.vue'

const locationData = ref(null)

const fetchLocationData = () => {
  fetch('challenge-lists/2025-03.json', {
    headers: { 'Content-type': 'application/json' },
  })
    .then((res) => res.json())
    .then((response) => {
      console.log({ response })
      const todayChallenge = response['2025-03-15']
      locationData.value = todayChallenge
      store.target = {
        lat: todayChallenge.location_lat,
        lng: todayChallenge.location_lng,
      }
    })
    .catch((error) => {
      console.log('Looks like there was a problem: \n', error)
    })
}

const infoPanelModel = computed(() => ({
  description: locationData.value.location_name,
  countryCode: locationData.value.country_code,
  countryName: locationData.value.country_name,
}))

onMounted(() => {
  fetchLocationData()
})
</script>
