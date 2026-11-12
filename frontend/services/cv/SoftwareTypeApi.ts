/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { SoftwareType } from '@/models/SoftwareType'
import { SoftwareTypeSerializer } from '@/serializers/jsonapi/SoftwareTypeSerializer'
import { CVApi } from '@/services/cv/CVApi'

export class SoftwareTypeApi extends CVApi<SoftwareType> {
  private serializer: SoftwareTypeSerializer
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance)
    this.basePath = basePath
    this.serializer = new SoftwareTypeSerializer()
  }

  findAll (): Promise<SoftwareType[]> {
    const params: { [idx: string]: any } = {
      'page[size]': 10000,
      'filter[status.iexact]': 'ACCEPTED',
      sort: 'term'
    }
    return this.axiosApi.get(
      this.basePath,
      {
        params
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      return SoftwareTypeApi.sort(this.serializer.convertJsonApiObjectListToModelList(response))
    })
  }

  static sort (softwareTypes: SoftwareType[]): SoftwareType[] {
    const softwareTypesCopy: SoftwareType[] = [...softwareTypes]
    // sort alphabetical
    softwareTypesCopy.sort((a, b) => {
      if (a.name < b.name) {
        return -1
      }
      if (a.name > b.name) {
        return 1
      }
      return 0
    })
    // move 'Others' to the end
    const othersIndex: number = softwareTypesCopy.findIndex(i => i.name.toLowerCase() === 'others')
    if (othersIndex > -1) {
      const other: SoftwareType = softwareTypesCopy.splice(othersIndex, 1)[0]
      softwareTypesCopy.push(other)
    }
    return softwareTypesCopy
  }
}
