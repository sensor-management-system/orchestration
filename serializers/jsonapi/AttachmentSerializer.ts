/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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
import {
  Attachment
} from '@/models/Attachment'

import { IJsonApiNestedElement } from '@/serializers/jsonapi/JsonApiTypes'

export class AttachmentSerializer {
  convertJsonApiElementToModel (attachment: IJsonApiNestedElement): Attachment {
    const result = new Attachment()
    result.id = attachment.id
    result.label = attachment.label || ''
    result.url = attachment.url || ''

    return result
  }

  convertNestedJsonApiToModelList (attachments: IJsonApiNestedElement[]): Attachment[] {
    return attachments.map(this.convertJsonApiElementToModel)
  }

  convertModelListToNestedJsonApiArray (attachments: Attachment[]): IJsonApiNestedElement[] {
    const result = []
    for (const attachment of attachments) {
      const attachmentToSave: any = {}
      if (attachment.id != null) {
        attachmentToSave.id = attachment.id
      }
      attachmentToSave.label = attachment.label
      attachmentToSave.url = attachment.url

      result.push(attachmentToSave)
    }

    return result
  }
}
