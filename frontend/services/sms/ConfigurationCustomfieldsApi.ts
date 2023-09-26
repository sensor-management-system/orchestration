/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2022
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 * (UFZ, https://www.ufz.de)
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
