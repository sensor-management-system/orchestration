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
        <v-card-title>Suggest new unit</v-card-title>
        <v-card-text>
          <p>
            You can suggest a new unit for the controlled vocabulary. This is submitted as a proposal.
          </p>
          <p>
            A curator reviews your contribution before accepting it and including it in the full controlled vocabulary.
          </p>
          <p>
            In order to give the curator the opportunity to contact you, we will send your e-mail address with this request.
          </p>
          <!-- First we have a form to select if we want to add an existing
               unit or not.
          -->
          <v-form ref="unitSelectionTypeForm" @submit.prevent>
            <v-row>
              <v-col>
                <v-select
                  v-model="useExistingUnit"
                  :items="existingOrNewUnit"
                  :item-text="(x) => x.text"
                  :item-value="(x) => x.value"
                />
              </v-col>
            </v-row>
          </v-form>
          <!-- If the user wants to use an existing unit, then she/he
               should select it.
          -->
          <v-form v-if="useExistingUnit" ref="unitSelectionForm" @submit.prevent>
            <v-row>
              <v-col>
                <v-select
                  v-model="measuredQuantityUnit.unitId"
                  :items="units"
                  label="Unit"
                  item-value="id"
                  required
                  class="required"
                  :rules="[rules.required, notInExistingMeasuredQuantityBindings]"
                />
              </v-col>
            </v-row>
          </v-form>
          <!-- Else we show the input fields to add a new unit overall.
          -->
          <v-form v-else ref="unitForm" @submit.prevent>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="unit.name"
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
                  v-model="unit.definition"
                  label="Definition"
                  rows="2"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="unit.provenance"
                  label="Provenance"
                />
              </v-col>
              <v-col>
                <v-text-field
                  v-model="unit.provenanceUri"
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
                  v-model="unit.category"
                  label="Category"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-textarea
                  v-model="unit.note"
                  label="Note for the curator"
                  rows="2"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-select
                  v-model="unit.globalProvenanceId"
                  :items="globalProvenances"
                  label="Global provenance"
                  item-value="id"
                  clearable
                />
              </v-col>
            </v-row>
          </v-form>
          <!-- And last we show the default form for default limits.
          -->
          <v-form ref="measuredQuantityUnitForm" @submit.prevent>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="measuredQuantityUnit.defaultLimitMin"
                  label="Default limit min"
                  type="number"
                  step="any"
                  @wheel.prevent
                />
              </v-col>
              <v-col>
                <v-text-field
                  v-model="measuredQuantityUnit.defaultLimitMax"
                  label="Default limit max"
                  type="number"
                  step="any"
                  @wheel.prevent
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
import ProvenanceHint from '@/components/shared/ProvenanceHint.vue'
import { Rules } from '@/mixins/Rules'
import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'
import { Unit } from '@/models/Unit'
import { AddUnitAction, AddMeasuredQuantityUnitAction, LoadGlobalProvenancesAction, VocabularyState } from '@/store/vocabulary'

@Component({
  computed: {
    ...mapState('vocabulary', ['units', 'globalProvenances', 'measuredQuantityUnits'])
  },
  methods: {
    ...mapActions('vocabulary', ['addUnit', 'addMeasuredQuantityUnit', 'loadGlobalProvenances'])
  },
  components: {
    ProgressIndicator,
    ProvenanceHint
  }
})
export default class MeasuredQuantityUnitDialog extends mixins(Rules) {
  private unit = new Unit()
  private measuredQuantityUnit = new MeasuredQuantityUnit()
  private isSaving: boolean = false
  private addUnit!: AddUnitAction
  private addMeasuredQuantityUnit!: AddMeasuredQuantityUnitAction
  private loadGlobalProvenances!: LoadGlobalProvenancesAction
  private units!: VocabularyState['units']
  private globalProvenances!: VocabularyState['globalProvenances']
  private measuredQuantityUnits !: VocabularyState['measuredQuantityUnits']
  private useExistingUnit: boolean = true
  private existingOrNewUnit = [
    { text: 'Existing unit', value: true },
    { text: 'New unit', value: false }
  ]

  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  @Prop({
    required: false,
    type: String,
    default: null
  })
  readonly initialMeasuredQuantityId!: string | null

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
    this.unit = new Unit()
    this.measuredQuantityUnit = new MeasuredQuantityUnit()
    this.useExistingUnit = true
  }

  notInExistingNames (term: string| null): boolean | string {
    if (!term) {
      return true
    }
    if (this.units.find(x => x.name === term)) {
      return 'Term is already part of the controlled vocabulary'
    }
    return true
  }

  notInExistingMeasuredQuantityBindings (unitId: string | null): boolean | string {
    if (!unitId) {
      return true
    }
    const existing = this.measuredQuantityUnits.find(x => x.unitId === unitId && x.measuredQuantityId === this.measuredQuantityUnit.measuredQuantityId)
    if (existing) {
      return 'Unit selection already possible for the measured quantity'
    }
    return true
  }

  validateForms (): boolean {
    const formsToValidate = ['unitSelectionTypeForm']

    if (this.useExistingUnit) {
      formsToValidate.push('unitSelectionForm')
    } else {
      formsToValidate.push('unitForm')
    }
    formsToValidate.push('measuredQuantityUnitForm')

    let result = true
    for (const form of formsToValidate) {
      result = result && (this.$refs[form] as Vue & { validate: () => boolean}).validate()
    }
    return result
  }

  async submit () {
    if (!this.validateForms()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors before submitting')
      return
    }
    this.isSaving = true
    const unit = Unit.createFromObject(this.unit)
    const measuredQuantityUnit = MeasuredQuantityUnit.createFromObject(this.measuredQuantityUnit)
    this.showDialog = false
    try {
      let selectedUnit: Unit | null = null
      if (!this.useExistingUnit) {
        selectedUnit = await this.addUnit({ unit })
      } else {
        selectedUnit = this.units.find(x => x.id === measuredQuantityUnit.unitId) || null
      }
      if (selectedUnit) {
        measuredQuantityUnit.unitId = selectedUnit.id
        measuredQuantityUnit.name = selectedUnit.name
        measuredQuantityUnit.definition = selectedUnit.definition
      }
      const result = await this.addMeasuredQuantityUnit({
        measuredQuantityUnit
      })
      this.$emit('aftersubmit', result)
      this.$store.commit('snackbar/setSuccess', 'Your proposal has been successfully submitted. Your changes will be reviewed soon.')
    } catch (err) {
      this.$store.commit('snackbar/setError', 'Error on submitting the unit')
    } finally {
      this.isSaving = false
      this.resetInputs()
    }
  }

  @Watch('value')
  async onOpenCloseToggle (newValue: boolean) {
    if (newValue) {
      // We open the dialog
      if (this.initialMeasuredQuantityId) {
        this.measuredQuantityUnit.measuredQuantityId = this.initialMeasuredQuantityId
      }
      await this.fetchRelated()
    } else {
      this.resetInputs()
    }
  }
}
</script>
