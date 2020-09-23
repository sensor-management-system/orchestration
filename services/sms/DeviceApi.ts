import { AxiosInstance, Method } from 'axios'

import Contact from '@/models/Contact'
import Device from '@/models/Device'
import DeviceType from '@/models/DeviceType'
import Manufacturer from '@/models/Manufacturer'
import Status from '@/models/Status'
import { DeviceProperty } from '@/models/DeviceProperty'
import { MeasuringRange } from '@/models/MeasuringRange'
import { CustomTextField } from '@/models/CustomTextField'
import { Attachment } from '@/models/Attachment'

import { IFlaskJSONAPIFilter } from '@/utils/JSONApiInterfaces'

import { serverResponseToEntity as serverResponseToContact } from '@/services/sms/ContactApi'

import {
  IPaginationLoader, FilteredPaginationedLoader
} from '@/utils/PaginatedLoader'

export default class DeviceApi {
  private axiosApi: AxiosInstance

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
  }

  findById (id: string): Promise<Device> {
    return this.axiosApi.get(id, {
      params: {
        include: 'contacts'
      }
    }).then((rawResponse) => {
      const rawData = rawResponse.data
      const entry = rawData.data
      const included: any[] = rawData.included || []
      return serverResponseToEntity(entry, included)
    })
  }

  deleteById (id: string) : Promise<void> {
    return this.axiosApi.delete<string, void>(id)
  }

  save (device: Device) {
    const properties = []

    for (const property of device.properties) {
      const propertyToSave: any = {}
      if (property.id != null) {
        // currently it seems that the id is always set to a higher value
        // I can set it to 8, but it will be saved with a new id (9)
        // there is already an issue for the backend, so hopefully it will be fixed there
        propertyToSave.id = property.id
      }

      propertyToSave.measuring_range_min = property.measuringRange.min
      propertyToSave.measuring_range_max = property.measuringRange.max
      propertyToSave.failure_value = property.failureValue
      propertyToSave.accuracy = property.accuracy
      propertyToSave.label = property.label
      propertyToSave.unit_uri = property.unitUri
      propertyToSave.unit_name = property.unitName
      propertyToSave.compartment_uri = property.compartmentUri
      propertyToSave.compartment_name = property.compartmentName
      propertyToSave.property_uri = property.propertyUri
      propertyToSave.property_name = property.propertyName
      propertyToSave.sampling_media_uri = property.samplingMediaUri
      propertyToSave.sampling_media_name = property.samplingMediaName

      properties.push(propertyToSave)
    }

    const customfields = []
    for (const customField of device.customFields) {
      const customFieldToSave: any = {}

      if (customField.id != null) {
        customFieldToSave.id = customField.id
      }

      customFieldToSave.key = customField.key
      customFieldToSave.value = customField.value

      customfields.push(customFieldToSave)
    }

    const attachments = []
    for (const attachment of device.attachments) {
      const attachmentToSave: any = {}
      if (attachment.id != null) {
        attachmentToSave.id = attachment.id
      }
      attachmentToSave.label = attachment.label
      attachmentToSave.url = attachment.url

      attachments.push(attachmentToSave)
    }

    const contacts = []
    for (const contact of device.contacts) {
      contacts.push({
        id: contact.id,
        type: 'contact'
      })
    }

    const data: any = {
      type: 'device',
      attributes: {
        description: device.description,
        short_name: device.shortName,
        long_name: device.longName,
        serial_number: device.serialNumber,
        inventory_number: device.inventoryNumber,
        manufacturer_uri: device.manufacturerUri,
        manufacturer_name: device.manufacturerName,
        device_type_uri: device.deviceTypeUri,
        device_type_name: device.deviceTypeName,
        status_uri: device.statusUri,
        status_name: device.statusName,
        model: device.model,
        persistent_identifier: device.persistentIdentifier === '' ? null : device.persistentIdentifier,
        website: device.website,
        dual_use: device.dualUse,
        // those two time slots are set by the db, no matter what we deliver here
        created_at: device.createdAt,
        updated_at: device.updatedAt,
        // TODO
        // created_by: device.createdBy,
        // updated_by: device.updatedBy,

        customfields,
        properties,
        attachments
      },
      relationships: {
        contacts: {
          data: contacts
        }
        // TODO: events
      }
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

    return this.axiosApi.request({
      url,
      method,
      data: {
        data
      }
    }).then((serverAnswer) => {
      // the server answer doesn't include the contacts
      // so we will reload from the database
      return this.findById(serverAnswer.data.data.id)
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
        or: [
          {
            name: 'manufacturer_name',
            op: 'in_',
            val: manufacturers.map((m: Manufacturer) => m.name)
          },
          {
            name: 'manufacturer_uri',
            op: 'in_',
            val: manufacturers.map((m: Manufacturer) => m.uri)
          }
        ]
      })
    }
    return this
  }

  withOneMatchingStatusOf (states: Status[]) {
    if (states.length > 0) {
      this.serverSideFilterSettings.push({
        or: [
          {
            name: 'status_name',
            op: 'in_',
            val: states.map((s: Status) => s.name)
          },
          {
            name: 'status_uri',
            op: 'in_',
            val: states.map((s: Status) => s.uri)
          }
        ]
      })
    }
    return this
  }

  withOneMatchingDeviceTypeOf (types: DeviceType[]) {
    if (types.length > 0) {
      this.serverSideFilterSettings.push({
        or: [
          {
            name: 'device_type_name',
            op: 'in_',
            val: types.map((t: DeviceType) => t.name)
          },
          {
            name: 'device_type_uri',
            op: 'in_',
            val: types.map((t: DeviceType) => t.uri)
          }
        ]
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
      const included: any[] = rawData.included || []

      for (const entry of rawData.data) {
        const device = serverResponseToEntity(entry, included)
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
      const included: any[] = rawData.included || []
      for (const entry of rawData.data) {
        // client side filtering will not be done here
        // (but in the FilteredPaginationedLoader)
        // so that we know if we still have elements here
        // there may be others to load as well
        result.push(serverResponseToEntity(entry, included))
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

export function serverResponseToEntity (entry: any, included: any[]) : Device {
  const result: Device = new Device()

  const attributes = entry.attributes
  const relationships = entry.relationships

  result.id = entry.id

  result.description = attributes.description || ''
  result.shortName = attributes.short_name || ''
  result.longName = attributes.long_name || ''
  result.serialNumber = attributes.serial_number || ''
  result.manufacturerUri = attributes.manufacturer_uri || ''
  result.manufacturerName = attributes.manufacturer_name || ''
  result.deviceTypeUri = attributes.device_type_uri || ''
  result.deviceTypeName = attributes.device_type_name || ''
  result.statusUri = attributes.status_uri || ''
  result.statusName = attributes.status_name || ''
  result.model = attributes.model || ''
  result.dualUse = attributes.dual_use || false
  result.inventoryNumber = attributes.inventory_number || ''
  result.persistentIdentifier = attributes.persistent_identifier || ''
  result.website = attributes.website || ''
  result.createdAt = attributes.created_at
  result.updatedAt = attributes.updated_at
  // TODO
  // result.createdBy = attributes.created_by
  // result.updatedBy = attributes.updated_by
  // result.events = []
  result.attachments = []
  result.contacts = []
  const properties: DeviceProperty[] = []

  for (const propertyFromServer of attributes.properties) {
    const property = new DeviceProperty()
    property.id = propertyFromServer.id
    property.measuringRange = new MeasuringRange(
      propertyFromServer.measuring_range_min,
      propertyFromServer.measuring_range_max
    )
    property.failureValue = propertyFromServer.failure_value
    property.accuracy = propertyFromServer.accuracy
    property.label = propertyFromServer.label || ''
    property.unitUri = propertyFromServer.unit_uri || ''
    property.unitName = propertyFromServer.unit_name || ''
    property.compartmentUri = propertyFromServer.compartment_uri || ''
    property.compartmentName = propertyFromServer.compartment_name || ''
    property.propertyUri = propertyFromServer.property_uri || ''
    property.propertyName = propertyFromServer.property_name || ''
    property.samplingMediaUri = propertyFromServer.sampling_media_uri || ''
    property.samplingMediaName = propertyFromServer.sampling_media_name || ''

    properties.push(property)
  }

  result.properties = properties

  const customFields: CustomTextField[] = []

  for (const customFieldFromServer of attributes.customfields) {
    const customField = new CustomTextField()
    customField.id = customFieldFromServer.id
    customField.key = customFieldFromServer.key || ''
    customField.value = customFieldFromServer.value || ''

    customFields.push(customField)
  }

  result.customFields = customFields

  const attachments: Attachment[] = []

  for (const attachmentFromServer of attributes.attachments) {
    const attachment = new Attachment()
    attachment.id = attachmentFromServer.id
    attachment.label = attachmentFromServer.label || ''
    attachment.url = attachmentFromServer.url || ''

    attachments.push(attachment)
  }

  result.attachments = attachments

  const contactIds = []
  if (relationships.contacts && relationships.contacts.data && relationships.contacts.data.length > 0) {
    for (const relationShipContactData of relationships.contacts.data) {
      const contactId = relationShipContactData.id
      contactIds.push(contactId)
    }
  }

  const possibleContacts: {[key: string]: Contact} = {}
  if (included && included.length > 0) {
    for (const includedEntry of included) {
      if (includedEntry.type === 'contact') {
        const contactId = includedEntry.id
        if (contactIds.includes(contactId)) {
          const contact = serverResponseToContact(includedEntry)
          possibleContacts[contactId] = contact
        }
      }
    }
  }

  const contacts = []

  for (const contactId of contactIds) {
    if (possibleContacts[contactId]) {
      contacts.push(possibleContacts[contactId])
    } else {
      const contact = new Contact()
      contact.id = contactId
      contacts.push(contact)
    }
  }

  result.contacts = contacts

  return result
}
