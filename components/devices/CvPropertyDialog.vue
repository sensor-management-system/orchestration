<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022 - 2023
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
    <v-dialog
      v-model="showDialog"
      max-width="600"
      persistent
      scrollable
    >
      <v-card>
        <v-card-title>Suggest new measured quantity</v-card-title>
        <v-card-text>
          <p>
            You can suggest a new measured quantity for the controlled vocabulary. This is submitted as a proposal.
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
                  v-model="suggestion.samplingMediaId"
                  :items="samplingMedia"
                  label="Sampling medium"
                  item-value="id"
                  clearable
                  required
                  class="required"
                  :rules="[rules.required]"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-select
                  v-model="suggestion.aggregationTypeId"
                  :items="aggregationtypes"
                  label="Default aggregation type"
                  item-value="id"
                  clearable
                  required
                  class="required"
                  :rules="[rules.required]"
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
import { Property } from '@/models/Property'
import { AddPropertyAction, LoadAggregationtypesAction, LoadGlobalProvenancesAction, VocabularyState } from '@/store/vocabulary'

@Component({
  computed: {
    ...mapState('vocabulary', ['globalProvenances', 'samplingMedia', 'properties', 'aggregationtypes'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadGlobalProvenances', 'loadAggregationtypes', 'addProperty']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  components: {
    ProvenanceHint
  }
})
export default class CvPropertyDialog extends mixins(Rules) {
  private suggestion = new Property()
  private addProperty!: AddPropertyAction
  private loadGlobalProvenances!: LoadGlobalProvenancesAction
  private loadAggregationtypes!: LoadAggregationtypesAction
  private samplingMedia!: VocabularyState['samplingMedia']
  private properties!: VocabularyState['properties']
  private globalProvenances!: VocabularyState['globalProvenances']
  private aggregationtypes!: VocabularyState['aggregationtypes']

  // vuex definition for typescript check
  setLoading!: SetLoadingAction

  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  @Prop({
    required: false,
    type: String,
    default: ''
  })
  readonly initialTerm!: string

  @Prop({
    required: false,
    type: String,
    default: null
  })
  readonly initialSamplingMediaId!: string | null

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (value: boolean) {
    this.$emit('input', value)
  }

  async fetchRelated () {
    try {
      await Promise.all([this.loadGlobalProvenances(), this.loadAggregationtypes()])
    } catch {
      this.$store.commit('snackbar/setError', 'Loading of cv values failed')
    }
  }

  resetInputs () {
    this.suggestion = new Property()
  }

  notInExistingNames (term: string| null): boolean | string {
    if (!term) {
      return true
    }
    if (this.properties.find(x => x.name === term)) {
      return 'Term is already part of the controlled vocabulary'
    }
    return true
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
    const property = Property.createFromObject(this.suggestion)
    this.showDialog = false
    try {
      const result = await this.addProperty({ property })
      this.$emit('aftersubmit', result)
      this.$store.commit('snackbar/setSuccess', 'Your proposal has been successfully submitted. Your changes will be reviewed soon.')
    } catch (err) {
      this.$store.commit('snackbar/setError', 'Error on submitting the property')
    } finally {
      this.setLoading(false)
      this.resetInputs()
    }
  }

  @Watch('value')
  async onOpenCloseToggle (newValue: boolean) {
    if (newValue) {
      // We open the dialog
      this.suggestion.name = this.initialTerm
      this.suggestion.samplingMediaId = this.initialSamplingMediaId
      await this.fetchRelated()
    } else {
      this.resetInputs()
    }
  }
}
</script>
