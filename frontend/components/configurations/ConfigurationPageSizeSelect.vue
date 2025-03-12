<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <page-size-select
    v-model="chosenPageSize"
    :items="pageSizes"
    label="Items per page"
    @input="$emit('input')"
  />
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'
import PageSizeSelect from '@/components/shared/PageSizeSelect.vue'
import { ConfigurationsState, PageSizesGetter, SetPageSizeAction } from '@/store/configurations'

@Component({
  components: { PageSizeSelect },
  computed: {
    ...mapState('configurations', ['pageSize']),
    ...mapGetters('configurations', ['pageSizes'])
  },
  methods: {
    ...mapActions('configurations', ['setPageSize'])
  }
})
export default class ConfigurationPageSizeSelect extends Vue {
  pageSize!: ConfigurationsState['pageSize']
  pageSizes!: PageSizesGetter
  setPageSize!: SetPageSizeAction

  get chosenPageSize (): number {
    return this.pageSize
  }

  set chosenPageSize (newVal: number) {
    const oldVal = this.pageSize
    if (oldVal !== newVal) {
      this.setPageSize(newVal)
    }
  }
}
</script>

<style scoped>

</style>
