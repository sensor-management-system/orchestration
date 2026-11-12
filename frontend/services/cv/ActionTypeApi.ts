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

import { ActionType } from '@/models/ActionType'
import { ActionTypeSerializer } from '@/serializers/jsonapi/ActionTypeSerializer'
import { ExtendableCVApi } from '@/services/cv/ExtendableCVApi'

export const ACTION_TYPE_API_FILTER_DEVICE = 'Device'
export const ACTION_TYPE_API_FILTER_PLATFORM = 'Platform'
export const ACTION_TYPE_API_FILTER_CONFIGURATION = 'Configuration'
export type ActionTypeApiFilterType = typeof ACTION_TYPE_API_FILTER_DEVICE | typeof ACTION_TYPE_API_FILTER_PLATFORM | typeof ACTION_TYPE_API_FILTER_CONFIGURATION

export class ActionTypeApi extends ExtendableCVApi<ActionType> {
  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath, new ActionTypeSerializer())
    this.basePath = basePath
    this.serializer = new ActionTypeSerializer()
  }

  findAllForType (actionTypeFilter: ActionTypeApiFilterType, currentUserEMail: string | null): Promise<ActionType[]> {
    return this.findAll(
      currentUserEMail,
      {
        'filter[action_category__term]': actionTypeFilter
      }
    )
  }
}
