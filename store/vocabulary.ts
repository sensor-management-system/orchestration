/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */
import { Commit, GetterTree, ActionTree } from 'vuex'
import { RootState } from '@/store'

import { ActionCategory } from '@/models/ActionCategory'
import { AggregationType } from '@/models/AggregationType'
import { Manufacturer } from '@/models/Manufacturer'
import { Status } from '@/models/Status'
import { PlatformType } from '@/models/PlatformType'
import { DeviceType } from '@/models/DeviceType'
import { ActionType } from '@/models/ActionType'
import { Compartment } from '@/models/Compartment'
import { SamplingMedia } from '@/models/SamplingMedia'
import { Property } from '@/models/Property'
import { Unit } from '@/models/Unit'
import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'
import { EpsgCode } from '@/models/EpsgCode'
import { ElevationDatum } from '@/models/ElevationDatum'
import { CvContactRole } from '@/models/CvContactRole'
import { SiteType } from '@/models/SiteType'
import { SiteUsage } from '@/models/SiteUsage'
import { Country } from '@/models/Country'
import { License } from '@/models/License'

import { ACTION_TYPE_API_FILTER_DEVICE, ACTION_TYPE_API_FILTER_PLATFORM, ACTION_TYPE_API_FILTER_CONFIGURATION, ActionTypeApiFilterType } from '@/services/cv/ActionTypeApi'
import { GlobalProvenance } from '@/models/GlobalProvenance'

const KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION = 'device_calibration'
const KIND_OF_ACTION_TYPE_GENERIC_CONFIGURATION_ACTION = 'generic_configuration_action'
const KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION = 'generic_device_action'
const KIND_OF_ACTION_TYPE_GENERIC_PLATFORM_ACTION = 'generic_platform_action'
const KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION = 'parameter_change_action'
const KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE = 'software_update'

export interface VocabularyState {
  manufacturers: Manufacturer[]
  equipmentstatus: Status[]
  devicetypes: DeviceType[]
  platformtypes: PlatformType[],
  platformGenericActionTypes: ActionType[],
  deviceGenericActionTypes: ActionType[],
  configurationGenericActionTypes: ActionType[],
  compartments: Compartment[],
  samplingMedia: SamplingMedia[],
  properties: Property[],
  units: Unit[],
  measuredQuantityUnits: MeasuredQuantityUnit[],
  epsgCodes: EpsgCode[],
  elevationData: ElevationDatum[],
  cvContactRoles: CvContactRole[],
  globalProvenances: GlobalProvenance[],
  aggregationtypes: AggregationType[],
  actionCategories: ActionCategory[],
  siteUsages: SiteUsage[],
  siteTypes: SiteType[],
  countries: Country[],
  licenses: License[]
}

const state = (): VocabularyState => ({
  manufacturers: [],
  equipmentstatus: [],
  devicetypes: [],
  platformtypes: [],
  platformGenericActionTypes: [],
  deviceGenericActionTypes: [],
  configurationGenericActionTypes: [],
  compartments: [],
  samplingMedia: [],
  properties: [],
  units: [],
  measuredQuantityUnits: [],
  epsgCodes: [],
  elevationData: [],
  cvContactRoles: [],
  globalProvenances: [],
  aggregationtypes: [],
  actionCategories: [],
  siteUsages: [],
  siteTypes: [],
  countries: [],
  licenses: []
})

export type ActionTypeItem = { id: string, name: string, uri: string, kind: string }
export type GetPlatformTypeByUriGetter = (uri: string) => PlatformType | undefined
export type GetDeviceTypeByUriGetter = (uri: string) => DeviceType | undefined
export type GetSiteUsageByUriGetter = (uri: string) => SiteUsage | undefined
export type getSiteTypeByUriGetter = (uri: string) => SiteType | undefined
export type GetEquipmentstatusByUriGetter = (uri: string) => Status | undefined
export type GetManufacturerByUriGetter = (uri: string) => Manufacturer | undefined
export type PlatformActionTypeItemsGetter = ActionTypeItem[]
export type DeviceActionTypeItemsGetter = ActionTypeItem[]
export type ConfigurationActionTypeItemsGetter = ActionTypeItem[]
export type CountryNamesGetter = string[]

