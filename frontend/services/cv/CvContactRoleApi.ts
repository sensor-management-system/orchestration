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

import { CvContactRole } from '@/models/CvContactRole'
import { CvContactRoleSerializer } from '@/serializers/jsonapi/CvContactRoleSerializer'
import { ExtendableCVApi } from '@/services/cv/ExtendableCVApi'

export class CvContactRoleApi extends ExtendableCVApi<CvContactRole> {
  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath, new CvContactRoleSerializer())
  }
}
