<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-pagination
    v-model="page"
    :disabled="isLoading"
    :length="totalPages"
    :total-visible="7"
    @input="$emit('input')"
  />
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'
import { LoadingSpinnerState } from '@/store/progressindicator'
import { ConfigurationsState, SetPageNumberAction } from '@/store/configurations'

@Component({
  computed: {
    ...mapState('configurations', ['pageNumber', 'totalPages']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('configurations', ['setPageNumber'])
  }
})
export default class ConfigurationPagination extends Vue {
  isLoading!: LoadingSpinnerState['isLoading']
  totalPages!: ConfigurationsState['totalPages']
  pageNumber!: ConfigurationsState['pageNumber']
  setPageNumber!: SetPageNumberAction

  get page () {
    return this.pageNumber
  }

  set page (newVal) {
    this.setPage(newVal)
  }

  public setPage (newVal: number) {
    // extra method to make this external available
    this.setPageNumber(newVal)
  }
}
</script>

<style scoped>

</style>
