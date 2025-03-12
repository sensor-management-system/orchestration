<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <FoundEntries v-model="totalCount" entity-name="platform" />
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapState } from 'vuex'
import FoundEntries from '@/components/shared/FoundEntries.vue'
import { PlatformsState } from '@/store/platforms'

@Component({
  components: { FoundEntries },
  computed: {
    ...mapState('platforms', ['totalCount'])
  }
})
export default class PlatformFoundEntries extends Vue {
  totalCount!: PlatformsState['totalCount']
}
</script>

<style scoped>

</style>
