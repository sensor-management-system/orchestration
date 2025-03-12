<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <FoundEntries v-model="totalCount" entity-name="device" />
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapState } from 'vuex'
import FoundEntries from '@/components/shared/FoundEntries.vue'
import { DevicesState } from '@/store/devices'

@Component({
  components: { FoundEntries },
  computed: {
    ...mapState('devices', ['totalCount'])
  }
})
export default class DeviceFoundEntries extends Vue {
  totalCount!: DevicesState['totalCount']
}
</script>

<style scoped>

</style>
