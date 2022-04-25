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
    <ProgressIndicator
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="editable"
        :disabled="isEditCustomFieldsPage || isNewCustomFieldsPage"
        color="primary"
        small
        @click="createField"
      >
        Add Custom Field
      </v-btn>
    </v-card-actions>
    <hint-card v-if="(customFields.length === 0) && !isLoading">
      There are no custom fields for this device.
    </hint-card>

    <div
      v-for="(field, index) in customFields"
      :key="'customfield-' + index"
    >
      <NuxtChild
        v-model="customFields[index]"
        @openDeleteDialog="showDeleteDialogFor"
      />
      <v-dialog v-model="showDeleteDialog[field.id]" max-width="290">
        <v-card>
          <v-card-title class="headline">
            Delete Field
          </v-card-title>
          <v-card-text>
            Do you really want to delete the field <em>{{ field.key }}</em>?
          </v-card-text>
          <v-card-actions>
            <v-btn
              text
              @click="hideDeleteDialogFor(field.id)"
            >
              No
            </v-btn>
            <v-spacer />
            <v-btn
              color="error"
              text
              @click="deleteAndCloseDialog(field)"
            >
              <v-icon left>
                mdi-delete
              </v-icon>
              Delete
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
    <div v-show="isNewCustomFieldsPage">
      <CustomFieldCardForm
        ref="newCustomFieldCardForm"
        v-model="newCustomField"
      >
        <template #actions>
          <v-btn
            v-if="editable"
            ref="cancelButton"
            text
            small
            nuxt
            @click="cancel()"
          >
            Cancel
          </v-btn>
          <v-btn
            v-if="editable"
            color="green"
            small
            :disabled="newCustomField._key === ''"
            @click="save()"
          >
            Apply
          </v-btn>
        </template>
      </CustomFieldCardForm>
    </div>
    <v-card-actions
      v-if="customFields.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="editable"
        :disabled="isEditCustomFieldsPage || isNewCustomFieldsPage"
        color="primary"
        small
        @click="createField"
      >
        Add Custom Field
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { CustomTextField } from '@/models/CustomTextField'

import { Device } from '@/models/Device'

import HintCard from '@/components/HintCard.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import CustomFieldCardForm from '@/components/CustomFieldCardForm.vue'

@Component({
  components: {
    HintCard,
    ProgressIndicator,
    CustomFieldCardForm
  }
})
export default class DeviceCustomFieldsPage extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Device

  // TODO: uncomment the next two lines and remove the third one after merging the permission management branch
  // @InjectReactive()
  //   editable!: boolean
  get editable (): boolean {
    return this.$auth.loggedIn
  }

  private customFields: CustomTextField[] = []
  private isLoading = false
  private isSaving = false
  private newCustomField = new CustomTextField()

  private showDeleteDialog: {[idx: string]: boolean} = {}

  created () {
    if (!this.editable && this.isEditCustomFieldsPage) {
      this.$router.replace('/devices/' + this.deviceId + '/customfields')
    }
  }

  async fetch (): Promise<void> {
    this.isLoading = true
    try {
      this.customFields = await this.$api.devices.findRelatedCustomFields(this.deviceId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch custom fields')
    } finally {
      this.isLoading = false
    }
  }

  head () {
    return {
      titleTemplate: 'Custom Fields - %s'
    }
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isEditCustomFieldsPage (): boolean {
    // eslint-disable-next-line no-useless-escape
    const editUrl = '^\/devices\/' + this.deviceId + '\/customfields\/([0-9]+)\/edit$'
    return !!this.$route.path.match(editUrl)
  }

  get isNewCustomFieldsPage (): boolean {
    return this.$route.path === '/devices/' + this.deviceId + '/customfields/new'
  }

  save (): void {
    this.isSaving = true
    this.$api.customfields.add(this.deviceId, this.newCustomField).then((newField: CustomTextField) => {
      this.isSaving = false
      this.$emit('input', newField)
      // we have to call fetch here because the new field is not present after page reload
      this.newCustomField = new CustomTextField()
      this.$fetch()
      this.$router.push('/devices/' + this.deviceId + '/customfields')
    }).catch(() => {
      this.isSaving = false
      this.$store.commit('snackbar/setError', 'Failed to save custom field')
    })
  }

  cancel (): void {
    this.newCustomField = new CustomTextField()
    this.$router.push('/devices/' + this.deviceId + '/customfields')
  }

  // TODO: focus on the key input field
  createField (): void {
    this.$vuetify.goTo(document.body.scrollHeight)
    this.$router.push('/devices/' + this.deviceId + '/customfields/new')
  }

  deleteAndCloseDialog (field: CustomTextField) {
    if (!field.id) {
      return
    }
    this.$api.customfields.deleteById(field.id).then(() => {
      const index: number = this.customFields.findIndex((f: CustomTextField) => f.id === field.id)
      if (index > -1) {
        this.customFields.splice(index, 1)
      }
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to delete custom field')
    })

    this.showDeleteDialog = {}
  }

  showDeleteDialogFor (id: string) {
    Vue.set(this.showDeleteDialog, id, true)
  }

  hideDeleteDialogFor (id: string) {
    Vue.set(this.showDeleteDialog, id, false)
  }
}
</script>
