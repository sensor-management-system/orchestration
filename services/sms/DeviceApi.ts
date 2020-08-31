import { AxiosInstance, Method } from 'axios'

import Device from '@/models/Device'
import DeviceType from '@/models/DeviceType'
import Manufacturer from '@/models/Manufacturer'
import Status from '@/models/Status'

import { IFlaskJSONAPIFilter } from '@/utils/JSONApiInterfaces'

import {
  IPaginationLoader, FilteredPaginationedLoader
} from '@/utils/PaginatedLoader'
import { DeviceProperty } from '~/models/DeviceProperty'

export default class DeviceApi {
  private axiosApi: AxiosInstance

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
  }

  findById (id: string): Promise<Device> {
    // TODO: Think about also including the contacts
    // with ?include=contacts
    return this.axiosApi.get(id).then((rawResponse) => {
      const entry = rawResponse.data.data
      return serverResponseToEntity(entry)
    })
  }

  deleteById (id: number) : Promise<void> {
    return this.axiosApi.delete<string, void>(String(id))
  }

  save (device: Device) {
    // TODO: consistent camelCase

    const properties = []

    for (const property of device.properties) {
      const propertyToSave: any = {}
      if (property.id != null) {
        propertyToSave.id = property.id
      }

      propertyToSave.measuringRangeMin = property.measuringRange.min
      propertyToSave.measuringRangeMax = property.measuringRange.max
      propertyToSave.failureValue = property.failureValue
      propertyToSave.accuracy = property.accuracy
      propertyToSave.label = property.label
      propertyToSave.unitUri = property.unitUri
      propertyToSave.unitName = property.unitName
      propertyToSave.compartmentUri = property.compartmentUri
      propertyToSave.compartmentName = property.compartmentName
      propertyToSave.propertyUri = property.propertyUri
      propertyToSave.propertyName = property.propertyName
      propertyToSave.samplingMediaUri = property.samplingMediaUri
      propertyToSave.samplingMediaName = property.samplingMediaName

      properties.push(propertyToSave)
    }

    const data: any = {
      type: 'device',
      attributes: {
        description: device.description,
        shortName: device.shortName,
        longName: device.longName,
        serialNumber: device.serialNumber,
        manufacturerUri: device.manufacturerUri,
        manufacturerName: device.manufacturerName,
        deviceTypeUri: device.deviceTypeUri,
        deviceTypeName: device.deviceTypeName,
        statusUri: device.statusUri,
        statusName: device.statusName,
        model: device.model,
        dualUse: device.dualUse,
        inventoryNumber: device.inventoryNumber,
        persistentIdentifier: device.persistentIdentifier === '' ? null : device.persistentIdentifier,
        website: device.website,
        createdAt: device.createdAt,
        updatedAt: device.updatedAt,
        // TODO
        // createdBy: device.createdBy,
        // updatedBy: device.updatedBy,

        // TODO
        customfields: [],
        properties,
        attachments: []

        /*
        customFields: [
          {
            key: 'key1',
            value: 'value1'
          },
          {
            key: 'key2',
            value: 'value2
          }
        ]
        */
      }

      /*
      relationships: {
        events: {

        },
        contacts: {
          data: [
            {
              type: 'contact',
              id: 1,
            },
            {
              type: 'contact',
              id: 2
            }
          ]
        }

      }
      */
    }
    let method: Method = 'patch'
    let url = ''

    if (device.id === null) {
      // new -> post
      method = 'post'
    } else {
      // old -> patch
      data.id = device.id
      url = String(device.id)
    }

    // TODO: links for contacts
    return this.axiosApi.request({
      url,
      method,
      data: {
        data
      }
    }).then((serverAnswer) => {
      return serverResponseToEntity(serverAnswer.data.data)
    })
  }

  newSearchBuilder (): DeviceSearchBuilder {
    return new DeviceSearchBuilder(this.axiosApi)
  }
}

export class DeviceSearchBuilder {
  private axiosApi: AxiosInstance
  private clientSideFilterFunc: (device: Device) => boolean
  private serverSideFilterSettings: IFlaskJSONAPIFilter[] = []

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
    this.clientSideFilterFunc = (_d: Device) => true
  }

  withTextInName (text: string | null) {
    if (text) {
      const ilikeValue = '%' + text + '%'
      const fieldsToSearchIn = [
        'short_name',
        'long_name'
        // here we can add description
        // as well
        // --> if so, also change the method name here
      ]

      const filter: IFlaskJSONAPIFilter[] = []
      for (const field of fieldsToSearchIn) {
        filter.push({
          name: field,
          op: 'ilike',
          val: ilikeValue
        })
      }

      this.serverSideFilterSettings.push({
        or: filter
      })
    }
    return this
  }

  withOneMachtingManufacturerOf (manufacturers: Manufacturer[]) {
    if (manufacturers.length > 0) {
      this.serverSideFilterSettings.push({
        // TODO: change to manufacturer_name
        // and extend with manufacturer uri as well
        name: 'manufacturer',
        op: 'in_',
        val: manufacturers.map((m: Manufacturer) => m.name)
      })
    }
    return this
  }

  withOneMatchingStatusOf (states: Status[]) {
    if (states.length > 0) {
      // TODO: at the moment there is no status field
      // with could be used to read the data from
      // --> once this is there, we want to add the
      // serverside filtering is we do with the manufacturers
      const oldFilterFunc = this.clientSideFilterFunc
      this.clientSideFilterFunc = (device: Device) : boolean => {
        return oldFilterFunc(device) && (
          states.findIndex(s => s.uri === device.statusUri) > -1
        )
      }
    }
    return this
  }

  withOneMatchingDeviceTypeOf (types: DeviceType[]) {
    if (types.length > 0) {
      this.serverSideFilterSettings.push({
        // TODO: change to devicetype_uri
        // and extend with platformtype name as well
        name: 'type',
        op: 'in_',
        val: types.map((t: DeviceType) => t.uri)
      })
    }
    return this
  }

  build (): DeviceSearcher {
    return new DeviceSearcher(
      this.axiosApi,
      this.clientSideFilterFunc,
      this.serverSideFilterSettings
    )
  }
}

