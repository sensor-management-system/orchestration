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

import { Attachment } from '@/models/Attachment'
import { IJsonApiObject, IJsonApiDataWithOptionalId, IJsonApiTypeIdAttributes, IJsonApiObjectList } from '@/serializers/jsonapi/JsonApiTypes'

export class PlatformAttachmentSerializer {
  convertJsonApiObjectToModel (jsonApiObject: IJsonApiObject): Attachment {
    const data = jsonApiObject.data
    return this.convertJsonApiDataToModel(data)
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiObjectList): Attachment[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiTypeIdAttributes): Attachment {
    const attribues = jsonApiData.attributes

    const newEntry = new Attachment()

    newEntry.id = jsonApiData.id.toString()
    newEntry.url = attribues.url || ''
    newEntry.label = attribues.label || ''

    return newEntry
  }

  convertModelToJsonApiData (attachment: Attachment, platformId: string): IJsonApiDataWithOptionalId {
    const data: any = {
      type: 'platform_attachment',
      attributes: {
        url: attachment.url,
        label: attachment.label
      },
      relationships: {
        platform: {
          data: {
            type: 'platform',
            id: platformId
          }
        }
      }
    }
    if (attachment.id) {
      data.id = attachment.id
    }
    return data
  }
}
