/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'

import { IContact } from '@/models/Contact'

export interface IMetaCreationInfo {
  createdBy: IContact | null
  createdAt: DateTime | null
  updatedBy: IContact | null
  updatedAt: DateTime | null
  createdByUserId: string | null
}
