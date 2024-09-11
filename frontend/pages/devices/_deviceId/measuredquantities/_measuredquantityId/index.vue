<!--
SPDX-FileCopyrightText: 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <!-- A page just for redirection. -->
  <div />
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

@Component({})
export default class DevicePropertyIdPage extends Vue {
  created () {
    this.$router.push('/devices/' + this.deviceId + '/measuredquantities?focus=' + this.measuredquantityId)
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get measuredquantityId (): string {
    return this.$route.params.measuredquantityId
  }
}
</script>
