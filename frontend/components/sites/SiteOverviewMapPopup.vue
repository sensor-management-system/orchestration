<!--
SPDX-FileCopyrightText: 2020 - 2024
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <l-popup :options="{ closeButton: false, className: 'site-overview-popup', minWidth:300}">
    <v-card elevation="2" class="site-overview-popup-card-positioning">
      <v-card-title class="headline site-overview-popup-card-text-wrap">
        {{ value.label }}
      </v-card-title>
      <v-divider />
      <v-card-text class="pa-0">
        <v-list>
          <v-list-item
            dense
            :to="detailLink"
          >
            <v-list-item-content>
              <v-list-item-title>
                <v-icon
                  left
                  small
                >
                  mdi-open-in-new
                </v-icon>
                View
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <slot name="additonal-actions" :popup-site="value" />
        </v-list>
      </v-card-text>
    </v-card>
  </l-popup>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { Site } from '@/models/Site'

@Component
export default class SiteOverviewMapPopup extends Vue {
  @Prop({
    required: true,
    type: Site
  })
  readonly value!: Site

  get detailLink (): string {
    const params = '?' + (new URLSearchParams({ from: 'searchResult' })).toString()
    return `/sites/${this.value.id}${params}`
  }
}

</script>
<style>
.site-overview-popup-card-positioning{
  position: relative;
  top:12px;
}

/* Remove default Leaflet popup styles */
.site-overview-popup .leaflet-popup-content-wrapper {
  background-color: transparent; /* Remove background */
  border: none; /* Remove border */
  box-shadow: none; /* Remove shadow */
  padding: 0; /* Remove padding */
}

.site-overview-popup-card-text-wrap{
  word-break: break-word;
  white-space: normal;
  overflow-wrap: break-word;
}
</style>
