<!--
SPDX-FileCopyrightText: 2020 - 2022
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
import { PermissionsState } from '@/store/permissions'

@Component({
  components: {
    MountActionDetailsForm,
    ExtendedItemName
  },
  filters: { dateToDateTimeStringHHMM },
  computed: {
    ...mapState('contacts', ['contacts']),
    ...mapState('permissions', ['userInfo'])
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
  userInfo!: PermissionsState['userInfo']

  get currentUserContactId (): string | null {
    if (this.userInfo && this.userInfo.contactId) {
      return this.userInfo.contactId
    }
    return null
  }

  get currentUserAsContact (): Contact | null {
    if (this.currentUserContactId) {
      const userIndex = this.contacts.findIndex(c => c.id === this.currentUserContactId)
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
