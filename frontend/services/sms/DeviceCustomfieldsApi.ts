/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2021 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { CustomTextField } from '@/models/CustomTextField'
import {
  CustomTextFieldSerializer,
  CustomTextFieldEntityType,
  CustomTextFieldRelationEntityType
} from '@/serializers/jsonapi/CustomTextFieldSerializer'
import { CustomfieldsApi } from '@/services/sms/CustomfieldsApi'

export class DeviceCustomfieldsApi extends CustomfieldsApi {
  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath, new CustomTextFieldSerializer(CustomTextFieldEntityType.DEVICE))
  }

  add (deviceId: string, field: CustomTextField): Promise<CustomTextField> {
    return super.addWithRelation(deviceId, CustomTextFieldRelationEntityType.DEVICE, field)
  }

  update (deviceId: string, field: CustomTextField): Promise<CustomTextField> {
    return super.updateWithRelation(deviceId, CustomTextFieldRelationEntityType.DEVICE, field)
  }
}