const getters: GetterTree<VocabularyState, RootState> = {
  getPlatformTypeByUri: (state: VocabularyState) => (uri: string): PlatformType | undefined => {
    return state.platformtypes.find((platformType: PlatformType) => {
      return platformType.uri === uri
    })
  },
  getDeviceTypeByUri: (state: VocabularyState) => (uri: string): DeviceType | undefined => {
    return state.devicetypes.find((deviceType: DeviceType) => {
      return deviceType.uri === uri
    })
  },
  getEquipmentstatusByUri: (state: VocabularyState) => (uri: string): Status | undefined => {
    return state.equipmentstatus.find((equipmentstatus: Status) => {
      return equipmentstatus.uri === uri
    })
  },
  getManufacturerByUri: (state: VocabularyState) => (uri: string): Manufacturer | undefined => {
    return state.manufacturers.find((manufacturer: Manufacturer) => {
      return manufacturer.uri === uri
    })
  },
  getSiteUsageByUri: (state: VocabularyState) => (uri: string): SiteUsage | undefined => {
    return state.siteUsages.find(s => s.uri === uri)
  },
  getSiteTypeByUri: (state: VocabularyState) => (uri: string): SiteType | undefined => {
    return state.siteTypes.find(s => s.uri === uri)
  },
  platformActionTypeItems: (state: VocabularyState) => {
    return [
      {
        id: 'software_update',
        name: 'Software Update',
        uri: '',
        kind: KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
      },
      {
        id: 'parameter_change_action',
        name: 'Parameter Value Change',
        uri: '',
        kind: KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION
      },
      ...state.platformGenericActionTypes.map((actionType) => {
        return {
          id: actionType.id,
          name: actionType.name,
          uri: actionType.uri,
          kind: KIND_OF_ACTION_TYPE_GENERIC_PLATFORM_ACTION
        }
      })
    ].sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()))
  },
  deviceActionTypeItems: (state: VocabularyState) => {
    return [
      {
        id: 'device_calibration',
        name: 'Device Calibration',
        uri: '',
        kind: KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION
      },
      {
        id: 'software_update',
        name: 'Software Update',
        uri: '',
        kind: KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
      },
      {
        id: 'parameter_change_action',
        name: 'Parameter Value Change',
        uri: '',
        kind: KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION
      },
      ...state.deviceGenericActionTypes.map((actionType) => {
        return {
          id: actionType.id,
          name: actionType.name,
          uri: actionType.uri,
          kind: KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION
        }
      })
    ].sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()))
  },
  configurationActionTypeItems: (state: VocabularyState) => {
    return [
      {
        id: 'parameter_change_action',
        name: 'Parameter Value Change',
        uri: '',
        kind: KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION
      },
      ...state.configurationGenericActionTypes.map((actionType) => {
        return {
          id: actionType.id,
          name: actionType.name,
          uri: actionType.uri,
          kind: KIND_OF_ACTION_TYPE_GENERIC_CONFIGURATION_ACTION
        }
      })
    ].sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()))
  },
  countryNames: (state: VocabularyState) => {
    // We want to have germany as the first entry, so that this is the
    // first one in the select list (as we expect it to be the most common choice).
    const germany = state.countries.filter(c => c.name === 'Germany')
    const countriesThatAreNotGermany = state.countries.filter(c => c.name !== 'Germany')
    const countries = [...germany, ...countriesThatAreNotGermany]
    return countries.map(c => c.name)
  }
}

