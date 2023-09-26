<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
    <v-card v-for="(entityMountInformation, i) in value" :key="`${prefix}-${i}`" class="mb-6">
      <v-card-text>
        <div>Mounting info</div>
        <div class="text-h6 text--primary">
          <extended-item-name
            :value="entityMountInformation.entity"
            :shorten="false"
          />
        </div>
        <div>{{ dateRangeString }}</div>
      </v-card-text>
      <mount-action-details-form
        ref="mountActionDetailsForm"
        v-model="entityMountInformation.mountInfo"
        :readonly="false"
        :contacts="contacts"
        :with-unmount="selectedEndDate !== null"
        :with-dates="false"
        :parent-offsets="parentOffsets"
        @input="update"
      />
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, InjectReactive, Prop } from 'nuxt-property-decorator'
import { mapState } from 'vuex'

import { DateTime } from 'luxon'

import { ContactsState } from '@/store/contacts'

import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { Platform } from '@/models/Platform'

import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'
import { IOffsets, MountActionInformationDTO } from '@/utils/configurationInterfaces'

import MountActionDetailsForm from '@/components/configurations/MountActionDetailsForm.vue'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'

@Component({
  components: {
    MountActionDetailsForm,
    ExtendedItemName
  },
  filters: { dateToDateTimeStringHHMM },
  computed: {
    ...mapState('contacts', ['contacts'])
  }
})
export default class MountWizardMountForm extends Vue {
  @Prop({
    required: true,
    type: Array
  })
  readonly value!: { entity: Device | Platform, mountInfo: MountActionInformationDTO }[]

  @Prop({
    required: true,
    type: String
  })
  readonly prefix!: String

  @Prop({
    default: (): IOffsets => ({ offsetX: 0, offsetY: 0, offsetZ: 0 }),
    required: false,
    type: Object
  })
  readonly parentOffsets!: IOffsets

  @InjectReactive() selectedDate!: DateTime
  @InjectReactive() selectedEndDate!: DateTime | null

  contacts!: ContactsState['contacts']

  get currentUserMail (): string | null {
    if (this.$auth.user && this.$auth.user.email) {
      return this.$auth.user.email as string
    }
    return null
  }

  get currentUserAsContact (): Contact | null {
    if (this.currentUserMail) {
      const userIndex = this.contacts.findIndex(c => c.email === this.currentUserMail)
      if (userIndex > -1) {
        return this.contacts[userIndex]
      }
    }
    return null
  }

  get dateRangeString (): string {
    const start = `From ${dateToDateTimeStringHHMM(this.selectedDate)}`
    const end = (this.selectedEndDate === null) ? ' with open end' : ` until ${dateToDateTimeStringHHMM(this.selectedEndDate)}`
    return start + end
  }

  validateForm (): boolean {
    if (this.$refs.mountActionDetailsForm) {
      return Object.values(this.$refs.mountActionDetailsForm).every(
        form => (form as Vue & { validateForm: () => boolean }).validateForm()
      )
    } else {
      return true
    }
  }

  update () {
    this.$emit('input', this.value)
  }
}
</script>

<style scoped>

</style>
