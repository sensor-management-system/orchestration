<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
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
  <div>
    <v-icon v-if="value" color="green">
      mdi-check
    </v-icon>
    <v-icon v-else color="red">
      mdi-close
    </v-icon>
    {{ label }}
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component to show an info text
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

/**
 * A class component to show an info text
 * @extends Vue
 */
@Component
// @ts-ignore
export default class PermissionInfo extends Vue {
  /**
   * a list of projects
   */
  @Prop({
    default: false,
    required: true,
    type: Boolean
  })
  // @ts-ignore
  readonly value!: boolean

  /**
   * a label for the permission info
   */
  @Prop({
    default: '',
    required: true,
    type: String
  })
  // @ts-ignore
  readonly label!: string
}
</script>
