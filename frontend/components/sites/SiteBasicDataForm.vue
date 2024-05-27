<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-form
      ref="basicForm"
      @submit.prevent
    >
      <v-row>
        <v-col cols="12" md="6">
          <visibility-switch
            :value="value.visibility"
            :disabled-options="[visibilityPrivateValue]"
            :rules="privateRules"
            :readonly="readonly"
            :entity-name="entityName"
            @input="update('visibility', $event)"
          />
        </v-col>
        <v-col cols="12" md="6">
          <permission-group-select
            :value="value.permissionGroups"
            :readonly="readonly"
            :entity-name="entityName"
            :rules="[pageRules.validatePermissionGroups]"
            @input="update('permissionGroups', $event)"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            :value="value.label"
            :readonly="readonly"
            :disabled="readonly"
            label="Label"
            required
            class="required"
            :rules="[rules.required]"
            @input="update('label', $event)"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-autocomplete
            :value="value.outerSiteId"
            :item-value="(x) => x.id"
            :item-text="(x) => x.label"
            :items="sitesExceptSelf"
            label="Part of"
            :readonly="readonly"
            hint="Select a site to which this site belongs"
            persistent-hint
            clearable
            @input="update('outerSiteId',$event)"
          />
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="6">
          <combobox
            label="Usage"
            clearable
            :items="siteUsages"
            item-text="name"
            :value="valueSiteUsageItem"
            :readonly="readonly"
            :disabled="readonly"
            @input="updateSiteUsage"
          >
            <template #append-outer>
              <v-tooltip
                v-if="itemHasDefinition(valueSiteUsageItem)"
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
                <span>{{ valueSiteUsageItem.definition }}</span>
              </v-tooltip>
              <v-btn icon @click="showNewSiteUsageDialog = true">
                <v-icon>
                  mdi-tooltip-plus-outline
                </v-icon>
              </v-btn>
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
          </combobox>
        </v-col>
        <v-col cols="12" md="6">
          <combobox
            label="Type"
            clearable
            :items="siteTypes"
            item-text="name"
            :value="valueSiteTypeItem"
            :readonly="readonly"
            :disabled="readonly"
            @input="updateSiteType"
          >
            <template #append-outer>
              <v-tooltip
                v-if="itemHasDefinition(valueSiteTypeItem)"
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
                <span>{{ valueSiteTypeItem.definition }}</span>
              </v-tooltip>
              <v-btn icon @click="showNewSiteTypeDialog = true">
                <v-icon>
                  mdi-tooltip-plus-outline
                </v-icon>
              </v-btn>
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
          </combobox>
        </v-col>
      </v-row>

      <v-row align="center">
        <v-col v-if="siteAttachments.length > 0" cols="12">
          <AttachmentImagesForm
            :attachments="siteAttachments"
            :value="value.images"
            :download-attachment="downloadAttachment"
            :proxy-url="proxyUrl"
            @input="update('images', $event)"
          />
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <v-textarea
            :value="value.description"
            :readonly="readonly"
            :disabled="readonly"
            label="Description"
            rows="3"
            @input="update('description', $event)"
          />
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="9">
          <v-text-field
            :value="value.website"
            :readonly="readonly"
            :disabled="readonly"
            label="Website"
            placeholder="https://"
            type="url"
            @input="update('website', $event)"
          >
            <template slot="append">
              <a v-if="value.website.length > 0" :href="value.website" target="_blank">
                <v-icon
                  small
                >
                  mdi-open-in-new
                </v-icon>
              </a>
            </template>
          </v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="9">
          <v-select
            :value="value.epsgCode"
            class="required"
            :item-value="(x) => x.code"
            :item-text="(x) => x.text"
            :items="epsgCodes()"
            label="EPSG Code"
            :rules="[rules.required]"
            @change="update('epsgCode', $event)"
          />
        </v-col>
      </v-row>
      <v-divider
        class="my-4"
      />
      <v-row>
        <v-col cols="12" class="mb-4">
          <h4>Draw the site geometry</h4>
          <SiteMap :value="value.geometry" :outer="outerSiteGeometry" @updateCoords="update('geometry', $event)" />
        </v-col>
      </v-row>
      <h4>Address information</h4>
      <v-row>
        <v-col cols="8">
          <autocomplete-text-input
            :value="value.address.street"
            :readonly="readonly"
            :disabled="readonly"
            label="Street"
            placeholder="Street name"
            endpoint="site-streets"
            @input="update('address.street', $event)"
          />
        </v-col>
        <v-col cols="4">
          <autocomplete-text-input
            :value="value.address.streetNumber"
            :readonly="readonly"
            :disabled="readonly"
            label="Street number"
            placeholder="Street number"
            endpoint="site-street-numbers"
            @input="update('address.streetNumber', $event)"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6">
          <autocomplete-text-input
            :value="value.address.city"
            :readonly="readonly"
            :disabled="readonly"
            label="City"
            placeholder="City"
            endpoint="site-cities"
            @input="update('address.city', $event)"
          />
        </v-col>
        <v-col cols="2">
          <autocomplete-text-input
            :value="value.address.zipCode"
            :readonly="readonly"
            :disabled="readonly"
            label="Zip code"
            placeholder="Zip code"
            endpoint="site-zip-codes"
            @input="update('address.zipCode', $event)"
          />
        </v-col>
        <v-col cols="4">
          <combobox
            :value="value.address.country"
            :items="countryNames"
            :readonly="readonly"
            :disabled="readonly"
            label="Country"
            placeholder="Country"
            @input="update('address.country', $event)"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6">
          <autocomplete-text-input
            :value="value.address.building"
            :readonly="readonly"
            :disabled="readonly"
            label="Building"
            placeholder="Building"
            endpoint="site-buildings"
            @input="update('address.building', $event)"
          />
        </v-col>
        <v-col cols="6">
          <autocomplete-text-input
            :value="value.address.room"
            :readonly="readonly"
            :disabled="readonly"
            label="Room"
            placeholder="Room"
            endpoint="site-rooms"
            @input="update('address.room', $event)"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <label>Keywords</label>
          <v-chip-group>
            <v-chip v-for="keyword, idx in value.keywords" :key="idx" close small @click:close="removeKeyword(keyword)">
              {{ keyword }}
            </v-chip>
          </v-chip-group>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <autocomplete-text-input
            ref="newKeywordField"
            :search-input.sync="newKeyword"
            label="New keyword"
            endpoint="keywords"
            @keyup.enter="addNewKeyword"
          >
            <template #append>
              <v-btn icon :disabled="!newKeyword" @click="addNewKeywordAndBlurNewKeywordField">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </template>
          </autocomplete-text-input>
        </v-col>
      </v-row>
    </v-form>
    <site-usage-dialog
      v-model="showNewSiteUsageDialog"
      :initial-term="valueSiteUsageItem ? valueSiteUsageItem.name : null"
      @aftersubmit="updateSiteUsage"
    />
    <site-type-dialog
      v-model="showNewSiteTypeDialog"
      :initial-term="valueSiteTypeItem ? valueSiteTypeItem.name : null"
      :initial-site-usage-id="valueSiteUsageItem ? valueSiteUsageItem.id : null"
      @aftersubmit="updateSiteType"
    />
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { Rules } from '@/mixins/Rules'

