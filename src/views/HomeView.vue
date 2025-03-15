<template>
  <guess-location :location-data="locationData" />
</template>

<script setup>
import GuessLocation from '@/components/GuessLocation/GuessLocation.vue'
import { store } from '@/utils/store'
const locationData = {
  author_name: 'Marvin Rozendal',
  author_url: 'https://unsplash.com/@muffinrozendal',
  daily_challenge_date: '2025-03-14',
  location_lat: -39.353815,
  location_lng: 174.438272,
  location_name: 'Taranaki, Nieuw-Zeeland',
  photo_url:
    'https://images.unsplash.com/photo-1574837074543-ff6a966fdcfd?ixid=M3w3MjEyMjJ8MHwxfGFsbHx8fHx8fHx8fDE3NDE4ODE2Njd8&ixlib=rb-4.0.3',
  provider_id: 'xXRD2ZWq2jo',
}

store.target = {
  lat: locationData.location_lat,
  lng: locationData.location_lng,
}
</script>
