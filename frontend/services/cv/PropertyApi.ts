/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { Property } from '@/models/Property'
import { PropertySerializer } from '@/serializers/jsonapi/PropertySerializer'
import { ExtendableCVApi } from '@/services/cv/ExtendableCVApi'

export class PropertyApi extends ExtendableCVApi<Property> {
  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath, new PropertySerializer())
  }
}