import { ILatLng, Site } from '@/models/Site'
import { Status } from '@/models/Status'
import { PermissionGroup } from '@/models/PermissionGroup'
import { Visibility } from '@/models/Visibility'
import { DetailedUserInfo } from '@/models/UserInfo'
import { ICvSelectItem, hasDefinition, CvSelectItem } from '@/models/CvSelectItem'

import PermissionGroupSelect from '@/components/PermissionGroupSelect.vue'
import VisibilitySwitch from '@/components/VisibilitySwitch.vue'
import AutocompleteTextInput from '@/components/shared/AutocompleteTextInput.vue'
import AttachmentImagesForm from '@/components/shared/AttachmentImagesForm.vue'
import SiteUsageDialog from '@/components/sites/SiteUsageDialog.vue'
import SiteTypeDialog from '@/components/sites/SiteTypeDialog.vue'
import Combobox from '@/components/shared/Combobox.vue'

import Validator from '@/utils/validator'
import SiteMap from '@/components/sites/SiteMap.vue'
import { SiteUsage } from '@/models/SiteUsage'
import { SiteType } from '@/models/SiteType'

import { DownloadAttachmentAction, SearchSitesAction, SitesState } from '@/store/sites'
import { ProxyUrlAction } from '@/store/proxy'
import { VocabularyState } from '@/store/vocabulary'
import { Image } from '@/models/Image'
interface INameAndUri {
  name: string
  uri: string
}

type SiteUsageComboboxValue = SiteUsage | string | undefined
type SiteTypeComboboxValue = SiteType | string | undefined

@Component({
  components: {
    PermissionGroupSelect,
    VisibilitySwitch,
    SiteMap,
    AutocompleteTextInput,
    SiteUsageDialog,
    SiteTypeDialog,
    Combobox,
    AttachmentImagesForm
  },
  methods: {
    ...mapState('vocabulary', ['epsgCodes']),
    ...mapActions('sites', ['searchSites', 'downloadAttachment']),
    ...mapActions('proxy', ['proxyUrl'])
  },
  computed: {
    ...mapState('sites', ['sites', 'siteAttachments'])
  }
})
export default class SiteBasicDataForm extends mixins(Rules) {
  private showNewSiteUsageDialog = false
  private showNewSiteTypeDialog = false
  private states: Status[] = []
  private userInfo: DetailedUserInfo | null = null
  private entityName: string = 'site / lab'
  private newKeyword = ''

