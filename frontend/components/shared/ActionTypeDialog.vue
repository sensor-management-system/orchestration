<!--
SPDX-FileCopyrightText: 2022 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-dialog
      v-model="showDialog"
      max-width="600"
      persistent
      scrollable
    >
      <v-card>
        <v-card-title>Suggest new action type</v-card-title>
        <v-card-text>
          <p>
            You can suggest a new action type for the controlled vocabulary. This is submitted as a proposal.
          </p>
          <p>
            A curator reviews your contribution before accepting it and including it in the full controlled vocabulary.
          </p>
          <p>
            In order to give the curator the opportunity to contact you, we will send your e-mail address with this request.
          </p>
          <v-form ref="suggestionForm" @submit.prevent>
            <v-row>
              <v-col>
                <v-select
                  v-model="suggestion.actionCategoryId"
                  :items="actionCategories"
                  label="Action category"
                  item-value="id"
                  clearable
                  required
                  class="required"
                  :rules="[rules.required]"
                  disabled
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="suggestion.name"
                  label="Term"
                  required
                  class="required"
                  :rules="[rules.required, notInExistingNames]"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-textarea
                  v-model="suggestion.definition"
                  label="Definition"
                  rows="2"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="suggestion.provenance"
                  label="Provenance"
                />
              </v-col>
              <v-col>
                <v-text-field
                  v-model="suggestion.provenanceUri"
                  label="Provenance URI"
                />
              </v-col>
            </v-row>
            <v-row class="mt-0">
              <v-col class="pt-0 pb-0">
                <provenance-hint />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="suggestion.category"
                  label="Category"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-textarea
                  v-model="suggestion.note"
                  label="Note for the curator"
                  rows="2"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-select
                  v-model="suggestion.globalProvenanceId"
                  :items="globalProvenances"
                  label="Global provenance"
                  item-value="id"
                  clearable
                />
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn
            text
            @click="showDialog = false"
          >
            Cancel
          </v-btn>
          <v-spacer />
          <v-btn
            color="primary"
            @click="submit"
          >
            Submit
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'
import { SetLoadingAction } from '@/store/progressindicator'
import ProvenanceHint from '@/components/shared/ProvenanceHint.vue'
import { Rules } from '@/mixins/Rules'
import { ActionType } from '@/models/ActionType'
import { AddActiontypeAction, LoadGlobalProvenancesAction, LoadActionCategoriesAction, VocabularyState } from '@/store/vocabulary'
import { ActionTypeApiFilterType, ACTION_TYPE_API_FILTER_DEVICE, ACTION_TYPE_API_FILTER_PLATFORM, ACTION_TYPE_API_FILTER_CONFIGURATION } from '@/services/cv/ActionTypeApi'

@Component({
  computed: {
    ...mapState('vocabulary', ['actionCategories', 'globalProvenances', 'platformGenericActionTypes', 'deviceGenericActionTypes', 'configurationGenericActionTypes'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadGlobalProvenances', 'loadActionCategories', 'addActiontype']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  components: {
    ProvenanceHint
  }
})
export default class ActionTypeDialog extends mixins(Rules) {
  private suggestion = new ActionType()
  private addActiontype!: AddActiontypeAction
  private loadGlobalProvenances!: LoadGlobalProvenancesAction
  private loadActionCategories!: LoadActionCategoriesAction
  private actionCategories!: VocabularyState['actionCategories']
  private platformGenericActionTypes!: VocabularyState['platformGenericActionTypes']
  private deviceGenericActionTypes!: VocabularyState['deviceGenericActionTypes']
  private configurationGenericActionTypes!: VocabularyState['configurationGenericActionTypes']
  private globalProvenances!: VocabularyState['globalProvenances']

  // vuex definition for typescript check
  setLoading!: SetLoadingAction

  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  @Prop({
    required: true,
    type: String
  })
  readonly initialActionTypeApiFilterType!: ActionTypeApiFilterType

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (value: boolean) {
    this.$emit('input', value)
  }

  async fetchRelated () {
    try {
      await Promise.all([this.loadGlobalProvenances(), this.loadActionCategories()])
    } catch {
      this.$store.commit('snackbar/setError', 'Loading of controlled vocabulary failed')
    }
  }

  resetInputs () {
    this.suggestion = new ActionType()
  }

  notInExistingNames (term: string| null): boolean | string {
    if (!term) {
      return true
    }
    if (this.specificActionTypes.find(x => x.name === term)) {
      return 'Term is already part of the controlled vocabulary'
    }
    return true
  }

  get specificActionTypes (): ActionType[] {
    const associatedActionCategory = this.actionCategories.find(x => x.id === this.suggestion.actionCategoryId)
    if (!associatedActionCategory) {
      return []
    }
    if (associatedActionCategory.name === ACTION_TYPE_API_FILTER_DEVICE) {
      return this.deviceGenericActionTypes
    }
    if (associatedActionCategory.name === ACTION_TYPE_API_FILTER_PLATFORM) {
      return this.platformGenericActionTypes
    }
    if (associatedActionCategory.name === ACTION_TYPE_API_FILTER_CONFIGURATION) {
      return this.configurationGenericActionTypes
    }
    return []
  }

  validateForm (): boolean {
    return (this.$refs.suggestionForm as Vue & { validate: () => boolean }).validate()
  }

  async submit () {
    if (!this.validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors before submitting')
      return
    }
    this.setLoading(true)
    // We copy the values as we reset the data when we close the dialog
    const suggestion = ActionType.createFromObject(this.suggestion)
    const actionCategoryTerm = this.initialActionTypeApiFilterType
    this.showDialog = false
    try {
      const result = await this.addActiontype({ actiontype: suggestion, actionCategoryTerm })
      this.$emit('aftersubmit', result)
      this.$store.commit('snackbar/setSuccess', 'Your proposal has been successfully submitted. Your changes will be reviewed soon.')
    } catch (err) {
      this.$store.commit('snackbar/setError', 'Error on submitting the action type')
    } finally {
      this.setLoading(false)
      this.resetInputs()
    }
  }

  @Watch('value')
  async onOpenCloseToggle (newValue: boolean) {
    if (newValue) {
      // We open the dialog
      await this.fetchRelated()
      const actionCategoryId = this.actionCategories.find(x => x.name === this.initialActionTypeApiFilterType)?.id || null
      this.suggestion.actionCategoryId = actionCategoryId
    } else {
      this.resetInputs()
    }
  }
}
</script>
