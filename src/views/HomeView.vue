<template>
  <guess-location v-if="locationData" :location-data="locationData" />
</template>

<script setup>
import GuessLocation from '@/components/GuessLocation/GuessLocation.vue'
import { onMounted } from 'vue'
import { store } from '@/utils/store'
import { ref } from 'vue'

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

onMounted(() => {
  fetchLocationData()
})
</script>
