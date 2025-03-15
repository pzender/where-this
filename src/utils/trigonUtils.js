const EARTH_RADIUS_KM = 6371

function centralAngleRadians(gLat, gLng, aLat, aLng) {
  const gLatRad = (gLat * Math.PI) / 180
  const aLatRad = (aLat * Math.PI) / 180
  const dLatRad = ((aLat - gLat) * Math.PI) / 180
  const dLngRad = ((aLng - gLng) * Math.PI) / 180

  const a =
    Math.sin(dLatRad / 2) * Math.sin(dLatRad / 2) +
    Math.cos(gLatRad) * Math.cos(aLatRad) * Math.sin(dLngRad / 2) * Math.sin(dLngRad / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return c
}

export function centralAngle(gLat, gLng, aLat, aLng) {
  const centralAngleRad = centralAngleRadians(gLat, gLng, aLat, aLng)
  return centralAngleRad / (Math.PI / 180)
}

export function greatCircleDistance(gLat, gLng, aLat, aLng) {
  return centralAngleRadians(gLat, gLng, aLat, aLng) * EARTH_RADIUS_KM
}

export function directionAngle(gLat, gLng, aLat, aLng) {
  const dLat = gLat - aLat
  const dLng = gLng - aLng
  return (Math.atan2(dLng, dLat) * 180) / Math.PI
}
