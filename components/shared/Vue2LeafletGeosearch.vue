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

<script>
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { GeoSearchControl } from 'leaflet-geosearch'

/*
 * This component has been adapted from https://github.com/fega/vue2-leaflet-geosearch
 * under the MIT license
*/
@Component
export default class VGeosearch extends Vue {
  @Prop({
    required: true
  })
    options

  mounted () {
    this.add()
  }

  beforeDestroy () {
    this.remove()
  }

  deferredMountedTo (parent) {
    const searchControl = new GeoSearchControl(this.options)
    parent.addControl(searchControl)
    searchControl.getContainer().onclick = (e) => { e.stopPropagation() }
  }

  remove () {
    if (this.markerCluster) {
      this.$parent.removeLayer(this.markerCluster)
    }
  }

  add () {
    if (this.$parent._isMounted) {
      this.deferredMountedTo(this.$parent.mapObject)
    }
  }
}
</script>
