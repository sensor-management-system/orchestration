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
import { Commit } from 'vuex/types'
import { Manufacturer } from '@/models/Manufacturer'
import { Status } from '@/models/Status'
import { PlatformType } from '@/models/PlatformType'
import { DeviceType } from '@/models/DeviceType'
import { ActionType } from '@/models/ActionType'
import { ACTION_TYPE_API_FILTER_DEVICE, ACTION_TYPE_API_FILTER_PLATFORM } from '@/services/cv/ActionTypeApi'
import { Compartment } from '@/models/Compartment'
import { SamplingMedia } from '@/models/SamplingMedia'
import { Property } from '@/models/Property'
import { Unit } from '@/models/Unit'
import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'

const KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE = 'software_update'
const KIND_OF_ACTION_TYPE_GENERIC_PLATFORM_ACTION = 'generic_platform_action'
const KIND_OF_ACTION_TYPE_GENERIC_DEVICE_ACTION = 'generic_device_action'
const KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION = 'device_calibration'

interface vocabularyState {
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
  measuredQuantityUnits: MeasuredQuantityUnit[]
}

const state = {
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
  measuredQuantityUnits: []
}

const getters = {
  getPlatformTypeByUri: (state: vocabularyState) => (uri: string): PlatformType | undefined => {
    return state.platformtypes.find((platformType: PlatformType) => {
      return platformType.uri === uri
    })
  },
  getDeviceTypeByUri: (state: vocabularyState) => (uri: string): DeviceType | undefined => {
    return state.devicetypes.find((deviceType: DeviceType) => {
      return deviceType.uri === uri
    })
  },
  getEquipmentstatusByUri: (state: vocabularyState) => (uri: string): Status | undefined => {
    return state.equipmentstatus.find((equipmentstatus: Status) => {
      return equipmentstatus.uri === uri
    })
  },
  getManufacturerByUri: (state: vocabularyState) => (uri: string): Manufacturer | undefined => {
    return state.manufacturers.find((manufacturer: Manufacturer) => {
      return manufacturer.uri === uri
    })
  },
  platformActionTypeItems: (state: vocabularyState) => {
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
  deviceActionTypeItems: (state: vocabularyState) => {
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

const actions = {
  async loadManufacturers ({ commit }: { commit: Commit }) {
    // @ts-ignore
    commit('setManufacturers', await this.$api.manufacturer.findAll())
  },
  async loadEquipmentstatus ({ commit }: { commit: Commit }) {
    // @ts-ignore
    commit('setEquipmentstatus', await this.$api.states.findAll())
  },
  async loadDevicetypes ({ commit }: { commit: Commit }) {
    // @ts-ignore
    commit('setDevicetypes', await this.$api.deviceTypes.findAll())
  },
  async loadPlatformtypes ({ commit }: { commit: Commit }) {
    // @ts-ignore
    commit('setPlatformtypes', await this.$api.platformTypes.findAll())
  },
  async loadPlatformGenericActionTypes ({ commit }: { commit: Commit }) { // TODO check api and maybe refactor
    commit('setPlatformGenericActionTypes', await this.$api.actionTypes.newSearchBuilder().onlyType(ACTION_TYPE_API_FILTER_PLATFORM).build().findMatchingAsList()
    )
  },
  async loadDeviceGenericActionTypes ({ commit }: { commit: Commit }) {
    commit('setDeviceGenericActionTypes', await this.$api.actionTypes.newSearchBuilder().onlyType(ACTION_TYPE_API_FILTER_DEVICE).build().findMatchingAsList())
  },
  async loadCompartments ({ commit }: { commit: Commit }) {
    commit('setCompartments', await this.$api.compartments.findAllPaginated())
  },
  async loadSamplingMedia ({ commit }: { commit: Commit }) {
    commit('setSamplingMedia', await this.$api.samplingMedia.findAllPaginated())
  },
  async loadProperties ({ commit }: { commit: Commit }) {
    commit('setProperties', await this.$api.properties.findAllPaginated())
  },
  async loadUnits ({ commit }: { commit: Commit }) {
    commit('setUnits', await this.$api.units.findAllPaginated())
  },
  async loadMeasuredQuantityUnits ({ commit }: { commit: Commit }) {
    commit('setMeasuredQuantityUnits', await this.$api.measuredQuantityUnits.findAllPaginated())
  }
}

const mutations = {
  setManufacturers (state: vocabularyState, manufacturers: Manufacturer[]) {
    state.manufacturers = manufacturers
  },
  setEquipmentstatus (state: vocabularyState, equipmentstatus: Status[]) {
    state.equipmentstatus = equipmentstatus
  },
  setDevicetypes (state: vocabularyState, devicetypes: DeviceType[]) {
    state.devicetypes = devicetypes
  },
  setPlatformtypes (state: vocabularyState, platformtypes: PlatformType[]) {
    state.platformtypes = platformtypes
  },
  setPlatformGenericActionTypes (state: vocabularyState, platformGenericActionTypes: ActionType[]) {
    state.platformGenericActionTypes = platformGenericActionTypes
  },
  setDeviceGenericActionTypes (state: vocabularyState, deviceGenericACtionTypes: ActionType[]) {
    state.deviceGenericActionTypes = deviceGenericACtionTypes
  },
  setCompartments (state: vocabularyState, compartments: Compartment[]) {
    state.compartments = compartments
  },
  setSamplingMedia (state: vocabularyState, samplingMedia: SamplingMedia[]) {
    state.samplingMedia = samplingMedia
  },
  setProperties (state: vocabularyState, properties: Property[]) {
    state.properties = properties
  },
  setUnits (state: vocabularyState, units: Unit[]) {
    state.units = units
  },
  setMeasuredQuantityUnits (state: vocabularyState, measuredQuantityUnits: MeasuredQuantityUnit[]) {
    state.measuredQuantityUnits = measuredQuantityUnits
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
