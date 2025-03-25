import { rhumbBearing, point, rhumbDistance, polygon, pointToPolygonDistance } from '@turf/turf'
import simplifiedBorders from './simplifiedBorders'
import { GUESS_TOLERANCE_KILOMETERS } from './configs'

export function directionAngle(gLat, gLng, aLat, aLng) {
  const guess = point([gLng, gLat])
  const target = point([aLng, aLat])

  return rhumbBearing(guess, target)
}

export function distance(gLat, gLng, aLat, aLng) {
  const guess = point([gLng, gLat])
  const target = point([aLng, aLat])

  return rhumbDistance(guess, target, { units: 'kilometers' })
}

export function isGuessCorrect(gLat, gLng, aLat, aLng) {
  return distance(gLat, gLng, aLat, aLng) < GUESS_TOLERANCE_KILOMETERS
}

export function isGuessInCountry(gLat, gLng, countryCode) {
  const guess = point([gLng, gLat])
  const countryBorders = simplifiedBorders[countryCode].borders
  const isPoint = countryBorders.length === 1 && countryBorders[0].length === 1

  return isPoint
    ? rhumbDistance(guess, point(countryBorders[0])) < GUESS_TOLERANCE_KILOMETERS
    : countryBorders.some((vertices) => pointToPolygonDistance(guess, polygon([vertices])) < 0)
}
