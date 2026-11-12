/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2023 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { License } from '@/models/License'
import { LicenseSerializer } from '@/serializers/jsonapi/LicenseSerializer'
import { ExtendableCVApi } from '@/services/cv/ExtendableCVApi'

export class LicenseApi extends ExtendableCVApi<License> {
  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath, new LicenseSerializer())
  }
}