export type LoadManufacturersAction = () => Promise<void>
export type LoadEquipmentstatusAction = () => Promise<void>
export type LoadDevicetypesAction = () => Promise<void>
export type LoadPlatformtypesAction = () => Promise<void>
export type LoadPlatformGenericActionTypesAction = () => Promise<void>
export type LoadDeviceGenericActionTypesAction = () => Promise<void>
export type LoadConfigurationGenericActionTypesAction = () => Promise<void>
export type LoadCompartmentsAction = () => Promise<void>
export type LoadSamplingMediaAction = () => Promise<void>
export type LoadPropertiesAction = () => Promise<void>
export type LoadUnitsAction = () => Promise<void>
export type LoadMeasuredQuantityUnitsAction = () => Promise<void>
export type LoadEpsgCodesAction = () => Promise<void>
export type LoadElevationDataAction = () => Promise<void>
export type LoadCvContactRolesAction = () => Promise<void>
export type LoadGlobalProvenancesAction = () => Promise<void>
export type LoadAggregationtypesAction = () => Promise<void>
export type LoadActionCategoriesAction = () => Promise<void>
export type LoadSiteUsagesAction = () => Promise<void>
export type LoadSiteTypesAction = () => Promise<void>
export type LoadCountriesAction = () => Promise<void>
export type LoadLicensesAction = () => Promise<void>
export type AddDeviceTypeAction = ({ devicetype }: {devicetype: DeviceType}) => Promise<DeviceType>
export type AddPlatformTypeAction = ({ platformtype }: {platformtype: PlatformType}) => Promise<PlatformType>
export type AddManufacturerAction = ({ manufacturer }: { manufacturer: Manufacturer}) => Promise<Manufacturer>
export type AddEquipmentstatusAction = ({ status }: { status: Status }) => Promise<Status>
export type AddCvContactRoleAction = ({ contactRole }: { contactRole: CvContactRole }) => Promise<CvContactRole>
export type AddCompartmentAction = ({ compartment }: { compartment: Compartment }) => Promise<Compartment>
export type AddSamplingMediaAction = ({ samplingMedium }: { samplingMedium: SamplingMedia}) => Promise<SamplingMedia>
export type AddPropertyAction = ({ property }: { property: Property}) => Promise<Property>
export type AddActiontypeAction = ({ actiontype, actionCategoryTerm }: {actiontype: ActionType, actionCategoryTerm: ActionTypeApiFilterType}) => Promise<ActionType>
export type AddUnitAction = ({ unit }: {unit: Unit }) => Promise<Unit>
export type AddMeasuredQuantityUnitAction = ({ measuredQuantityUnit }: { measuredQuantityUnit: MeasuredQuantityUnit }) => Promise<MeasuredQuantityUnit>
export type AddSiteUsageAction = ({ siteUsage }: { siteUsage: SiteUsage }) => Promise<SiteUsage>
export type AddSiteTypeAction = ({ siteType }: { siteType: SiteType }) => Promise<SiteType>
export type AddAggregationTypeAction = ({ aggregationType }: { aggregationType: AggregationType}) => Promise<AggregationType>
export type AddLicenseAction = ({ license }: { license: License }) => Promise<License>

