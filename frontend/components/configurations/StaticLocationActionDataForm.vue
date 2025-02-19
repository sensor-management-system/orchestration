<!--
SPDX-FileCopyrightText: 2022 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-form
    ref="basicForm"
    @submit.prevent
  >
    <v-card>
      <v-card-title>
        Begin of the static location
      </v-card-title>
      <v-card-text class="text--primary">
        <v-row>
          <v-col cols="12" md="6">
            <DateTimePicker
              :value="value.beginDate"
              label="Begin date"
              placeholder="e.g 2000-01-31 12:00"
              :required="true"
              :rules="[...[rules.required],...beginDateExtraRules]"
              @input="update('beginDate', $event)"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              :value="value.label"
              label="Label"
              @input="update('label', $event)"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="4">
            <v-text-field
              :value="value.x"
              label="x"
              type="number"
              step="any"
              :rules="[rules.required]"
              class="required"
              @wheel.prevent
              @change="update('x', $event)"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              :value="value.y"
              label="y"
              type="number"
              step="any"
              :rules="[rules.required]"
              class="required"
              @wheel.prevent
              @change="update('y', $event)"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              :value="value.epsgCode"
              :item-value="(x) => x.code"
              :item-text="(x) => x.text"
              :items="epsgCodes"
              label="EPSG Code"
              :rules="[rules.required]"
              @change="update('epsgCode', $event)"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="4" offset-md="4">
            <v-text-field
              :value="value.z"
              label="z"
              type="number"
              step="any"
              @wheel.prevent
              @change="update('z', $event)"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              :value="elevationDatum"
              :item-value="(x) => x.name"
              :item-text="(x) => x.name"
              :items="elevationData"
              label="Elevation Datum"
              :rules="[rules.required]"
              @change="update('elevationDatum', $event)"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-alert
              dense
              type="info"
            >
              <p class="mb-0">
                You can select a point on the map to set the coordinates or use the button to take your current location.
              </p>
              <p class="mb-0">
                <em>
                  Please note that the accuracy of the automatic localization is limited by the device you currently use.
                  Consider using differential GPS if you need high accuracy.
                </em>
              </p>
            </v-alert>
            <location-map
              :value="location"
              @input="update('location', $event)"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="12">
            <v-textarea
              :value="value.description"
              label="Description"
              rows="3"
              @input="update('beginDescription', $event)"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="6">
            <v-autocomplete
              :value="value.beginContact"
              :items="contacts"
              label="Contact"
              clearable
              required
              :item-text="(x) => x.toString()"
              :item-value="(x) => x"
              :rules="[rules.required]"
              class="required"
              @change="update('beginContact', $event)"
            />
          </v-col>
          <v-col v-if="currentUserContactId" cols="12" md="1" align-self="center">
            <v-btn small @click="selectCurrentUserAsContact(typeBeginContact)">
              {{ labelForSelectMeButton }}
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
      <v-divider class="mx-4 mt-4" />
      <v-card-title id="static-location-end">
        End of the static location
      </v-card-title>
      <v-card-text class="text--primary">
        <v-row>
          <v-col cols="12" md="6">
            <DateTimePicker
              :value="value.endDate"
              label="End date"
              placeholder="e.g 2000-01-31 12:00"
              :rules="endDateExtraRules"
              @input="update('endDate', $event)"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="12">
            <v-textarea
              :value="value.endDescription"
              label="Description"
              rows="3"
              @input="update('endDescription', $event)"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="6">
            <v-autocomplete
              :value="value.endContact"
              :items="contacts"
              label="Contact"
              clearable
              required
              :item-text="(x) => x.toString()"
              :item-value="(x) => x"
              @change="update('endContact', $event)"
            />
          </v-col>
          <v-col v-if="currentUserContactId" cols="12" md="1" align-self="center">
            <v-btn small @click="selectCurrentUserAsContact(typeEndContact)">
              {{ labelForSelectMeButton }}
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
      <slot name="actions" />
    </v-card>
  </v-form>
</template>

<script lang="ts">
import { Component, mixins, Prop, Vue } from 'nuxt-property-decorator'
import { mapGetters, mapState } from 'vuex'
import { DateTime } from 'luxon'
import DateTimePicker from '@/components/DateTimePicker.vue'
import LocationMap from '@/components/configurations/LocationMap.vue'
import { StaticLocationAction } from '@/models/StaticLocationAction'
import { VocabularyState } from '@/store/vocabulary'
import { ContactsState } from '@/store/contacts'
import {
  ConfigurationsState,
  LocationActionTimepointsExceptPassedIdAndTypeTypeGetter,
  LocationTypes
} from '@/store/configurations'
import { StationaryLocation } from '@/models/Location'
import {
  extractStationaryLocationFromStaticLocationBeginAction,
  setCoordinatesInStaticLocationBeginActionFromStationaryLocation
} from '@/utils/locationHelper'
import { ElevationDatum } from '@/models/ElevationDatum'
import { Contact } from '@/models/Contact'
import Validator from '@/utils/validator'
import { Rules } from '@/mixins/Rules'
import { parseFloatOrNull } from '@/utils/numericsHelper'
import { PermissionsState } from '@/store/permissions'

