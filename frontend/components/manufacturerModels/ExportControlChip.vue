<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2024
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

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
  <v-chip
    v-if="text && color"
    :color="color"
    text-color="white"
    small
    class="mr-1 mb-1"
  >
    {{ text }}
  </v-chip>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

interface ChipSetting {
  value: boolean | null
  text: string
  color: string
}

@Component
export default class ExportControlChip extends Vue {
  @Prop({
    default: null,
    type: Boolean
  })
  readonly value!: boolean | null

  get settings (): ChipSetting[] {
    return [
      {
        value: null,
        text: 'Dual use unknown',
        color: 'red'
      },
      {
        value: true,
        text: 'Dual use',
        color: 'orange'
      },
      {
        value: false,
        text: 'No dual use',
        color: 'grey'
      }
    ]
  }

  get color (): string | null {
    for (const entry of this.settings) {
      if (entry.value === this.value) {
        return entry.color
      }
    }
    return null
  }

  get text (): string | null {
    for (const entry of this.settings) {
      if (entry.value === this.value) {
        return entry.text
      }
    }
    return null
  }
}
</script>