const actions: ActionTree<VocabularyState, RootState> = {
  async loadManufacturers ({ commit }: { commit: Commit }): Promise<void> {
    // @ts-ignore
    commit('setManufacturers', await this.$api.manufacturer.findAll())
  },
  async loadEquipmentstatus ({ commit }: { commit: Commit }): Promise<void> {
    // @ts-ignore
    commit('setEquipmentstatus', await this.$api.states.findAll())
  },
  async loadDevicetypes ({ commit }: { commit: Commit }): Promise<void> {
    // @ts-ignore
    commit('setDevicetypes', await this.$api.deviceTypes.findAll())
  },
  async loadPlatformtypes ({ commit }: { commit: Commit }): Promise<void> {
    // @ts-ignore
    commit('setPlatformtypes', await this.$api.platformTypes.findAll())
  },
  async loadPlatformGenericActionTypes ({ commit }: { commit: Commit }): Promise<void> { // TODO check api and maybe refactor
    commit('setPlatformGenericActionTypes', await this.$api.actionTypes.newSearchBuilder().onlyType(ACTION_TYPE_API_FILTER_PLATFORM).build().findMatchingAsList()
    )
  },
  async loadDeviceGenericActionTypes ({ commit }: { commit: Commit }): Promise<void> {
    commit('setDeviceGenericActionTypes', await this.$api.actionTypes.newSearchBuilder().onlyType(ACTION_TYPE_API_FILTER_DEVICE).build().findMatchingAsList())
  },
  async loadConfigurationGenericActionTypes ({ commit }: { commit: Commit }): Promise<void> {
    commit('setConfigurationGenericActionTypes', await this.$api.actionTypes.newSearchBuilder().onlyType(ACTION_TYPE_API_FILTER_CONFIGURATION).build().findMatchingAsList())
  },
  async loadCompartments ({ commit }: { commit: Commit }): Promise<void> {
    commit('setCompartments', await this.$api.compartments.findAll())
  },
  async loadSamplingMedia ({ commit }: { commit: Commit }): Promise<void> {
    commit('setSamplingMedia', await this.$api.samplingMedia.findAll())
  },
  async loadProperties ({ commit }: { commit: Commit }): Promise<void> {
    commit('setProperties', await this.$api.properties.findAll())
  },
  async loadUnits ({ commit }: { commit: Commit }): Promise<void> {
    commit('setUnits', await this.$api.units.findAll())
  },
  async loadMeasuredQuantityUnits ({ commit }: { commit: Commit }): Promise<void> {
    commit('setMeasuredQuantityUnits', await this.$api.measuredQuantityUnits.findAll())
  },
  async loadEpsgCodes ({ commit }: { commit: Commit }): Promise<void> {
    commit('setEpsgCodes', await this.$api.epsgCodes.findAll())
  },
  async loadElevationData ({ commit }: { commit: Commit }): Promise<void> {
    commit('setElevationData', await this.$api.elevationData.findAll())
  },
  async loadCvContactRoles ({ commit }: {commit: Commit }): Promise<void> {
    commit('setCvContactRoles', await this.$api.cvContactRoles.findAll())
  },
  async loadGlobalProvenances ({ commit }: { commit: Commit }): Promise<void> {
    commit('setGlobalProvenances', await this.$api.globalProvenances.findAll())
  },
  async loadAggregationtypes ({ commit }: { commit: Commit }): Promise<void> {
    commit('setAggregationtypes', await this.$api.aggregationTypes.findAll())
  },
  async loadActionCategories ({ commit }: { commit: Commit }): Promise<void> {
    commit('setActionCategories', await this.$api.actionCategories.findAll())
  },
  async loadSiteUsages ({ commit }: { commit: Commit }): Promise<void> {
    commit('setSiteUsages', await this.$api.siteUsages.findAll())
  },
  async loadSiteTypes ({ commit }: { commit: Commit }): Promise<void> {
    commit('setSiteTypes', await this.$api.siteTypes.findAll())
  },
  async loadCountries ({ commit }: { commit: Commit }): Promise<void> {
    commit('setCountries', await this.$api.countries.findAll())
  },
  async loadLicenses ({ commit }: { commit: Commit }): Promise<void> {
    commit('setLicenses', await this.$api.licenses.findAll())
  },
  async addDevicetype ({ commit, state }: {commit: Commit, state: VocabularyState }, { devicetype }: {devicetype: DeviceType }): Promise<DeviceType> {
    const newDevicetype = await this.$api.deviceTypes.add(devicetype)
    const devicetypes = [...state.devicetypes, newDevicetype]
    await commit('setDevicetypes', devicetypes)
    return newDevicetype
  },
  async addPlatformtype ({ commit, state }: {commit: Commit, state: VocabularyState }, { platformtype }: { platformtype: PlatformType }): Promise<PlatformType> {
    const newPlatformtype = await this.$api.platformTypes.add(platformtype)
    const platformtypes = [...state.platformtypes, newPlatformtype]
    await commit('setPlatformtypes', platformtypes)
    return newPlatformtype
  },
  async addManufacturer ({ commit, state }: {commit: Commit, state: VocabularyState }, { manufacturer }: { manufacturer: Manufacturer }): Promise<Manufacturer> {
    const newManufacturer = await this.$api.manufacturer.add(manufacturer)
    const manufacturers = [...state.manufacturers, newManufacturer]
    await commit('setManufacturers', manufacturers)
    return newManufacturer
  },
  async addEquipmentstatus ({ commit, state }: {commit: Commit, state: VocabularyState }, { status }: { status: Status }): Promise<Status> {
    const newStatus = await this.$api.states.add(status)
    const equipmentstatus = [...state.equipmentstatus, newStatus]
    await commit('setEquipmentstatus', equipmentstatus)
    return newStatus
  },
  async addCvContactRole ({ commit, state }: {commit: Commit, state: VocabularyState }, { contactRole }: { contactRole: CvContactRole }): Promise<CvContactRole> {
    const newContactRole = await this.$api.cvContactRoles.add(contactRole)
    const cvContactRoles = [...state.cvContactRoles, newContactRole]
    await commit('setCvContactRoles', cvContactRoles)
    return newContactRole
  },
  async addCompartment ({ commit, state }: {commit: Commit, state: VocabularyState }, { compartment }: { compartment: Compartment }): Promise<Compartment> {
    const newCompartment = await this.$api.compartments.add(compartment)
    const compartments = [...state.compartments, newCompartment]
    await commit('setCompartments', compartments)
    return newCompartment
  },
  async addSamplingMedia ({ commit, state }: {commit: Commit, state: VocabularyState}, { samplingMedium }: { samplingMedium: SamplingMedia}): Promise<SamplingMedia> {
    const newSamplingMedium = await this.$api.samplingMedia.add(samplingMedium)
    const samplingMedia = [...state.samplingMedia, newSamplingMedium]
    await commit('setSamplingMedia', samplingMedia)
    return samplingMedium
  },
  async addProperty ({ commit, state }: {commit: Commit, state: VocabularyState}, { property }: {property: Property}): Promise<Property> {
    const newProperty = await this.$api.properties.add(property)
    const properties = [...state.properties, newProperty]
    await commit('setProperties', properties)
    return newProperty
  },
  async addActiontype ({ commit, state }: { commit: Commit, state: VocabularyState}, { actiontype, actionCategoryTerm }: { actiontype: ActionType, actionCategoryTerm: ActionTypeApiFilterType}): Promise<ActionType> {
    const newActiontype = await this.$api.actionTypes.add(actiontype)
    if (actionCategoryTerm === ACTION_TYPE_API_FILTER_DEVICE) {
      const deviceGenericActionTypes = [...state.deviceGenericActionTypes, newActiontype]
      await commit('setDeviceGenericActionTypes', deviceGenericActionTypes)
    } else if (actionCategoryTerm === ACTION_TYPE_API_FILTER_PLATFORM) {
      const platformGenericActionTypes = [...state.platformGenericActionTypes, newActiontype]
      await commit('setPlatformGenericActionTypes', platformGenericActionTypes)
    } else if (actionCategoryTerm === ACTION_TYPE_API_FILTER_CONFIGURATION) {
      const configurationGenericActionTypes = [...state.configurationGenericActionTypes, newActiontype]
      await commit('setConfigurationGenericActionTypes', configurationGenericActionTypes)
    }
    return newActiontype
  },
  async addUnit ({ commit, state }: {commit: Commit, state: VocabularyState}, { unit }: {unit: Unit}): Promise<Unit> {
    const newUnit = await this.$api.units.add(unit)
    const units = [...state.units, newUnit]
    await commit('setUnits', units)
    return newUnit
  },
  async addMeasuredQuantityUnit ({ commit, state }: {commit: Commit, state: VocabularyState}, { measuredQuantityUnit }: {measuredQuantityUnit: MeasuredQuantityUnit}): Promise<MeasuredQuantityUnit> {
    const newMeasuredQuantityUnit = await this.$api.measuredQuantityUnits.add(measuredQuantityUnit)
    const measuredQuantityUnits = [...state.measuredQuantityUnits, newMeasuredQuantityUnit]
    await commit('setMeasuredQuantityUnits', measuredQuantityUnits)
    return newMeasuredQuantityUnit
  },
  async addSiteUsage ({ commit, state }: {commit: Commit, state: VocabularyState }, { siteUsage }: { siteUsage: SiteUsage }): Promise<SiteUsage> {
    const newSiteUsage = await this.$api.siteUsages.add(siteUsage)
    const siteUsages = [...state.siteUsages, newSiteUsage]
    await commit('setSiteUsages', siteUsages)
    return newSiteUsage
  },
  async addSiteType ({ commit, state }: {commit: Commit, state: VocabularyState }, { siteType }: { siteType: SiteType }): Promise<SiteType> {
    const newSiteType = await this.$api.siteTypes.add(siteType)
    const siteTypes = [...state.siteTypes, newSiteType]
    await commit('setSiteTypes', siteTypes)
    return newSiteType
  },
  async addAggregationType ({ commit, state }: {commit: Commit, state: VocabularyState }, { aggregationType }: { aggregationType: AggregationType}): Promise<AggregationType> {
    const newAggregationType = await this.$api.aggregationTypes.add(aggregationType)
    const aggregationTypes = [...state.aggregationtypes, newAggregationType]
    await commit('setAggregationtypes', aggregationTypes)
    return newAggregationType
  },
  async addLicense ({ commit, state }: {commit: Commit, state: VocabularyState}, { license }: { license: License}): Promise<License> {
    const newLicense = await this.$api.licenses.add(license)
    const licenses = [...state.licenses, newLicense]
    await commit('setLicenses', licenses)
    return newLicense
  }
}

