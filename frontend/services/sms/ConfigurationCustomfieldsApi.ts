/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
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

export class ConfigurationCustomfieldsApi extends CustomfieldsApi {
  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath, new CustomTextFieldSerializer(CustomTextFieldEntityType.CONFIGURATION))
  }

  add (configurationId: string, field: CustomTextField): Promise<CustomTextField> {
    return super.addWithRelation(configurationId, CustomTextFieldRelationEntityType.CONFIGURATION, field)
  }

  update (configurationId: string, field: CustomTextField): Promise<CustomTextField> {
    return super.updateWithRelation(configurationId, CustomTextFieldRelationEntityType.CONFIGURATION, field)
  }
}
