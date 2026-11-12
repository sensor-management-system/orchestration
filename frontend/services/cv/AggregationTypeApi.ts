/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { AggregationType } from '@/models/AggregationType'
import { AggregationTypeSerializer } from '@/serializers/jsonapi/AggregationTypeSerializer'
import { ExtendableCVApi } from '@/services/cv/ExtendableCVApi'

export class AggregationTypeApi extends ExtendableCVApi<AggregationType> {
  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath, new AggregationTypeSerializer())
  }
}