const mutations = {
  setManufacturers (state: VocabularyState, manufacturers: Manufacturer[]) {
    state.manufacturers = manufacturers
  },
  setEquipmentstatus (state: VocabularyState, equipmentstatus: Status[]) {
    state.equipmentstatus = equipmentstatus
  },
  setDevicetypes (state: VocabularyState, devicetypes: DeviceType[]) {
    state.devicetypes = devicetypes
  },
  setPlatformtypes (state: VocabularyState, platformtypes: PlatformType[]) {
    state.platformtypes = platformtypes
  },
  setPlatformGenericActionTypes (state: VocabularyState, platformGenericActionTypes: ActionType[]) {
    state.platformGenericActionTypes = platformGenericActionTypes
  },
  setDeviceGenericActionTypes (state: VocabularyState, deviceGenericActionTypes: ActionType[]) {
    state.deviceGenericActionTypes = deviceGenericActionTypes
  },
  setConfigurationGenericActionTypes (state: VocabularyState, configurationGenericActionTypes: ActionType[]) {
    state.configurationGenericActionTypes = configurationGenericActionTypes
  },
  setCompartments (state: VocabularyState, compartments: Compartment[]) {
    state.compartments = compartments
  },
  setSamplingMedia (state: VocabularyState, samplingMedia: SamplingMedia[]) {
    state.samplingMedia = samplingMedia
  },
  setProperties (state: VocabularyState, properties: Property[]) {
    state.properties = properties
  },
  setUnits (state: VocabularyState, units: Unit[]) {
    state.units = units
  },
  setMeasuredQuantityUnits (state: VocabularyState, measuredQuantityUnits: MeasuredQuantityUnit[]) {
    state.measuredQuantityUnits = measuredQuantityUnits
  },
  setEpsgCodes (state: VocabularyState, epsgCodes: EpsgCode[]) {
    state.epsgCodes = epsgCodes
  },
  setElevationData (state: VocabularyState, elevationData: ElevationDatum[]) {
    state.elevationData = elevationData
  },
  setCvContactRoles (state: VocabularyState, cvContactRoles: CvContactRole[]) {
    state.cvContactRoles = cvContactRoles
  },
  setGlobalProvenances (state: VocabularyState, globalProvenances: GlobalProvenance[]) {
    state.globalProvenances = globalProvenances
  },
  setAggregationtypes (state: VocabularyState, aggregationtypes: AggregationType[]) {
    state.aggregationtypes = aggregationtypes
  },
  setActionCategories (state: VocabularyState, actionCategories: ActionCategory[]) {
    state.actionCategories = actionCategories
  },
  setSiteUsages (state: VocabularyState, siteUsages: SiteUsage[]) {
    state.siteUsages = siteUsages
  },
  setSiteTypes (state: VocabularyState, siteTypes: SiteType[]) {
    state.siteTypes = siteTypes
  },
  setCountries (state: VocabularyState, countries: Country[]) {
    state.countries = countries
  },
  setLicenses (state: VocabularyState, licenses: License[]) {
    state.licenses = licenses
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
