<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
          >
            <template #append-outer>
              <v-tooltip
                v-if="softwareType && softwareType.definition"
                right
              >
                <template #activator="{ on, attrs }">
                  <v-icon
                    color="primary"
                    small
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-help-circle-outline
                  </v-icon>
                </template>
                <span>{{ softwareType.definition }}</span>
              </v-tooltip>
              <a v-if="actionCopy.softwareTypeUrl" target="_blank" :href="actionCopy.softwareTypeUrl" style="line-height: 2;">
                <v-icon small>
                  mdi-open-in-new
                </v-icon>
              </a>
            </template>
            <template #item="data">
              <template v-if="(typeof data.item) !== 'object'">
                <v-list-item-content>{{ data.item }}</v-list-item-content>
              </template>
              <template v-else>
                <v-list-item-content>
                  <v-list-item-title>
                    {{ data.item.name }}
                    <v-tooltip
                      v-if="data.item.definition"
                      bottom
                    >
                      <template #activator="{ on, attrs }">
                        <v-icon
                          color="primary"
                          small
                          v-bind="attrs"
                          v-on="on"
                        >
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>{{ data.item.definition }}</span>
                    </v-tooltip>
                  </v-list-item-title>
                </v-list-item-content>
              </template>
            </template>
          </v-select>
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
import { mapActions, mapState } from 'vuex'
import { DateTime } from 'luxon'

import { Attachment } from '@/models/Attachment'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { SoftwareType } from '@/models/SoftwareType'
import { ActionCommonDetails } from '@/models/ActionCommonDetails'

import { protocolsInUrl } from '@/utils/urlHelpers'

import CommonActionForm from '@/components/actions/CommonActionForm.vue'
import DateTimePicker from '@/components/DateTimePicker.vue'
import { LoadSoftwareTypesAction, VocabularyState } from '@/store/vocabulary'

/**
 * A class component for a form for Software update actions
 * @extends Vue
 */
@Component({
  components: {
    CommonActionForm,
    DateTimePicker
  },
  methods: {
    ...mapActions('vocabulary', ['loadSoftwareTypes'])
  },
  computed: {
    ...mapState('vocabulary', ['softwareTypes'])
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

  private softwareTypes!: VocabularyState['softwareTypes']
  loadSoftwareTypes!: LoadSoftwareTypesAction

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
    await this.loadSoftwareTypes()
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

  get softwareType (): SoftwareType | undefined {
    let aSoftwareType: SoftwareType | undefined
    if (this.actionCopy && this.actionCopy.softwareTypeUrl) {
      aSoftwareType = this.softwareTypes.find(i => i.uri === this.actionCopy.softwareTypeUrl)
    }
    return aSoftwareType
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
