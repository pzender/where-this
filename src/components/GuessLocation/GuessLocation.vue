<template>
  <div class="flex flex-col lg:flex-row">
    <div class="flex-2 p-2">
      <h2 class="text-center">Where this?</h2>
      <photo-panel :photo-url="locationData?.photo_url" />
      <photo-attribution
        :author-name="locationData?.author_name"
        :author-url="locationData?.author_url"
      />
    </div>
    <div class="flex-1 p-2">
      <div class="flex flex-col justify-between h-full">
        <div class="flex-none order-1 lg:order-2">
          <leaflet-map />
        </div>
        <div class="grow order-2 lg:order-1">
          <info-panel :description="locationData?.location_name" />
        </div>
        <div class="order-last text-right text-xs font-thin italic">v.0.2.0</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import LeafletMap from './LeafletMap.vue'
import PhotoAttribution from './PhotoAttribution.vue'
import PhotoPanel from './PhotoPanel.vue'

import InfoPanel from './InfoPanel.vue'

defineProps({
  locationData: { type: Object, default: null },
})
</script>
