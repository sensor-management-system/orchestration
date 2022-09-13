/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
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

import { ACTION_TYPE_API_FILTER_DEVICE, ACTION_TYPE_API_FILTER_PLATFORM } from '@/services/cv/ActionTypeApi'

const KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE = 'software_update'
const KIND_OF_ACTION_TYPE_GENERIC_PLATFORM_ACTION = 'generic_platform_action'
const KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION = 'generic_device_action'
const KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION = 'device_calibration'

export interface VocabularyState {
  manufacturers: Manufacturer[]
  equipmentstatus: Status[]
  devicetypes: DeviceType[]
  platformtypes: PlatformType[],
  platformGenericActionTypes: ActionType[],
  deviceGenericActionTypes: ActionType[],
  compartments: Compartment[],
  samplingMedia: SamplingMedia[],
  properties: Property[],
  units: Unit[],
  measuredQuantityUnits: MeasuredQuantityUnit[],
  epsgCodes: EpsgCode[],
  elevationData: ElevationDatum[],
  cvContactRoles: CvContactRole[],
}

const state = (): VocabularyState => ({
  manufacturers: [],
  equipmentstatus: [],
  devicetypes: [],
  platformtypes: [],
  platformGenericActionTypes: [],
  deviceGenericActionTypes: [],
  compartments: [],
  samplingMedia: [],
  properties: [],
  units: [],
  measuredQuantityUnits: [],
  epsgCodes: [],
  elevationData: [],
  cvContactRoles: []
})

export type ActionTypeItem = { id: string, name: string, uri: string, kind: string }
export type GetPlatformTypeByUriGetter = (uri: string) => PlatformType | undefined
export type GetDeviceTypeByUriGetter = (uri: string) => DeviceType | undefined
export type GetEquipmentstatusByUriGetter = (uri: string) => Status | undefined
export type GetManufacturerByUriGetter = (uri: string) => Manufacturer | undefined
export type PlatformActionTypeItemsGetter = ActionTypeItem[]
export type DeviceActionTypeItemsGetter = ActionTypeItem[]

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
  platformActionTypeItems: (state: VocabularyState) => {
    return [
      {
        id: 'software_update',
        name: 'Software Update',
        uri: '',
        kind: KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
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
      ...state.deviceGenericActionTypes.map((actionType) => {
        return {
          id: actionType.id,
          name: actionType.name,
          uri: actionType.uri,
          kind: KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION
        }
      })
    ].sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()))
  }
}

export type LoadManufacturersAction = () => Promise<void>
export type LoadEquipmentstatusAction = () => Promise<void>
export type LoadDevicetypesAction = () => Promise<void>
export type LoadPlatformtypesAction = () => Promise<void>
export type LoadPlatformGenericActionTypesAction = () => Promise<void>
export type LoadDeviceGenericActionTypesAction = () => Promise<void>
export type LoadCompartmentsAction = () => Promise<void>
export type LoadSamplingMediaAction = () => Promise<void>
export type LoadPropertiesAction = () => Promise<void>
export type LoadUnitsAction = () => Promise<void>
export type LoadMeasuredQuantityUnitsAction = () => Promise<void>
export type LoadEpsgCodesAction = () => Promise<void>
export type LoadElevationDataAction = () => Promise<void>
export type LoadCvContactRolesAction = () => Promise<void>

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
  setDeviceGenericActionTypes (state: VocabularyState, deviceGenericACtionTypes: ActionType[]) {
    state.deviceGenericActionTypes = deviceGenericACtionTypes
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
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
