<template>
  <div id="map" :class="mapCssClass"></div>
  <div class="flex justify-between">
    <base-button @click="onClear" text="clear" />
    <base-button @click="onCenter" text="center map" />
    <base-button @click="onLock" text="lock" />
  </div>
</template>

<script setup>
import 'leaflet/dist/leaflet.css'
import * as L from 'leaflet'

import { computed, onMounted, ref } from 'vue'

import { addGuess, clearGuesses, isFinished } from '@/utils/store'
import BaseButton from '../Base/BaseButton.vue'

const mapBounds = L.LatLngBounds(L.LatLng(-90.0, -180.0), L.LatLng(90.0, 180.0))
let leafletMap = null
let markers = []
let isLocked = false

onMounted(() => {
  leafletMap = L.map('map', {
    center: [0.0, 0.0],
    zoom: 2,
    maxBounds: mapBounds,
    maxBoundsViscosity: 1.0,
  })

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 6,
    minZoom: 2,
    noWrap: false,
    maxBounds: mapBounds,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(leafletMap)

  leafletMap.on('click', onMapClick)
  //   leafletMap.on('drag', onMapDrag)
})

function onMapClick(event) {
  if (isFinished()) return
  const marker = getCurrentMarker()
  marker.setLatLng(event.latlng)
  marker.addTo(leafletMap)
  isLocked = false
}

function getCurrentMarker() {
  if (isLocked || markers.length === 0) {
    markers.push(new L.marker())
  }

  const lastIndex = markers.length - 1
  return markers[lastIndex]
}

function onClear() {
  while (markers.length > 0) {
    const marker = markers.pop()
    marker.removeFrom(leafletMap)
  }

  clearGuesses()
}

function onLock() {
  if (isLocked || markers.length === 0) return
  if (isFinished()) return // probably want to do something different then
  const currentGuess = getCurrentMarker().getLatLng()
  addGuess(currentGuess)

  isLocked = true
}

const isExpanded = ref(false)
const mapCssClass = computed(() => (isExpanded.value ? 'h-128' : 'h-128 lg:h-64 xl:h-96'))
</script>

<style></style>
