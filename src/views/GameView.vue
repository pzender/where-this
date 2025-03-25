<template>
  <h2 class="base-header">Where is this?</h2>
  <div v-if="locationData">
    <photo-panel :photo-url="locationData.photo_url" />
    <photo-attribution
      :author-name="locationData?.author_name"
      :author-url="locationData?.author_url"
    />
    <div class="flex flex-col lg:flex-row mt-4">
      <div class="flex-1 order-1 lg:order-2">
        <leaflet-map />
      </div>
      <div class="flex-1 order-2 lg:order-1">
        <info-panel v-bind="infoPanelModel" />
      </div>
    </div>
  </div>
  <div v-else-if="isProcessing">
    <base-processing />
  </div>
  <div v-else>
    (whoops, we couldn't find a game at this date. try today's challenge
    <router-link to="/">here</router-link>)
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { store } from '@/utils/store'
import { ref } from 'vue'

import LeafletMap from '@/components/GuessLocation/LeafletMap.vue'
import PhotoAttribution from '@/components/GuessLocation/PhotoAttribution.vue'
import PhotoPanel from '@/components/GuessLocation/PhotoPanel.vue'
import InfoPanel from '@/components/GuessLocation/InfoPanel.vue'
import BaseProcessing from '@/components/Base/BaseProcessing.vue'
import { RouterLink, useRoute } from 'vue-router'

const locationData = ref(null)
const isProcessing = ref(false)
const route = useRoute()

const fetchLocationData = () => {
  fetch(dataPath.value, {
    headers: { 'Content-type': 'application/json' },
  })
    .then((res) => res.json())
    .then((response) => {
      const todayChallenge = response[dataKey.value]
      locationData.value = todayChallenge
      store.target = {
        lat: todayChallenge.location_lat,
        lng: todayChallenge.location_lng,
      }
    })
    .catch((error) => {
      console.warn('Looks like there was a problem: \n', error)
    })
    .finally(() => {
      isProcessing.value = false
    })
}

const infoPanelModel = computed(() => ({
  description: locationData.value.location_name,
  countryCode: locationData.value.country_code,
  countryName: locationData.value.country_name,
}))

const dataPath = computed(() => {
  return `challenge-lists/${challengeDate.value.year}-${challengeDate.value.month}.json`
})

const dataKey = computed(() => {
  return `${challengeDate.value.year}-${challengeDate.value.month}-${challengeDate.value.day}`
})

const challengeDate = computed(() => {
  const routeDate = route.params['date'].split('-')
  const today = new Date()
  const year = routeDate[0] ? routeDate[0] : String(today.getUTCFullYear())
  const month = routeDate[1] ? routeDate[1] : String(today.getUTCMonth() + 1).padStart(2, '0')
  const day = routeDate[2] ? routeDate[2] : String(today.getUTCDate()).padStart(2, '0')

  return {
    year,
    month,
    day,
  }
})

onMounted(() => {
  isProcessing.value = true
  fetchLocationData()
})
</script>
