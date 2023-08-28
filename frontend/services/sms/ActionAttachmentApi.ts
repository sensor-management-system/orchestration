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
import { AxiosInstance } from 'axios'

import { Attachment } from '@/models/Attachment'
import { IActionAttachmentSerializer } from '@/serializers/jsonapi/ActionAttachmentSerializer'

export interface IActionAttachmentApi {
  serializer: IActionAttachmentSerializer
  add (actionId: string, attachment: Attachment): Promise<any>
  delete (id: string): Promise<void>
}

export abstract class AbstractActionAttachmentApi implements IActionAttachmentApi {
  private axiosApi: AxiosInstance
  readonly basePath: string

  abstract get serializer (): IActionAttachmentSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
  }

  async add (actionId: string, attachment: Attachment): Promise<any> {
    const data = this.serializer.convertModelToJsonApiData(attachment, actionId)
    await this.axiosApi.post(this.basePath, { data })
  }

  async delete (id: string): Promise<void> {
    return await this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }
}
