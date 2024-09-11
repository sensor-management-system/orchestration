<!--
SPDX-FileCopyrightText: 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div />
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

@Component({})
export default class MeasuredQuantityIdPage extends Vue {
  async created () {
    try {
      const deviceId = await this.$api.deviceProperties.getDeviceId(this.measuredquantityId)
      this.$router.push('/devices/' + deviceId + '/measuredquantities/' + this.measuredquantityId)
    } catch {
      this.$store.commit('snackbar/setError', 'Failed to lookup the measured quantity id.')
      this.$router.push('/')
    }
  }

  get measuredquantityId (): string {
    return this.$route.params.measuredquantityId
  }
}
</script>
