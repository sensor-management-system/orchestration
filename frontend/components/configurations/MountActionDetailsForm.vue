<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022 - 2024
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
  <span>
    <v-form
      v-if="value"
      ref="mountForm"
      @submit.prevent
    >
      <v-container>
        <mount-action-date-form
          v-if="withDates"
          ref="dateForm"
          v-model="mountActionDateDTO"
          :begin-date-rules="beginDateRules"
          :end-date-rules="endDateRules"
          :end-required="unmountRequired"
          @input="update"
        />
        <v-row class="pb-0">
          <v-col
            md="12"
            lg="4"
            xl="3"
          >
            <v-text-field
              v-model.number="mountActionInformationDTO.offsetX"
              data-role="textfield-offset-x"
              label="Offset (x)"
              type="number"
              step="any"
              :disabled="readonly"
              required
              :rules="[rules.numeric, rules.required]"
              class="required m-annotated"
              @wheel.prevent
              @input="update"
            />
          </v-col>
          <v-col
            md="12"
            lg="4"
            xl="3"
          >
            <v-text-field
              v-model.number="mountActionInformationDTO.offsetY"
              data-role="textfield-offset-y"
              label="Offset (y)"
              type="number"
              step="any"
              :disabled="readonly"
              required
              :rules="[rules.numeric, rules.required]"
              class="required m-annotated"
              @wheel.prevent
              @input="update"
            />
          </v-col>
          <v-col
            md="12"
            lg="4"
            xl="3"
          >
            <v-text-field
              v-model.number="mountActionInformationDTO.offsetZ"
              data-role="textfield-offset-z"
              label="Offset (z)"
              type="number"
              step="any"
              :disabled="readonly"
              required
              :rules="[rules.numeric, rules.required]"
              class="required m-annotated"
              @wheel.prevent
              @input="update"
            />
          </v-col>
        </v-row>
        <v-row no-gutters>
          <v-col class="text-caption text--secondary">Offsets are relative to parent platform/root</v-col>
        </v-row>
        <v-row>
          <v-col md="12" lg="4" xl="3">
            <v-row
              no-gutters
            >
              <v-col
                cols="12"
                md="6"
                lg="12"
                class="text-caption text--secondary"
              >
                Absolute offset (x):
                <v-tooltip
                  bottom
                >
                  <template #activator="{ on, attrs }">
                    <v-icon
                      small
                      v-bind="attrs"
                      v-on="on"
                    >
                      mdi-help-circle
                    </v-icon>
                  </template>
                  The offsets of the node are included.
                </v-tooltip>
              </v-col>
              <v-col
                cols="12"
                md="6"
                lg="12"
              >
                {{ absoluteOffsets.offsetX }} m
              </v-col>
            </v-row>
          </v-col>
          <v-col md="12" lg="4" xl="3">
            <v-row
              no-gutters
            >
              <v-col
                cols="12"
                md="6"
                lg="12"
                class="text-caption text--secondary"
              >
                Absolute offset (y):
              </v-col>
              <v-col
                cols="12"
                md="6"
                lg="12"
              >
                {{ absoluteOffsets.offsetY }} m
              </v-col>
            </v-row>
          </v-col>
          <v-col md="12" lg="4" xl="3">
            <v-row
              no-gutters
            >
              <v-col
                cols="12"
                md="6"
                lg="12"
                class="text-caption text--secondary"
              >
                Absolute offset (z):
              </v-col>
              <v-col
                cols="12"
                md="6"
                lg="12"
              >
                {{ absoluteOffsets.offsetZ }} m
              </v-col>
            </v-row>
          </v-col>
        </v-row>
        <v-row class="pb-0">
          <v-col cols="12" md="4">
            <v-text-field
              v-model.number="mountActionInformationDTO.x"
              label="Coordinate (x)"
              type="number"
              step="any"
              clearable
              @wheel.prevent
              @change="update"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              v-model.number="mountActionInformationDTO.y"
              label="Coordinate (y)"
              type="number"
              step="any"
              clearable
              @wheel.prevent
              @change="update"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="mountActionInformationDTO.epsgCode"
              :item-value="(x) => x.code"
              :item-text="(x) => x.text"
              :items="epsgCodes"
              label="EPSG Code"
              clearable
              @change="update"
            />
          </v-col>
        </v-row>
        <v-row class="pb-0">
          <v-col cols="12" md="4" offset-md="4">
            <v-text-field
              v-model.number="mountActionInformationDTO.z"
              label="Coordinate (z)"
              type="number"
              step="any"
              clearable
              @wheel.prevent
              @change="update"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="elevationDatum"
              :item-value="(x) => x.name"
              :item-text="(x) => x.name"
              :items="elevationData"
              label="Elevation Datum"
              clearable
              @change="update"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <span>
              <v-autocomplete
                v-model="mountActionInformationDTO.beginContact"
                data-role="select-begin-contact"
                :items="contacts"
                label="Begin contact"
                :disabled="readonly"
                :item-text="(x) => x.toString()"
                :item-value="(x) => x"
                required
                :rules="[rules.required]"
                class="required"
                @input="update"
              />
            </span>
          </v-col>
          <v-col v-if="withUnmount">
            <span>
              <v-autocomplete
                v-model="mountActionInformationDTO.endContact"
                data-role="select-end-contact"
                :items="contacts"
                label="End contact"
                :disabled="readonly"
                :item-text="(x) => x.toString()"
                :item-value="(x) => x"
                :required="unmountRequired"
                :clearable="!unmountRequired"
                :rules="getEndContactRules()"
                :class="unmountRequired ? 'required' : ''"
                @input="update"
              />
            </span>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-textarea
              v-model="mountActionInformationDTO.beginDescription"
              data-role="textarea-begin-description"
              label="Begin description"
              rows="3"
              :disabled="readonly"
              @input="update"
            />
          </v-col>
          <v-col v-if="withUnmount">
            <v-textarea
              v-model="mountActionInformationDTO.endDescription"
              data-role="textarea-end-description"
              label="End description"
              rows="3"
              :disabled="readonly"
              @input="update"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </span>