export class DeviceSearcher {
  private axiosApi: AxiosInstance
  private clientSideFilterFunc: (device: Device) => boolean
  private serverSideFilterSettings: IFlaskJSONAPIFilter[]

  constructor (
    axiosApi: AxiosInstance,
    clientSideFilterFunc: (device: Device) => boolean,
    serverSideFilterSettings: IFlaskJSONAPIFilter[]
  ) {
    this.axiosApi = axiosApi
    this.clientSideFilterFunc = clientSideFilterFunc
    this.serverSideFilterSettings = serverSideFilterSettings
  }

  private get commonParams (): any {
    return {
      filter: JSON.stringify(this.serverSideFilterSettings),
      // yes, it must be snake_case as the flask & sqlalchemy implementation
      // use this casing (only the json:api on top of that uses camelCase)
      sort: 'short_name'
    }
  }

  findMatchingAsList (): Promise<Device[]> {
    return this.axiosApi.get(
      '',
      {
        params: {
          'page[size]': 100000,
          ...this.commonParams
        }
      }
    ).then((rawResponse: any) => {
      const rawData = rawResponse.data
      const result: Device[] = []

      for (const entry of rawData.data) {
        const device = serverResponseToEntity(entry)
        if (this.clientSideFilterFunc(device)) {
          result.push(device)
        }
      }
      return result
    })
  }

  findMatchingAsPaginationLoader (pageSize: number): Promise<IPaginationLoader<Device>> {
    const loaderPromise: Promise<IPaginationLoader<Device>> = this.findAllOnPage(1, pageSize)
    return loaderPromise.then((loader) => {
      return new FilteredPaginationedLoader<Device>(loader, this.clientSideFilterFunc)
    })
  }

  private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Device>> {
    return this.axiosApi.get(
      '',
      {
        params: {
          'page[size]': pageSize,
          'page[number]': page,
          ...this.commonParams
        }
      }
    ).then((rawResponse) => {
      const rawData = rawResponse.data
      const result: Device[] = []
      for (const entry of rawData.data) {
        // client side filtering will not be done here
        // (but in the FilteredPaginationedLoader)
        // so that we know if we still have elements here
        // there may be others to load as well
        result.push(serverResponseToEntity(entry))
      }

      let funToLoadNext = null
      if (result.length > 0) {
        funToLoadNext = () => this.findAllOnPage(page + 1, pageSize)
      }

      return {
        elements: result,
        funToLoadNext
      }
    })
  }
}

export function serverResponseToEntity (entry: any) : Device {
  const result: Device = new Device()

  const attributes = entry.attributes

  result.id = entry.id

  result.description = attributes.description || ''
  result.shortName = attributes.shortName || ''
  result.longName = attributes.longName || ''
  result.serialNumber = attributes.serialNumber || ''
  result.manufacturerUri = attributes.manufacturerUri || ''
  result.manufacturerName = attributes.manufacturerName || ''
  result.deviceTypeUri = attributes.deviceTypeUri || ''
  result.deviceTypeName = attributes.deviceTypeName || ''
  result.statusUri = attributes.statusUri || ''
  result.statusName = attributes.statusName || ''
  result.model = attributes.model || ''
  result.dualUse = attributes.dualUse || false
  result.inventoryNumber = attributes.inventoryNumber || ''
  result.persistentIdentifier = attributes.persistentIdentifier || ''
  result.website = attributes.website || ''
  result.createdAt = attributes.createdAt
  result.updatedAt = attributes.updatedAt
  // result.createdBy = attributes.createdBy
  // result.updatedBy = attributes.updatedBy
  result.customFields = []
  // result.events = []
  result.attachments = []
  result.contacts = []
  result.properties = []

  for (const propertyFromServer of attributes.properties) {
    const property = new DeviceProperty()
    property.id = Number.parseInt(propertyFromServer.id)
    property.measuringRange.min = propertyFromServer.measuringRangeMin
    property.measuringRange.max = propertyFromServer.measuringRangeMax
    property.failureValue = propertyFromServer.failureValue
    property.accuracy = propertyFromServer.accuracy
    property.label = propertyFromServer.label || ''
    property.unitUri = propertyFromServer.unitUri || ''
    property.unitName = propertyFromServer.unitName || ''
    property.compartmentUri = propertyFromServer.compartmentUri || ''
    property.compartmentName = propertyFromServer.compartmentName || ''
    property.propertyUri = propertyFromServer.propertyUri || ''
    property.propertyName = propertyFromServer.propertyName || ''
    property.samplingMediaUri = propertyFromServer.samplingMediaUri || ''
    property.samplingMediaName = propertyFromServer.samplingMediaName || ''

    result.properties.push(propertyFromServer)
  }

  return result
}
