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
    <NuxtChild
      v-if="editable && isEditModeForField"
      v-model="field"
    />
    <CustomFieldCard
      v-else
      v-model="field"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import CustomFieldCard from '@/components/CustomFieldCard.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { CustomTextField } from '@/models/CustomTextField'

@Component({
  components: {
    CustomFieldCard,
    ProgressIndicator
  }
})
export default class DeviceCustomFieldsIdPage extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: CustomTextField

  // TODO: uncomment the next two lines and remove the third one after merging the permission management branch
  // @InjectReactive()
  //   editable!: boolean
  get editable () {
    return this.$auth.loggedIn
  }

  created () {
    if (!this.editable) {
      this.$router.replace('/devices/' + this.deviceId + '/customfields')
    }
  }

  get field (): CustomTextField {
    return this.value
  }

  set field (value: CustomTextField) {
    this.$emit('input', value)
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isEditModeForField () {
    return this.$route.path === '/devices/' + this.deviceId + '/customfields/' + this.value.id + '/edit'
  }
}
</script>