</template>
<script lang="ts">

import { Component, Prop, Vue, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { DateTime } from 'luxon'

import { Rules } from '@/mixins/Rules'
import { VocabularyState, LoadEpsgCodesAction, LoadElevationDataAction } from '@/store/vocabulary'

import { Contact } from '@/models/Contact'

import MountActionDateForm from '@/components/configurations/MountActionDateForm.vue'
import { MountActionDateDTO, MountActionInformationDTO, IOffsets } from '@/utils/configurationInterfaces'

@Component({
  components: {
    MountActionDateForm
  },
  computed: {
    ...mapState('vocabulary', ['epsgCodes', 'elevationData'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadEpsgCodes', 'loadElevationData'])
  }
})
export default class MountActionDetailsForm extends mixins(Rules) {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: MountActionInformationDTO

  @Prop({
    default: () => false,
    type: Boolean
  })
  readonly readonly!: boolean

  @Prop({
    default: () => true,
    type: Boolean
  })
  readonly withUnmount!: boolean

  @Prop({
    default: () => false,
    type: Boolean
  })
  readonly unmountRequired!: boolean

  @Prop({
    default: () => true,
    type: Boolean
  })
  readonly withDates!: boolean

  @Prop({
    default: () => [],
    type: Array
  })
  readonly contacts!: Contact[]

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly beginDateRules!: ((value: DateTime | null) => string | boolean)[]

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly endDateRules!: ((value: DateTime | null) => string | boolean)[]

  @Prop({
    default: (): IOffsets => ({ offsetX: 0, offsetY: 0, offsetZ: 0 }),
    required: false,
    type: Object
  })
  readonly parentOffsets!: IOffsets

  // vuex definition for typescript check
  epsgCodes!: VocabularyState['epsgCodes']
  elevationData!: VocabularyState['elevationData']
  loadElevationData!: LoadElevationDataAction
  loadEpsgCodes!: LoadEpsgCodesAction

  fetch () {
    Promise.all([this.loadElevationData(), this.loadEpsgCodes()])
  }

  get mountActionDateDTO (): MountActionDateDTO {
    return {
      beginDate: this.mountActionInformationDTO.beginDate,
      endDate: this.mountActionInformationDTO.endDate
    }
  }

  set mountActionDateDTO (value: MountActionDateDTO) {
    this.mountActionInformationDTO.beginDate = value.beginDate
    this.mountActionInformationDTO.endDate = value.endDate
  }

  get mountActionInformationDTO (): MountActionInformationDTO {
    return this.value
  }

  validateForm (): boolean {
    let isValid: boolean = false
    if (this.$refs.mountForm) {
      isValid = (this.$refs.mountForm as Vue & { validate: () => boolean }).validate()
    }
    if (isValid && this.$refs.dateForm) {
      isValid = (this.$refs.dateForm as MountActionDateForm).validateForm()
    }
    return isValid
  }

  resetValidation (): void {
    if (this.$refs.mountForm) {
      (this.$refs.mountForm as Vue & { resetValidation: () => void }).resetValidation()
    }
    if (this.$refs.dateForm) {
      (this.$refs.dateForm as MountActionDateForm).resetValidation()
    }
  }

  getEndContactRules (): ((value: any) => boolean | string)[] {
    if (this.unmountRequired) {
      // @ts-ignore
      return [this.rules.required]
    }
    return []
  }

  update () {
    this.$emit('input', this.mountActionInformationDTO)
  }

  get absoluteOffsets (): IOffsets {
    return {
      offsetX: this.parentOffsets.offsetX + this.value.offsetX,
      offsetY: this.parentOffsets.offsetY + this.value.offsetY,
      offsetZ: this.parentOffsets.offsetZ + this.value.offsetZ
    }
  }

  get elevationDatum (): string | null {
    if (!this.mountActionInformationDTO.elevationDatumName) {
      return null
    }
    const elevationDatumIndex = this.elevationData.findIndex(d => d.uri === this.mountActionInformationDTO.elevationDatumUri)
    if (elevationDatumIndex > -1) {
      return this.elevationData[elevationDatumIndex].name
    }
    return this.mountActionInformationDTO.elevationDatumName
  }

  set elevationDatum (newElevationDatumName: string | null) {
    this.mountActionInformationDTO.elevationDatumUri = ''
    if (!newElevationDatumName) {
      this.mountActionInformationDTO.elevationDatumName = ''
    } else {
      this.mountActionInformationDTO.elevationDatumName = newElevationDatumName
      const elevationDatumIndex = this.elevationData.findIndex(d => d.uri === this.mountActionInformationDTO.elevationDatumUri)
      if (elevationDatumIndex > -1) {
        this.mountActionInformationDTO.elevationDatumUri = this.elevationData[elevationDatumIndex].uri
      }
    }
  }
}
</script>

<style scoped>
/* @import "@/assets/styles/_forms.scss"; */

/* the m-annotated class is to add the unit (meters) to the fields */
.m-annotated::after {
  content: " m";
  white-space: pre;
}
</style>
