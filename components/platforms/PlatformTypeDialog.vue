<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
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
      v-model="isSaving"
      :dark="true"
    />
    <v-dialog
      v-model="showDialog"
      max-width="600"
      persistent
      scrollable
    >
      <v-card>
        <v-card-title>Suggest new platform type</v-card-title>
        <v-card-text>
          <p>
            You can suggest a new platform type for the controlled vocabulary. This is submitted as a proposal.
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
                <v-text-field
                  v-model="newPlatformType.name"
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
                  v-model="newPlatformType.definition"
                  label="Definition"
                  rows="2"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="newPlatformType.provenance"
                  label="Provenance"
                />
              </v-col>
              <v-col>
                <v-text-field
                  v-model="newPlatformType.provenanceUri"
                  label="Provenance URI"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="newPlatformType.category"
                  label="Category"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-textarea
                  v-model="newPlatformType.note"
                  label="Note for the curator"
                  rows="2"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-select
                  v-model="newPlatformType.globalProvenanceId"
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
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { Rules } from '@/mixins/Rules'
import { PlatformType } from '@/models/PlatformType'
import { AddPlatformTypeAction, LoadGlobalProvenancesAction, VocabularyState } from '@/store/vocabulary'

@Component({
  computed: {
    ...mapState('vocabulary', ['platformtypes', 'globalProvenances'])
  },
  methods: {
    ...mapActions('vocabulary', ['addPlatformtype', 'loadGlobalProvenances'])
  },
  components: {
    ProgressIndicator
  }
})
export default class PlatformTypeDialog extends mixins(Rules) {
  private newPlatformType = new PlatformType()
  private isSaving: boolean = false
  private addPlatformtype!: AddPlatformTypeAction
  private loadGlobalProvenances!: LoadGlobalProvenancesAction
  private platformtypes!: VocabularyState['platformtypes']
  private globalProvenances!: VocabularyState['globalProvenances']

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

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (value: boolean) {
    this.$emit('input', value)
  }

  async fetchRelated () {
    try {
      await this.loadGlobalProvenances()
    } catch {
      this.$store.commit('snackbar/setError', 'Loading of global provenances failed')
    }
  }

  resetInputs () {
    this.newPlatformType = new PlatformType()
  }

  notInExistingNames (term: string| null): boolean | string {
    if (!term) {
      return true
    }
    if (this.platformtypes.find(pt => pt.name === term)) {
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
    this.isSaving = true
    const platformtype = PlatformType.createFromObject(this.newPlatformType)
    this.showDialog = false
    try {
      const result = await this.addPlatformtype({ platformtype })
      this.$emit('aftersubmit', result)
      this.$store.commit('snackbar/setSuccess', 'Your proposal has been successfully submitted. Your changes will be reviewed soon.')
    } catch (err) {
      this.$store.commit('snackbar/setError', 'Error on submitting the platform type')
    } finally {
      this.isSaving = false
      this.resetInputs()
    }
  }

  @Watch('value')
  async onOpenCloseToggle (newValue: boolean) {
    if (newValue) {
      // We open the dialog
      this.newPlatformType.name = this.initialTerm
      await this.fetchRelated()
    } else {
      this.resetInputs()
    }
  }
}
</script>
