import { reactive } from 'vue'
import { ALLOWED_GUESSES } from './configs'
import { isGuessCorrect } from './geographicUtils'

export const emptyGuesses = () => new Array(ALLOWED_GUESSES).fill(null)

// TODO: this should probably keep entire history as dictionary & work based on dates as keys / keep stuff in localStorage

export const store = reactive({
  guesses: emptyGuesses(),
  target: {},
})
export const isFull = () => store.guesses.every((g) => g !== null)
export const hasCorrectGuess = () =>
  store.guesses
    .filter((g) => g !== null)
    .some((g) => isGuessCorrect(g.lat, g.lng, store.target.lat, store.target.lng))
export const isFinished = () => isFull() || hasCorrectGuess()

export const addGuess = (value) => {
  if (store.isFull) {
    console.warn('adding a guess to a full store!')
    return
  }
  store.guesses[store.guesses.indexOf(null)] = value
}

export const clearGuesses = () => {
  store.guesses = emptyGuesses()
}
