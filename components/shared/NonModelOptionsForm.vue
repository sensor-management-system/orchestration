<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
- Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
  <v-form>
    <v-row>
      <v-col cols="12" md="9">
        <v-checkbox
          v-if="showCheckbox"
          :disabled="entity.isPrivate"
          :value="value.persistentIdentifierShouldBeCreated"
          label="Create a Persistent Identifier (PID)"
          :hint="hintText"
          persistent-hint
          @change="update('createPid', $event)"
        />
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'
import { Device } from '@/models/Device'
import { Platform } from '@/models/Platform'

export interface NonModelOptions {
    persistentIdentifierShouldBeCreated: boolean
}

@Component
export default class NonModelOptionsForm extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: NonModelOptions

  @Prop({
    required: true,
    type: Object
  })
  readonly entity!: Device | Platform

  @Watch('entity.isPrivate', { immediate: true })
  // @ts-ignore
  onValueChanged (val: boolean) {
    if (val) { this.update('createPid', false) }
  }

  get showCheckbox () {
    if (!process.env.pidBaseUrl) {
      return false
    }

    if (this.entity.persistentIdentifier) {
      return false
    }

    return true
  }

  get hintText (): string {
    return this.entity.isPrivate
      ? 'PIDs are not available for private visibility'
      : 'Information about the entity including the full name and email of the owner is stored at PID-service outside the SMS'
  }

  update (key: string, value: boolean) {
    const options = this.value

    switch (key) {
      case 'createPid':
        options.persistentIdentifierShouldBeCreated = value as boolean
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }
    this.$emit('input', options)
  }
}
</script>
