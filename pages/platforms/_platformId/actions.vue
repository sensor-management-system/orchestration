<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
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
      <NuxtChild/>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions } from 'vuex'

@Component({
  methods:mapActions('platforms',['loadAllPlatformActions'])
})
export default class PlatformActionsPage extends Vue {
  async created(){
    await this.loadAllPlatformActions(this.platformId);
  }
  // async fetch () {
  //   this.showload(true)
  //   await this.fetchActions()
  //   this.showload(false)
  // }

  // async fetchActions (): Promise<void> {
  //   this.actions = []
  //   await Promise.all([
  //     this.fetchGenericActions(),
  //     this.fetchSoftwareUpdateActions(),
  //     this.fetchMountActions(),
  //     this.fetchUnmountActions()
  //   ])
  //   // sort the actions
  //   const comparator = new DateComparator()
  //   this.actions.sort((i: IActionCommonDetails, j: IActionCommonDetails): number => {
  //     if (isDateCompareable(i) && isDateCompareable(j)) {
  //       // multiply result with -1 to get descending order
  //       return comparator.compare(i, j) * -1
  //     }
  //     if (isDateCompareable(i)) {
  //       return -1
  //     }
  //     if (isDateCompareable(j)) {
  //       return 1
  //     }
  //     return 0
  //   })
  // }
  head () {
    return {
      titleTemplate: 'Actions - %s'
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }


  // get apiDispatcher () {
  //   return new PlatformActionApiDispatcher(this.$api)
  // }
}
</script>
