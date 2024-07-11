<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <NuxtChild />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { mapActions } from 'vuex'

import { LoadEpsgCodesAction, LoadElevationDataAction } from '@/store/vocabulary'
import {
  LoadDeviceMountActionsIncludingDeviceInformationAction,
  LoadLocationActionTimepointsAction
} from '@/store/configurations'
import { LoadAllContactsAction } from '@/store/contacts'
import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  methods: {
    ...mapActions('vocabulary', ['loadEpsgCodes', 'loadElevationData']),
    ...mapActions('contacts', ['loadAllContacts']),
    ...mapActions('configurations', ['loadLocationActionTimepoints', 'loadDeviceMountActionsIncludingDeviceInformation']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationLocations extends Vue {
  // vuex definition for typescript check
  loadEpsgCodes!: LoadEpsgCodesAction
  loadElevationData!: LoadElevationDataAction
  loadLocationActionTimepoints!: LoadLocationActionTimepointsAction
  loadDeviceMountActionsIncludingDeviceInformation!: LoadDeviceMountActionsIncludingDeviceInformationAction
  loadAllContacts!: LoadAllContactsAction
  setLoading!: SetLoadingAction

  async fetch () {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadEpsgCodes(),
        this.loadElevationData(),
        this.loadAllContacts(),
        this.loadLocationActionTimepoints(this.configurationId),
        this.loadDeviceMountActionsIncludingDeviceInformation(this.configurationId)
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch locations')
    } finally {
      this.setLoading(false)
    }
  }

  get configurationId () {
    return this.$route.params.configurationId
  }
}
</script>
