<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
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
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        small
        text
        nuxt
        :to="'/devices/' + deviceId + '/actions'"
      >
        cancel
      </v-btn>
      <v-btn
        v-if="isLoggedIn"
        color="green"
        small
        @click="save"
      >
        apply
      </v-btn>
    </v-card-actions>
    <!-- just to be consistent with the new mask, we show the selected action type as an disabled v-select here -->
    <v-select
      :value="valueCopy.actionTypeName"
      :items="[valueCopy.actionTypeName]"
      :item-text="(x) => x"
      disabled
      label="Action Type"
    />
    <GenericDeviceActionForm
      ref="genericDeviceActionForm"
      v-model="valueCopy"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        small
        text
        nuxt
        :to="'/devices/' + deviceId + '/actions'"
      >
        cancel
      </v-btn>
      <v-btn
        v-if="isLoggedIn"
        color="green"
        small
        @click="save"
      >
        apply
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'nuxt-property-decorator'

import { GenericDeviceAction } from '@/models/GenericDeviceAction'

import GenericDeviceActionForm from '@/components/GenericDeviceActionForm.vue'

@Component({
  components: {
    GenericDeviceActionForm
  }
})
export default class DeviceActionEditPage extends Vue {
  private valueCopy: GenericDeviceAction = new GenericDeviceAction()

  @Prop({
    default: () => new GenericDeviceAction(),
    required: true,
    type: Object
  })
  readonly value!: GenericDeviceAction

  created () {
    if (this.value) {
      this.valueCopy = GenericDeviceAction.createFromObject(this.value)
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  save (): void {
    this.$api.genericDeviceActions.update(this.deviceId, this.valueCopy).then((action: GenericDeviceAction) => {
      this.$router.push('/devices/' + this.deviceId + '/actions', () => this.$emit('input', action))
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    })
  }

  @Watch('value', { immediate: true, deep: true })
  // @ts-ignore
  onValueChanged (val: GenericDeviceAction) {
    this.valueCopy = GenericDeviceAction.createFromObject(val)
  }
}
</script>
