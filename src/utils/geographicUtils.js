import { rhumbBearing, point, rhumbDistance, polygon, pointToPolygonDistance } from '@turf/turf'
import simplifiedBorders from './simplifiedBorders'

export const GUESS_TOLERANCE_KILOMETERS = 50

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
  const countryBorders = simplifiedBorders[countryCode].borders.map((l) => polygon([l]))

  return countryBorders.some((poly) => pointToPolygonDistance(guess, poly) < 0)
}
