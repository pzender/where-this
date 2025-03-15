<template>
  <div>
    <h2 class="text-center">Your guesses</h2>
    <div class="flex justify-evenly mt-4">
      <span v-for="(icon, index) in guessIcons" :key="index" :class="icon"></span>
    </div>
    <div v-if="lastGuess" class="text-center my-2">
      Last guess: {{ lastGuessFormatted }}, off by {{ distanceToTarget }} km
    </div>
    <div v-else class="text-center my-2">Make your guess!</div>
    <div v-if="showAnswer" class="text-center my-2">
      Answer:
      {{ description }}
      {{ answerFormatted }}
    </div>
  </div>
</template>
<script setup>
import { store, isFinished } from '@/utils/store'
import { directionAngle, centralAngle, greatCircleDistance } from '@/utils/TrigonUtils'
import { computed } from 'vue'

defineProps({
  description: { type: String, default: null },
})

const guessIcons = computed(() => store.guesses.map(mapGuessToIcon))
const lastGuess = computed(() => store.guesses.filter((i) => i != null).slice(-1)[0])
const lastGuessFormatted = computed(() =>
  formatCoordinates(lastGuess.value.lat, lastGuess.value.lng),
)

const answerFormatted = computed(() => formatCoordinates(store.target.lat, store.target.lng))
const showAnswer = computed(() => isFinished())
const distanceToTarget = computed(() =>
  greatCircleDistance(
    lastGuess.value.lat,
    lastGuess.value.lng,
    store.target.lat,
    store.target.lng,
  ).toFixed(0),
)

function mapGuessToIcon(guess) {
  if (guess == null) return showAnswer.value ? 'pi pi-minus' : 'pi pi-question' //'pi pi-question'

  const aLat = store.target.lat
  const aLng = store.target.lng
  const angleDiff = centralAngle(guess.lat, guess.lng, aLat, aLng)
  if (angleDiff < 1) return 'pi pi-map-marker text-green-600'

  const heading = directionAngle(guess.lat, guess.lng, aLat, aLng)

  return {
    [heading > -45 && heading <= 45 && angleDiff > 15]: 'pi pi-angle-double-down text-red-600',
    [heading > -45 && heading <= 45 && angleDiff <= 15]: 'pi pi-angle-down text-yellow-600',
    [heading > 45 && heading <= 135 && angleDiff > 15]: 'pi pi-angle-double-left text-red-600',
    [heading > 45 && heading <= 135 && angleDiff <= 15]: 'pi pi-angle-left text-yellow-600',
    [heading > 135 || (heading <= -135 && angleDiff > 15)]: 'pi pi-angle-double-up text-red-600',
    [heading > 135 || (heading <= -135 && angleDiff <= 15)]: 'pi pi-angle-up text-yellow-600',
    [heading > -135 && heading <= -45 && angleDiff > 15]: 'pi pi-angle-double-right text-red-600',
    [heading > -135 && heading <= -45 && angleDiff <= 15]: 'pi pi-angle-right text-yellow-600',
  }[true]
}

function formatCoordinates(lat, lng) {
  const northSouth = lat > 0 ? 'N' : 'S'
  const eastWest = lng > 0 ? 'E' : 'W'
  return `(${Math.abs(lat).toFixed(3)} ${northSouth}, ${Math.abs(lng).toFixed(3)} ${eastWest})`
}
</script>
