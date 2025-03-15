import { reactive } from 'vue'
import { ALLOWED_GUESSES } from './configs'
import { centralAngle } from './TrigonUtils'

export const emptyGuesses = () => new Array(ALLOWED_GUESSES).fill(null)

export const store = reactive({
  guesses: emptyGuesses(),
  target: {},
})
export const isFull = () => store.guesses.every((g) => g !== null)
export const hasCorrectGuess = () =>
  store.guesses
    .filter((g) => g !== null)
    .some((g) => centralAngle(g.lat, g.lng, store.target.lat, store.target.lng) < 1)
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
