/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { SiteType } from '@/models/SiteType'
import { SiteTypeSerializer } from '@/serializers/jsonapi/SiteTypeSerializer'
import { ExtendableCVApi } from '@/services/cv/ExtendableCVApi'

export class SiteTypeApi extends ExtendableCVApi<SiteType> {
  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath, new SiteTypeSerializer())
  }
}