@Component({
  components: {
    DateTimePicker,
    LocationMap
  },
  computed: {
    ...mapState('vocabulary', ['epsgCodes', 'elevationData']),
    ...mapState('contacts', ['contacts']),
    ...mapGetters('configurations', ['locationActionTimepointsExceptPassedIdAndType']),
    ...mapState('configurations', ['configuration']),
    ...mapState('permissions', ['userInfo'])
  }
})
export default class StaticLocationActionDataForm extends mixins(Rules) {
  private readonly labelForSelectMeButton = 'Add current user'
  @Prop({
    default: () => new StaticLocationAction(),
    required: true,
    type: StaticLocationAction
  })
  readonly value!: StaticLocationAction

  private readonly typeBeginContact = 'beginContact'
  private readonly typeEndContact = 'endContact'

  // vuex definition for typescript check
  epsgCodes!: VocabularyState['epsgCodes']
  elevationData!: VocabularyState['elevationData']
  contacts!: ContactsState['contacts']
  configuration!: ConfigurationsState['configuration']
  locationActionTimepointsExceptPassedIdAndType!: LocationActionTimepointsExceptPassedIdAndTypeTypeGetter
  userInfo!: PermissionsState['userInfo']

  get currentUserContactId (): string | null {
    return this.userInfo?.contactId as string | null
  }

  get elevationDatum (): string {
    const elevationDatumIndex = this.elevationData.findIndex(d => d.uri === this.value.elevationDatumUri)
    if (elevationDatumIndex > -1) {
      return this.elevationData[elevationDatumIndex].name
    }
    return this.value.elevationDatumName
  }

  get location (): StationaryLocation {
    return extractStationaryLocationFromStaticLocationBeginAction(this.value)
  }

  update (key: string, value: any): void {
    const copy = StaticLocationAction.createFromObject(this.value)

    switch (key) {
      case 'beginDate':
        copy.beginDate = value as DateTime | null
        break
      case 'x':
        copy.x = parseFloatOrNull(value)
        break
      case 'y':
        copy.y = parseFloatOrNull(value)
        break
      case 'z':
        copy.z = parseFloatOrNull(value)
        break
      case 'location':
        (() => {
          const newLocation = value as StationaryLocation
          setCoordinatesInStaticLocationBeginActionFromStationaryLocation(copy, newLocation)
        })()
        break
      case 'epsgCode':
        copy.epsgCode = value as string
        break
      case 'elevationDatum':
        (() => {
          const elevationDatumIndex = this.elevationData.findIndex((d: ElevationDatum) => d.name === value)
          if (elevationDatumIndex > -1) {
            copy.elevationDatumUri = this.elevationData[elevationDatumIndex].uri
          }
          copy.elevationDatumName = value as string
        })()
        break
      case 'beginDescription':
        copy.beginDescription = value as string
        break
      case 'beginContact':
        copy.beginContact = value as Contact | null
        break
      case 'label':
        copy.label = value as string
        break
      case 'endDate':
        copy.endDate = value as DateTime | null
        break
      case 'endDescription':
        copy.endDescription = value as string
        break
      case 'endContact':
        copy.endContact = value as Contact | null
        break
    }
    this.$emit('input', copy)
  }

  public isValid (): boolean {
    return (this.$refs.basicForm as Vue & { validate: () => boolean }).validate()
  }

  selectCurrentUserAsContact (type: string) {
    if (this.currentUserContactId) {
      const foundUser = this.contacts.find((c: Contact) => c.id === this.currentUserContactId)
      if (foundUser) {
        this.update(type, foundUser)
        return
      }
    }
    this.$store.commit('snackbar/setError', 'No contact found with your data')
  }

  get timepointsExceptCurrentlyEdited () {
    return this.locationActionTimepointsExceptPassedIdAndType(this.value.id, LocationTypes.staticStart)
  }

  get beginDateExtraRules (): any[] {
    return [
      Validator.canNotIntersectWithExistingInterval(this.value.beginDate, this.timepointsExceptCurrentlyEdited),
      Validator.startDateMustBeAfterPreviousAction(this.value.beginDate, this.value.endDate, this.timepointsExceptCurrentlyEdited),
      Validator.validateStartDateIsBeforeEndDate(this.value.beginDate, this.value.endDate),
      Validator.canNotStartAnActionAfterAnActiveAction(this.value.beginDate, this.timepointsExceptCurrentlyEdited),
      Validator.dateMustBeInRangeOfConfigurationDates(this.configuration, this.value.beginDate)
    ]
  }

  get endDateExtraRules (): any[] {
    return [
      Validator.canNotIntersectWithExistingInterval(this.value.endDate, this.timepointsExceptCurrentlyEdited),
      Validator.validateStartDateIsBeforeEndDate(this.value.beginDate, this.value.endDate),
      Validator.endDateMustBeBeforeNextAction(this.value.beginDate, this.value.endDate, this.timepointsExceptCurrentlyEdited),
      Validator.dateMustBeInRangeOfConfigurationDates(this.configuration, this.value.endDate)
    ]
  }
}
</script>

<style scoped>

</style>
