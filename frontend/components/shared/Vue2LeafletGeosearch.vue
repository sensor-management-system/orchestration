<!--
SPDX-FileCopyrightText: 2020 - 2022
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div />
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { GeoSearchControl } from 'leaflet-geosearch'

/*
 * This component has been adapted from https://github.com/fega/vue2-leaflet-geosearch
 * under the MIT license
 *
 * We have quite a lot of ts-ignore annotations in this code. In this past
 * this was just plain js code without any type annotations.
 * However, after updating to nuxt-edge, jest started to complain about this file
 * here (especially the @Component decorator). We realized that jest handles
 * typescript and javascript files quite differently in order of the transformations
 * that it does with babel.
 * While enabling those transformations for the js files, seems to be quite complex
 * (and non of the codesnippets in the documentation worked as expected), it seemed
 * easier to just transform this file here to typescript (which is handled correctly
 * by jest - even with decorators).
 * However: For the moment, we don't really know what kind of types are given used
 * (some of the code under the hood doesn't have type annotations), so we decided
 * to handle it as we did in the past - without further type annotations.
*/
@Component
export default class VGeosearch extends Vue {
  @Prop({
    required: true
  })
    options: any

  mounted () {
    this.add()
  }

  beforeDestroy () {
    this.remove()
  }

  // @ts-ignore
  deferredMountedTo (parent) {
    // @ts-ignore
    const searchControl = new GeoSearchControl(this.options)
    parent.addControl(searchControl)
    // @ts-ignore
    searchControl.getContainer().onclick = (e) => { e.stopPropagation() }
  }

  remove () {
    // @ts-ignore
    if (this.markerCluster) {
      // @ts-ignore
      this.$parent.removeLayer(this.markerCluster)
    }
  }

  add () {
    // @ts-ignore
    if (this.$parent._isMounted) {
      // @ts-ignore
      this.deferredMountedTo(this.$parent.mapObject)
    }
  }
}
</script>
