<!--
SPDX-FileCopyrightText: 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <manufacturer-model-basic-data
      v-if="manufacturerModel"
      v-model="manufacturerModel"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapState } from 'vuex'

import { ManufacturermodelsState } from '@/store/manufacturermodels'
import ManufacturerModelBasicData from '@/components/manufacturerModels/ManufacturerModelBasicData.vue'

@Component({
  computed: {
    ...mapState('manufacturermodels', ['manufacturerModel'])
  },
  components: {
    ManufacturerModelBasicData
  }
})
export default class ManufacturerModelShowBasicPage extends Vue {
  manufacturerModel!: ManufacturermodelsState['manufacturerModel']
}
</script>
