<template>
  <h2 class="font-stretch-expanded font-bold py-1 text-lg bg-violet-900 text-center">
    Previous challenges
  </h2>
  <div v-if="data">
    <div v-for="entry in challenges" :key="entry">
      <history-row v-bind="mapRowDate(entry)" />
      <!-- {{ entry }} -->
    </div>
  </div>
</template>
<script setup>
import { computed, ref, onMounted } from 'vue'
import HistoryRow from '@/components/List/HistoryRow.vue'

const isProcessing = ref(false)
const data = ref(null)

const challenges = computed(() =>
  Object.keys(data.value)
    .sort()
    .filter((entry) => isChallengeVisible(entry))
    .map((entry) => data.value[entry]),
)

const fetchLocationData = (year, month) => {
  const dataPath = `challenge-lists/${year}-${month}.json`
  fetch(dataPath, {
    headers: { 'Content-type': 'application/json' },
  })
    .then((res) => res.json())
    .then((response) => {
      data.value = response
    })
    .catch((error) => {
      console.warn('Looks like there was a problem: \n', error)
    })
    .finally(() => {
      isProcessing.value = false
    })
}

const isChallengeVisible = (challengeDate) => {
  const today = new Date()
  const year = String(today.getUTCFullYear())
  const month = String(today.getUTCMonth() + 1).padStart(2, '0')
  const day = String(today.getUTCDate()).padStart(2, '0')
  const formattedCurrentDate = `${year}-${month}-${day}`
  return challengeDate <= formattedCurrentDate
}

const mapRowDate = (entry) => {
  // match with existing history from LocalStorage
  return {
    date: entry['daily_challenge_date'],
    photoUrl: entry['photo_url'],
    previousGuesses: [],
  }
}

onMounted(() => {
  isProcessing.value = true
  const today = new Date()
  const year = String(today.getUTCFullYear())
  const month = String(today.getUTCMonth() + 1).padStart(2, '0')
  fetchLocationData(year, month)
})
</script>
