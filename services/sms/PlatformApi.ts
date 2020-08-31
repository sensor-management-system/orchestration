import { AxiosInstance, Method } from 'axios'

import Platform from '@/models/Platform'
import PlatformType from '@/models/PlatformType'
import { Attachment } from '@/models/Attachment'
import Manufacturer from '@/models/Manufacturer'
import Status from '@/models/Status'

import { IFlaskJSONAPIFilter } from '@/utils/JSONApiInterfaces'

import {
  IPaginationLoader, FilteredPaginationedLoader
} from '@/utils/PaginatedLoader'

import { serverResponseToEntity as serverResponseToContact } from '@/services/sms/ContactApi'
import Contact from '~/models/Contact'

export default class PlatformApi {
  private axiosApi: AxiosInstance

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
  }

  findById (id: string): Promise<Platform> {
    // TODO: Think about also including the contacts
    // with ?include=contacts
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

  deleteById (id: number): Promise<void> {
    return this.axiosApi.delete<string, void>(String(id))
  }

  save (platform: Platform): Promise<Platform> {
    const attachments = []

    for (const attachment of platform.attachments) {
      const attachmentToSave: any = {}
      if (attachment.id != null) {
        attachmentToSave.id = attachment.id
      }
      attachmentToSave.label = attachment.label
      attachmentToSave.url = attachment.url

      attachments.push(attachmentToSave)
    }

    const contacts = []
    for (const contact of platform.contacts) {
      contacts.push({
        id: contact.id,
        type: 'contact'
      })
    }

    const data: any = {
      type: 'platform',
      attributes: {
        description: platform.description,
        short_name: platform.shortName,
        long_name: platform.longName,
        manufacturer_uri: platform.manufacturerUri,
        manufacturer_name: platform.manufacturerName,
        model: platform.model,
        platform_type_uri: platform.platformTypeUri,
        platform_type_name: platform.platformTypeName,
        status_uri: platform.statusUri,
        status_name: platform.statusName,
        website: platform.website,
        created_at: platform.createdAt,
        updated_at: platform.updatedAt,
        // created_by: platform.createdBy,
        // updated_by: platform.updatedBy,
        inventory_number: platform.inventoryNumber,
        serial_number: platform.serialNumber,
        persistent_identifier: platform.persistentIdentifier === '' ? null : platform.persistentIdentifier,
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

    if (platform.id === null) {
      // new -> post
      method = 'post'
    } else {
      // old -> patch
      data.id = platform.id
      url = String(platform.id)
    }

    // TODO: links for contacts
    return this.axiosApi.request({
      url,
      method,
      data: {
        data
      }
    }).then((serverAnswer) => {
      return this.findById(serverAnswer.data.data.id)
    })
  }

  newSearchBuilder (): PlatformSearchBuilder {
    return new PlatformSearchBuilder(this.axiosApi)
  }
}

export class PlatformSearchBuilder {
  private axiosApi: AxiosInstance
  private clientSideFilterFunc: (platform: Platform) => boolean
  private serverSideFilterSettings: IFlaskJSONAPIFilter[] = []

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
    this.clientSideFilterFunc = (_p: Platform) => true
  }

  withTextInName (text: string | null) : PlatformSearchBuilder {
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

  withOneMatchingManufacturerOf (manufacturers: Manufacturer[]): PlatformSearchBuilder {
    if (manufacturers.length > 0) {
      this.serverSideFilterSettings.push({
        // TODO: change to manufacturer_uri
        // and extend with manufacturer name as well
        name: 'manufacturer_uri',
        op: 'in_',
        val: manufacturers.map((m: Manufacturer) => m.uri)
      })
    }
    return this
  }

  withOneMatchingStatusOf (states: Status[]): PlatformSearchBuilder {
    if (states.length > 0) {
      // TODO: at the moment there is no status field
      // with could be used to read the data from
      // --> once this is there, we want to add the
      // serverside filtering is we do with the manufacturers
      const oldFilterFunc = this.clientSideFilterFunc
      this.clientSideFilterFunc = (platform: Platform) : boolean => {
        return oldFilterFunc(platform) && (
          states.findIndex(s => s.uri === platform.statusUri) > -1
        )
      }
    }
    return this
  }

  withOneMatchingPlatformTypeOf (types: PlatformType[]): PlatformSearchBuilder {
    if (types.length > 0) {
      this.serverSideFilterSettings.push({
        // TODO: change to platformtype_uri
        // and extend with platformtype name as well
        name: 'platform_type_uri',
        op: 'in_',
        val: types.map((t: PlatformType) => t.uri)
      })
    }
    return this
  }

  build (): PlatformSearcher {
    return new PlatformSearcher(
      this.axiosApi,
      this.clientSideFilterFunc,
      this.serverSideFilterSettings
    )
  }
}

export class PlatformSearcher {
  private axiosApi: AxiosInstance
  private clientSideFilterFunc: (platform: Platform) => boolean
  private serverSideFilterSettings: IFlaskJSONAPIFilter[]

  constructor (
    axiosApi: AxiosInstance,
    clientSideFilterFunc: (platform: Platform) => boolean,
    serverSideFilterSetting: IFlaskJSONAPIFilter[]
  ) {
    this.axiosApi = axiosApi
    this.clientSideFilterFunc = clientSideFilterFunc
    this.serverSideFilterSettings = serverSideFilterSetting
  }

  private get commonParams (): any {
    return {
      filter: JSON.stringify(this.serverSideFilterSettings),
      sort: 'short_name'
    }
  }

  findMatchingAsList (): Promise<Platform[]> {
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
      const result: Platform[] = []
      const included: any[] = rawData.included || []

      for (const entry of rawData.data) {
        const platform = serverResponseToEntity(entry, included)
        if (this.clientSideFilterFunc(platform)) {
          result.push(platform)
        }
      }
      return result
    })
  }

  findMatchingAsPaginationLoader (pageSize: number): Promise<IPaginationLoader<Platform>> {
    const loaderPromise: Promise<IPaginationLoader<Platform>> = this.findAllOnPage(1, pageSize)
    return loaderPromise.then((loader) => {
      return new FilteredPaginationedLoader<Platform>(loader, this.clientSideFilterFunc)
    })
  }

  private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Platform>> {
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
      const result: Platform[] = []
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

export function serverResponseToEntity (entry: any, included: any[]) : Platform {
  const result: Platform = Platform.createEmpty()

  const attributes = entry.attributes
  const relationships = entry.relationships

  // TODO: use camelCase only!!!
  result.id = Number.parseInt(entry.id)

  result.description = attributes.description || ''
  result.shortName = attributes.short_name || ''
  result.longName = attributes.long_name || ''
  result.manufacturerUri = attributes.manufacturer_uri || ''
  result.manufacturerName = attributes.manufacturer_name || ''
  result.model = attributes.model || ''
  result.platformTypeUri = attributes.platform_type_uri || ''
  result.platformTypeName = attributes.platform_type_name || ''
  result.statusUri = attributes.status_uri || ''
  result.statusName = attributes.status_name || ''
  result.website = attributes.website || ''
  result.createdAt = attributes.created_at
  result.updatedAt = attributes.updated_at

  // TODO
  // result.createdBy = attributes.created_by
  // result.updatedBy = attributes.updated_by

  result.inventoryNumber = attributes.inventory_number || ''
  result.serialNumber = attributes.serial_number || ''
  result.persistentIdentifier = attributes.persistent_identifier || ''

  // TODO
  result.contacts = []
  // result.events = []

  const attachments: Attachment[] = []

  for (const attachmentFromServer of attributes.attachments) {
    const attachment = new Attachment()
    attachment.id = Number.parseInt(attachmentFromServer.id)
    attachment.label = attachmentFromServer.label || ''
    attachment.url = attachmentFromServer.url || ''

    attachments.push(attachment)
  }

  result.attachments = attachments

  const contactIds = []
  if (relationships.contacts && relationships.contacts.data && relationships.contacts.data.length > 0) {
    for (const relationShipContactData of relationships.contacts.data) {
      const contactId = Number.parseInt(relationShipContactData.id)
      contactIds.push(contactId)
    }
  }

  const possibleContacts: {[key: number]: Contact} = {}
  if (included && included.length > 0) {
    for (const includedEntry of included) {
      if (includedEntry.type === 'contact') {
        const contactId = Number.parseInt(includedEntry.id)
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
