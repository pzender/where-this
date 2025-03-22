<template>
  <div>
    <h2 class="text-center">Your guesses</h2>
    <!-- icons -->
    <div class="flex justify-evenly mt-4">
      <span v-for="(icon, index) in guessIcons" :key="index" :class="icon"></span>
    </div>
    <!-- last guess -->
    <div v-if="!lastGuess" class="text-center my-2">
      Put a pin on the map and click 'Guess' to start!
    </div>
    <div v-if="lastGuess" class="text-center my-2">Last guess: {{ lastGuessFormatted }}</div>
    <!-- last guess feedback -->
    <div v-if="lastGuess" class="text-center my-2">{{ lastGuessFeedback }}</div>
    <!-- final answer -->
    <div v-if="showAnswer" class="text-center my-2">
      {{ description }}
      {{ answerCoordinatesFormatted }}
    </div>
    <div v-else-if="lastGuess && isLastGuessInCountry" class="text-center my-2">
      {{ countryName }}
    </div>
  </div>
</template>
<script setup>
import { store, isFinished } from '@/utils/store'
import {
  directionAngle,
  distance,
  GUESS_TOLERANCE_KILOMETERS,
  isGuessCorrect,
  isGuessInCountry,
} from '@/utils/geographicUtils'
import { computed } from 'vue'

const props = defineProps({
  description: { type: String, default: null },
  countryCode: { type: String, default: null },
  countryName: { type: String, default: null },
})

const closeGuessThreshold = 1000
const guessIcons = computed(() => store.guesses.map(mapGuessToIcon))
const lastGuess = computed(() => store.guesses.filter((i) => i != null).slice(-1)[0])
const lastGuessFormatted = computed(() =>
  formatCoordinates(lastGuess.value.lat, lastGuess.value.lng),
)

const answerCoordinatesFormatted = computed(() =>
  formatCoordinates(store.target.lat, store.target.lng),
)
const showAnswer = computed(() => isFinished())
const lastGuessFeedback = computed(() => getFeedback())

const distanceToTarget = computed(() =>
  distance(lastGuess.value.lat, lastGuess.value.lng, store.target.lat, store.target.lng).toFixed(0),
)

const isLastGuessInCountry = computed(() =>
  isGuessInCountry(lastGuess.value.lat, lastGuess.value.lng, props.countryCode),
)

const isLastGuessCorrect = computed(() =>
  isGuessCorrect(lastGuess.value.lat, lastGuess.value.lng, store.target.lat, store.target.lng),
)

function mapGuessToIcon(guess) {
  if (guess == null) return showAnswer.value ? 'pi pi-minus' : 'pi pi-question' //'pi pi-question'

  const aLat = store.target.lat
  const aLng = store.target.lng
  const distanceToTarget = distance(guess.lat, guess.lng, aLat, aLng)

  if (distanceToTarget < GUESS_TOLERANCE_KILOMETERS) return 'pi pi-bullseye text-green-600'

  const heading = directionAngle(guess.lat, guess.lng, aLat, aLng)
  return {
    [heading > -45 && heading <= 45 && distanceToTarget > closeGuessThreshold]:
      'pi pi-angle-double-up text-red-600',
    [heading > -45 && heading <= 45 && distanceToTarget <= closeGuessThreshold]:
      'pi pi-angle-up text-yellow-600',
    [heading > 45 && heading <= 135 && distanceToTarget > closeGuessThreshold]:
      'pi pi-angle-double-right text-red-600',
    [heading > 45 && heading <= 135 && distanceToTarget <= closeGuessThreshold]:
      'pi pi-angle-right text-yellow-600',
    [heading > 135 || (heading <= -135 && distanceToTarget > closeGuessThreshold)]:
      'pi pi-angle-double-down text-red-600',
    [heading > 135 || (heading <= -135 && distanceToTarget <= closeGuessThreshold)]:
      'pi pi-angle-down text-yellow-600',
    [heading > -135 && heading <= -45 && distanceToTarget > closeGuessThreshold]:
      'pi pi-angle-double-left text-red-600',
    [heading > -135 && heading <= -45 && distanceToTarget <= closeGuessThreshold]:
      'pi pi-angle-left text-yellow-600',
  }[true]
}

function getFeedback() {
  if (isLastGuessCorrect.value)
    return `Correct! You were ${distanceToTarget.value} km away. Well done!`
  else if (isLastGuessInCountry.value)
    return `Close! Right country, but ${distanceToTarget.value} km away. Try again!`
  else if (distanceToTarget.value <= closeGuessThreshold)
    return `Not quite! You were ${distanceToTarget.value} km away. Keep trying!`
  else
    return `Incorrect! Your guess was ${distanceToTarget.value} km away. Try a different approach.`
}

function formatCoordinates(lat, lng) {
  const northSouth = lat > 0 ? 'N' : 'S'
  const eastWest = lng > 0 ? 'E' : 'W'
  return `(${Math.abs(lat).toFixed(3)} ${northSouth}, ${Math.abs(lng).toFixed(3)} ${eastWest})`
}
</script>
