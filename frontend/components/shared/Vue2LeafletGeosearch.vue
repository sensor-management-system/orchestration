<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
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
