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

import { ParameterChangeAction } from '@/models/ParameterChangeAction'
import {
  ParameterChangeActionSerializer,
  ParameterChangeActionEntityType,
  ParameterChangeActionRelationEntityType
} from '@/serializers/jsonapi/ParameterChangeActionSerializer'
import { ParameterChangeActionApi } from '@/services/sms/ParameterChangeActionApi'

export class DeviceParameterChangeActionApi extends ParameterChangeActionApi {
  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath, new ParameterChangeActionSerializer(ParameterChangeActionEntityType.DEVICE_PARAMETER_VALUE_CHANGE))
  }

  findById (parameterId: string): Promise<ParameterChangeAction> {
    return super.findByIdWithRelation(parameterId, ParameterChangeActionRelationEntityType.DEVICE_PARAMETER)
  }

  add (parameterId: string, parameterChangeAction: ParameterChangeAction): Promise<ParameterChangeAction> {
    return super.addWithRelation(parameterId, ParameterChangeActionRelationEntityType.DEVICE_PARAMETER, parameterChangeAction)
  }

  update (parameterId: string, parameterChangeAction: ParameterChangeAction): Promise<ParameterChangeAction> {
    return super.updateWithRelation(parameterId, ParameterChangeActionRelationEntityType.DEVICE_PARAMETER, parameterChangeAction)
  }
}