  // vuex definition for typescript check
  siteAttachments!: SitesState['siteAttachments']
  downloadAttachment!: DownloadAttachmentAction
  proxyUrl!: ProxyUrlAction
  epsgCodes!: VocabularyState['epsgCodes']
  sites!: SitesState['sites']
  searchSites!: SearchSitesAction

  @Prop({
    required: true,
    type: Site
  })
  readonly value!: Site

  @Prop({
    default: () => false,
    type: Boolean
  })
  readonly readonly!: boolean

  @Prop({
    default: [] as SiteUsage[],
    required: true,
    type: Array
  })
  readonly siteUsages!: SiteUsage[]

  @Prop({
    default: () => [] as SiteType[],
    required: true,
    type: Array
  })
  readonly siteTypes!: SiteType[]

  @Prop({
    default: () => [] as string[],
    required: true,
    type: Array
  })
  readonly countryNames!: string[]

  async created () {
    try {
      await this.searchSites()
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Failed to laod sites')
    }
  }

  get sitesExceptSelf (): Site[] {
    return this.sites.filter(x => x.id !== this.value.id)
  }

  get pageRules (): {[index: string]: (a: any) => (boolean | string)} {
    // For the moment there is no way a site could be private.
    const isPrivate = false
    const canBePrivate = false

    return {
      validatePermissionGroups: Validator.validatePermissionGroups(isPrivate, this.entityName, canBePrivate)
    }
  }

  get privateRules () {
    return [
      Validator.validateVisibility(this.value.visibility, [], this.entityName)
    ]
  }

  /**
   * returns the URI of an value
   *
   * @param {string} name - the name of the dictionary to look in
   * @param {string} value - the value to look the URI for
   * @returns {string} the URI or an empty string
   */
  private getUriByValue (name: string, value: string): string {
    let valueToSet = ''

    const elementsByName: { [name: string]: { elements: INameAndUri[] } } = {
      siteUsageName: {
        elements: this.siteUsages
      },
      siteTypeName: {
        elements: this.siteTypes
      }
    }
    if (!elementsByName[name]) {
      return valueToSet
    }
    // the comoboboxes may set the value to null,
    // but we don't want to work further with nulls
    //
    // all of the comboboxes see the empty string as the
    // "no value" choice
    if (value === null) {
      value = ''
    }
    const index = elementsByName[name].elements.findIndex(x => x.name === value)
    if (index > -1) {
      valueToSet = elementsByName[name].elements[index].uri
    }
    return valueToSet
  }

  /**
   * updates the site usage
   *
   * @param {SiteUsageComboboxValue} value - an object as provided by the combobox
   * @fires SiteBasicDataForm#input
   */
  updateSiteUsage (value: SiteUsageComboboxValue): void {
    const newObj: Site = Site.createFromObject(this.value)

    if (value) {
      if (typeof value === 'string') {
        newObj.siteUsageName = value
        newObj.siteUsageUri = this.getUriByValue('siteUsageName', value)
      } else {
        newObj.siteUsageName = value.name
        newObj.siteUsageUri = value.uri
      }
    } else {
      newObj.siteUsageName = ''
      newObj.siteUsageUri = ''
    }

    this.$emit('input', newObj)
  }

  /**
   * updates the site type
   *
   * @param {SiteTypeComboboxValue} value - an object as provided by the combobox
   * @fires SiteBasicDataForm#input
   */
  updateSiteType (value: SiteTypeComboboxValue): void {
    const newObj: Site = Site.createFromObject(this.value)

    if (value) {
      if (typeof value === 'string') {
        newObj.siteTypeName = value
        newObj.siteTypeUri = this.getUriByValue('siteTypeName', value)
      } else {
        newObj.siteTypeName = value.name
        newObj.siteTypeUri = value.uri
      }
    } else {
      newObj.siteTypeName = ''
      newObj.siteTypeUri = ''
    }

    this.$emit('input', newObj)
  }

