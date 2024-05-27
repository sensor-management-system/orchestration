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
    <v-btn
      small
      text
      nuxt
      :to="to"
    >
      cancel
    </v-btn>
    <v-btn
      color="accent"
      small
      :disabled="disabled"
      @click="$emit('save')"
    >
      {{ saveBtnText }}
    </v-btn>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { RawLocation } from 'vue-router'

@Component
export default class SaveAndCancelButtons extends Vue {
  @Prop({ required: true, type: [String, Object] }) to!: RawLocation
  @Prop({ required: true, type: String }) saveBtnText!: string
  @Prop({ default: false, type: Boolean }) disabled!: boolean
}
</script>

<style scoped>

</style>
