/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2021 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { Parameter } from '@/models/Parameter'
import {
  ParameterSerializer,
  ParameterEntityType,
  ParameterRelationEntityType
} from '@/serializers/jsonapi/ParameterSerializer'
import { ParameterApi } from '@/services/sms/ParameterApi'

export class DeviceParameterApi extends ParameterApi {
  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath, new ParameterSerializer(ParameterEntityType.DEVICE))
  }

  add (deviceId: string, parameter: Parameter): Promise<Parameter> {
    return super.addWithRelation(deviceId, ParameterRelationEntityType.DEVICE, parameter)
  }

  update (deviceId: string, parameter: Parameter): Promise<Parameter> {
    return super.updateWithRelation(deviceId, ParameterRelationEntityType.DEVICE, parameter)
  }
}