  update (key: string, value: string|PermissionGroup[]|Image[]) {
    const newObj = Site.createFromObject(this.value)

    switch (key) {
      case 'label':
        newObj.label = value as string
        break

      case 'outerSiteId':
        newObj.outerSiteId = value as string
        break

      case 'images':
        newObj.images = value as Image[]
        break

      case 'description':
        newObj.description = value as string
        break

      case 'website':
        newObj.website = value as string
        break

      case 'epsgCode':
        newObj.epsgCode = value as string
        break

      case 'geometry':
        newObj.geometry = value as unknown as ILatLng[]
        break

      case 'address.street':
        newObj.address.street = value as string
        break

      case 'address.streetNumber':
        newObj.address.streetNumber = value as string
        break

      case 'address.city':
        newObj.address.city = value as string
        break

      case 'address.zipCode':
        newObj.address.zipCode = value as string
        break

      case 'address.country':
        newObj.address.country = value as string
        break

      case 'address.building':
        newObj.address.building = value as string
        break

      case 'address.room':
        newObj.address.room = value as string
        break

      case 'visibility':
        switch (value) {
          case Visibility.Internal:
            newObj.visibility = Visibility.Internal
            break
          case Visibility.Public:
            newObj.visibility = Visibility.Public
            break
        }
        break
      case 'permissionGroups':
        newObj.permissionGroups = value as PermissionGroup[]
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }
    this.$emit('input', newObj)
  }

  /**
   * returns an item to be used as the value of a combobox
   *
   * Checks whether value.propertyName and value.propertyUri can be found in
   * the list of CV properties. Returns the found property, otherwise
   * constructs one from the name and the uri. Returns null if both fields are
   * empty.
   *
   * @returns {ICvSelectItem|null} the property, a constructed one or null
   */
  get valueSiteUsageItem (): ICvSelectItem | null {
    if (!this.value.siteUsageName && !this.value.siteUsageUri) {
      return null
    }
    const siteUsage = this.siteUsages.find(c => c.uri === this.value.siteUsageUri)
    if (siteUsage) {
      return siteUsage
    }

    // Just there to have a toString method
    return new CvSelectItem({
      name: this.value.siteUsageName,
      uri: this.value.siteUsageUri,
      definition: '',
      id: null
    })
  }

  /**
   * returns an item to be used as the value of a combobox
   *
   * Checks whether value.propertyName and value.propertyUri can be found in
   * the list of CV properties. Returns the found property, otherwise
   * constructs one from the name and the uri. Returns null if both fields are
   * empty.
   *
   * @returns {ICvSelectItem|null} the property, a constructed one or null
   */
  get valueSiteTypeItem (): ICvSelectItem | null {
    if (!this.value.siteTypeName && !this.value.siteTypeUri) {
      return null
    }
    const siteType = this.siteTypes.find(c => c.uri === this.value.siteTypeUri)
    if (siteType) {
      return siteType
    }

    // Just there to have a toString method
    return new CvSelectItem({
      name: this.value.siteTypeName,
      uri: this.value.siteTypeUri,
      definition: '',
      id: null
    })
  }

  /**
   * checks if an URI ends with a specific id
   *
   * @param {string} uri - the URI to check the id for
   * @param {string} id - the id
   * @returns {boolean} returns true when the id was found, otherwise false
   */
  private checkUriEndsWithId (uri: string, id: string): boolean {
    return uri.match(new RegExp('^.+/' + id + '/?$')) !== null
  }

  /**
   * validates the user input
   *
   * Note: we can't use 'validate' as a method name, so I used 'validateForm'
   *
   * @return {boolean} true when input is valid, otherwise false
   */
  public validateForm (): boolean {
    return (this.$refs.basicForm as Vue & { validate: () => boolean }).validate()
  }

  get visibilityPrivateValue (): Visibility {
    return Visibility.Private
  }

  /**
   * checks wheter the item has a non-empty definition property
   *
   * @param {ICvSelectItem} item - the item to check for
   * @returns {boolean} returns true when the definition property exists and is not falsy
   */
  itemHasDefinition (item: ICvSelectItem): boolean {
    return hasDefinition(item)
  }

  addNewKeyword () {
    if (!this.newKeyword) {
      return
    }
    const newObj = Site.createFromObject(this.value)
    if (!newObj.keywords.includes(this.newKeyword)) {
      newObj.keywords.push(this.newKeyword)
    }
    this.newKeyword = ''
    this.$emit('input', newObj)
  }

  addNewKeywordAndBlurNewKeywordField () {
    this.addNewKeyword()
    this.$nuxt.$nextTick(() => {
      (this.$refs.newKeywordField as Vue & { blur: () => void }).blur()
    })
  }

  removeKeyword (keyword: string) {
    const newObj = Site.createFromObject(this.value)
    newObj.keywords = newObj.keywords.filter(k => k !== keyword)
    this.$emit('input', newObj)
  }

  get outerSiteGeometry (): ILatLng[] {
    if (!this.value.outerSiteId) {
      return []
    }
    const siteIdx = this.sites.findIndex(x => x.id === this.value.outerSiteId)
    if (siteIdx < 0) {
      return []
    }
    const outerSite = this.sites[siteIdx]
    return outerSite.geometry
  }
}
</script>
