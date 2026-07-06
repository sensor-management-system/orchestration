<!--
SPDX-FileCopyrightText: 2020 - 2026
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Rubankumar Moorthy <r.moorthy@fz-juelich.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Research Centre Juelich GmbH - Institute of Bio- and Geosciences Agrosphere (IBG-3, https://www.fz-juelich.de/en/ibg/ibg-3)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-form
    ref="DynamicLocationActionInfoForm"
  >
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          :value="value.label"
          label="Label"
          @change="update(constList.label, $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-select
          :value="value.epsgCode"
          class="required"
          :item-value="(x) => x.code"
          :item-text="(x) => x.text"
          :items="epsgCodes"
          label="EPSG Code"
          :rules="[rules.required]"
          @change="update(constList.epsgCode, $event)"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-select
          :value="elevationDatum"
          class="required"
          :item-value="(x) => x.name"
          :item-text="(x) => x.name"
          :items="elevationData"
          label="Elevation Datum"
          :rules="[rules.required]"
          @change="update(constList.elevationDatum, $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card flat>
          <v-card-title>
            Begin of dynamic location
          </v-card-title>
          <v-container>
            <v-row>
              <v-col>
                <v-autocomplete
                  :value="value.beginContact"
                  class="required"
                  :items="contacts"
                  label="Begin Contact"
                  clearable
                  required
                  :item-text="(x) => x.toString()"
                  :item-value="(x) => x"
                  :rules="[rules.required]"
                  @change="update(constList.beginContact, $event)"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-textarea
                  :value="value.beginDescription"
                  label="Begin Description"
                  rows="3"
                  @input="update(constList.beginDescription,$event)"
                />
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
    <v-row v-if="value.endDate">
      <v-col cols="12">
        <v-card flat>
          <v-card-title>
            End of dynamic location
          </v-card-title>
          <v-container>
            <v-row>
              <v-col>
                <v-autocomplete
                  :value="value.endContact"
                  class="required"
                  :items="contacts"
                  label="End Contact"
                  clearable
                  required
                  :item-text="(x) => x.toString()"
                  :item-value="(x) => x"
                  :rules="[rules.required]"
                  @change="update(constList.endContact, $event)"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-textarea
                  :value="value.endDescription"
                  label="End Description"
                  rows="3"
                  @input="update(constList.endDescription,$event)"
                />
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts">
import { Component, Vue, Prop, mixins } from 'nuxt-property-decorator'
import { mapState } from 'vuex'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { VocabularyState } from '@/store/vocabulary'
import { Rules } from '@/mixins/Rules'
import { ContactsState } from '@/store/contacts'
import { Contact } from '@/models/Contact'
import { ElevationDatum } from '@/models/ElevationDatum'
import { PermissionsState } from '@/store/permissions'

@Component({
  computed: {
    ...mapState('vocabulary', ['epsgCodes', 'elevationData']),
    ...mapState('contacts', ['contacts']),
    ...mapState('permissions', ['userInfo'])
  }
})
export default class DynamicLocationActionInfoForm extends mixins(Rules) {
  @Prop({
    default: () => new DynamicLocationAction(),
    required: true,
    type: DynamicLocationAction
  })
  readonly value!: DynamicLocationAction

  private constList = {
    epsgCode: 'epsgCode',
    elevationDatum: 'elevationDatum',
    beginContact: 'beginContact',
    beginDescription: 'beginDescription',
    endContact: 'endContact',
    endDescription: 'endDescription',
    label: 'label'
  }

  // vuex definition for typescript check
  epsgCodes!: VocabularyState['epsgCodes']
  elevationData!: VocabularyState['elevationData']
  contacts!: ContactsState['contacts']
  userInfo!: PermissionsState['userInfo']

  get currentUserContactId (): string | null {
    return this.userInfo?.contactId as string | null
  }

  get elevationDatum (): string {
    const elevationDatumIndex = this.elevationData.findIndex((d: ElevationDatum) => d.uri === this.value.elevationDatumUri)
    if (elevationDatumIndex > -1) {
      return this.elevationData[elevationDatumIndex].name
    }
    return this.value.elevationDatumName
  }

  update (key: string, value: any): void {
    const newObj = DynamicLocationAction.createFromObject(this.value)

    switch (key) {
      case this.constList.epsgCode:
        newObj.epsgCode = value as string
        break
      case this.constList.elevationDatum:
        (() => {
          const elevationDatumIndex = this.elevationData.findIndex((d: ElevationDatum) => d.name === value)
          if (elevationDatumIndex > -1) {
            newObj.elevationDatumUri = this.elevationData[elevationDatumIndex].uri
          } else {
            newObj.elevationDatumUri = ''
          }
          newObj.elevationDatumName = value || '' as string
        })()
        break
      case this.constList.beginDescription:
        newObj.beginDescription = value as string
        break
      case this.constList.beginContact:
        newObj.beginContact = value as Contact | null
        break
      case this.constList.endDescription:
        newObj.endDescription = value as string
        break
      case this.constList.endContact:
        newObj.endContact = value as Contact | null
        break
      case this.constList.label:
        newObj.label = value
        break
    }
    this.$emit('input', newObj)
  }

  public validateForm (): boolean {
    return (this.$refs.DynamicLocationActionInfoForm as Vue & { validate: () => boolean }).validate()
  }

  /**
   * Try to auto-select current user as beginContact / endContact (if empty).
   * Shows a snackbar if we do have an id + contacts list but can’t find a match.
   */
  autoSelectContacts () {
    if (!this.currentUserContactId || !this.contacts?.length) {
      return
    }
    const found = this.contacts.find((c: Contact) => c.id === this.currentUserContactId)
    if (!found) {
      this.$store.commit('snackbar/setError', 'No contact found with your data')
      return
    }
    const patch: Partial<DynamicLocationAction> = {}

    // Don’t overwrite if user already picked someone
    if (!this.value.beginContact) {
      patch.beginContact = found
    }
    // Only set endContact if an endDate exists (end section is shown)
    if (this.value.endDate && !this.value.endContact) {
      patch.endContact = found
    }

    if (Object.keys(patch).length) {
      const newObj = DynamicLocationAction.createFromObject(this.value)
      Object.assign(newObj, patch)
      this.$emit('input', newObj)
    }
  }
}
</script>

<style scoped>

</style>
