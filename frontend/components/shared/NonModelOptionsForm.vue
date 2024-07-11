<!--
SPDX-FileCopyrightText: 2022 - 2023
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
import { Configuration } from '@/models/Configuration'
import { Site } from '@/models/Site'

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
  readonly entity!: Device | Platform | Configuration | Site

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
    return this.isPrivate
      ? 'PIDs are not available for private visibility'
      : 'Information about the entity including the full name and email of the owner is stored at PID-service outside the SMS'
  }

  get isPrivate (): boolean {
    if (this.entity instanceof Configuration || this.entity instanceof Site) {
      // There is no isPrivate for configurations nor sites.
      return false
    }
    return this.entity.isPrivate
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
