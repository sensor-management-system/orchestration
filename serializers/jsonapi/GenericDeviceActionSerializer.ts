/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
import { DateTime } from 'luxon'
import { GenericDeviceAction, IGenericDeviceAction } from '@/models/GenericDeviceAction'
import {
  IJsonApiDataWithOptionalId,
  IJsonApiObject,
  IJsonApiObjectList,
  IJsonApiTypeIdAttributes
} from '@/serializers/jsonapi/JsonApiTypes'

export class GenericDeviceActionSerializer {
  convertJsonApiObjectToModel (jsonApiObject: IJsonApiObject): GenericDeviceAction {
    const data = jsonApiObject.data
    return this.convertJsonApiDataToModel(data)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiTypeIdAttributes): GenericDeviceAction {
    const attributes = jsonApiData.attributes
    const newEntry = GenericDeviceAction.createEmpty()

    newEntry.id = jsonApiData.id.toString()
    newEntry.description = attributes.description || ''
    newEntry.actionTypeName = attributes.action_type_name || ''
    newEntry.actionTypeUrl = attributes.action_type_uri || ''
    newEntry.beginDate = attributes.begin_date ? DateTime.fromISO(attributes.begin_date, { zone: 'UTC' }) : null
    newEntry.endDate = attributes.end_date ? DateTime.fromISO(attributes.end_date, { zone: 'UTC' }) : null
    // TODO: how to resolve the contact?

    return newEntry
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiObjectList): GenericDeviceAction[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel)
  }

  convertModelToJsonApiData (action: GenericDeviceAction, deviceId: string): IJsonApiDataWithOptionalId {
    const data: any = {
      type: 'generic_device_action',
      attributes: {
        description: action.description,
        action_type_name: action.actionTypeName,
        action_type_uri: action.actionTypeUrl,
        begin_date: action.beginDate != null ? action.beginDate.setZone('UTC').toISO() : null,
        end_date: action.endDate != null ? action.endDate.setZone('UTC').toISO() : null
        // TODO: how to handle the contact?
      },
      relationships: {
        device: {
          data: {
            type: 'device',
            id: deviceId
          }
        }
      }
    }
    if (action.id) {
      data.id = action.id
    }
    if (action.contact && action.contact.id) {
      data.relationships.contact = {
        data: {
          type: 'contact',
          id: action.contact.id
        }
      }
    }
    return data
  }
}
