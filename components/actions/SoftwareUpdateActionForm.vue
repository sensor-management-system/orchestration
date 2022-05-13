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
    <v-row>
      <v-col cols="12" md="6">
        <v-form
          ref="datesForm"
          v-model="datesAreValid"
          @submit.prevent
        >
          <DateTimePicker
            :value="actionCopy.updateDate"
            label="Update date"
            :required="true"
            :rules="[rules.dateNotNull]"
            @input="setUpdateDateAndValidate"
          />
        </v-form>
      </v-col>
      <v-col cols="12" md="6">
        <v-form
          ref="softwareTypeForm"
          @submit.prevent
        >
          <v-select
            :value="actionCopy.softwareTypeUrl"
            :items="softwareTypes"
            clearable
            :item-text="(x) => x.name"
            :item-value="(x) => x.uri"
            label="Software type"
            class="required"
            :rules="[rules.softwareTypeNotNull]"
            @input="setSoftwareType"
          />
        </v-form>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          :value="actionCopy.version"
          label="Version"
          placeholder="1.2.3"
          @input="setVersion"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-form
          ref="repositoryUrlForm"
          @submit.prevent
        >
          <v-text-field
            :value="actionCopy.repositoryUrl"
            label="Repository URL"
            placeholder="https://github.com/"
            :rules="[rules.isUrl]"
            @input="setRepositoryUrl"
          />
        </v-form>
      </v-col>
    </v-row>
    <CommonActionForm
      ref="commonForm"
      :value="actionCopy"
      :attachments="attachments"
      :rules="[rules.contactNotNull]"
      :current-user-mail="currentUserMail"
      @input="updateCommonFields"
    />
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component for a Software Update Action form
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'

import { Attachment } from '@/models/Attachment'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { SoftwareType } from '@/models/SoftwareType'
import { ActionCommonDetails } from '@/models/ActionCommonDetails'

import { protocolsInUrl } from '@/utils/urlHelpers'

import CommonActionForm from '@/components/actions/CommonActionForm.vue'
import DateTimePicker from '@/components/DateTimePicker.vue'

/**
 * A class component for a form for Software update actions
 * @extends Vue
 */
@Component({
  components: {
    CommonActionForm,
    DateTimePicker
  }
})
// @ts-ignore
export default class SoftwareUpdateActionForm extends Vue {
  private actionCopy: SoftwareUpdateAction = new SoftwareUpdateAction()
  private datesAreValid: boolean = true
  private rules: Object = {
    dateNotNull: this.mustBeProvided('Update date'),
    contactNotNull: this.mustBeProvided('Contact'),
    softwareTypeNotNull: this.mustBeProvided('Software type'),
    isUrl: this.isUrl
  }

  private softwareTypes: SoftwareType[] = []

  /**
   * a SoftwareUpdateAction
   */
  @Prop({
    default: () => new SoftwareUpdateAction(),
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly value!: SoftwareUpdateAction

  /**
   * a list of available attachments
   */
  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  // @ts-ignore
  readonly attachments!: Attachment[]

  @Prop({
    type: String
  })
  // @ts-ignore
  readonly currentUserMail: string | null

  async fetch (): Promise<any> {
    await this.fetchSoftwareTypes()
  }

  async fetchSoftwareTypes (): Promise<any> {
    this.softwareTypes = await this.$api.softwareTypes.findAllPaginated()
  }

  created () {
    // create a copy of the original value on which all operations will be applied
    this.createActionCopy(this.value)
  }

  /**
   * sets the update date and validates
   *
   * @param {DateTime | null} aDate - the update date
   */
  setUpdateDateAndValidate (aDate: DateTime | null) {
    this.actionCopy.updateDate = aDate
    this.checkValidationOfDates()
    this.$emit('input', this.actionCopy)
  }

  setSoftwareType (anUri: string | null) {
    let aSoftwareType: SoftwareType | undefined
    if (anUri) {
      aSoftwareType = this.softwareTypes.find(i => i.uri === anUri)
    }
    this.actionCopy.softwareTypeUrl = aSoftwareType?.uri || ''
    this.actionCopy.softwareTypeName = aSoftwareType?.name || ''
    this.$emit('input', this.actionCopy)
  }

  setVersion (version: string) {
    this.actionCopy.version = version
    this.$emit('input', this.actionCopy)
  }

  setRepositoryUrl (repositoryUrl: string) {
    this.actionCopy.repositoryUrl = repositoryUrl
    this.$emit('input', this.actionCopy)
  }

  updateCommonFields (action: ActionCommonDetails) {
    this.actionCopy.description = action.description
    this.actionCopy.contact = action.contact
    this.actionCopy.attachments = action.attachments.map((a: Attachment) => Attachment.createFromObject(a))
    this.$emit('input', this.actionCopy)
  }

  /**
   * validates the form based on its rules
   *
   */
  checkValidationOfDates () {
    return (this.$refs.datesForm as Vue & { validate: () => boolean }).validate()
  }

  /**
   * a rule to check that an field is non-empty
   *
   * @param {string} fieldname - the (human readable) label of the field
   * @return {(v: any) => boolean | string} a function that checks whether the field is valid or an error message
   */
  mustBeProvided (fieldname: string): (v: any) => boolean | string {
    const innerFunc: (v: any) => boolean | string = function (v: any) {
      if (v == null || v === '') {
        return fieldname + ' must be provided'
      }
      return true
    }
    return innerFunc
  }

  /**
   * checks whether the link is an valid URL or not
   *
   * to be honest, it just checks whether the string starts with http(s):// or similar
   *
   * @param {string} link - the link to validate
   * @returns {boolean | string} true when valid, otherwise an error message
   */
  isUrl (link: string): boolean | string {
    if (!protocolsInUrl(['http', 'https', 'ftp', 'ftps', 'sftp', 'ssh', 'dav', 'davs'], link)) {
      return 'The link is not a valid URL.'
    }
    return true
  }

  /**
   * checks if the form is valid
   *
   */
  isValid (): boolean {
    return this.checkValidationOfDates() &&
      (this.$refs.commonForm as Vue & { isValid: () => boolean }).isValid() &&
      (this.$refs.softwareTypeForm as Vue & { validate: () => boolean }).validate() &&
      (this.$refs.repositoryUrlForm as Vue & { validate: () => boolean }).validate()
  }

  createActionCopy (action: SoftwareUpdateAction): void {
    this.actionCopy = SoftwareUpdateAction.createFromObject(action)
  }

  @Watch('value', { immediate: true, deep: true })
  // @ts-ignore
  onValueChanged (val: SoftwareUpdateAction) {
    this.createActionCopy(val)
  }
}
</script>
<style lang="scss">
@import '@/assets/styles/_forms.scss';
</style>
