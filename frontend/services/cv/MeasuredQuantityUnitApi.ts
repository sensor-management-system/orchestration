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

import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'
import { MeasuredQuantityUnitSerializer } from '@/serializers/jsonapi/MeasuredQuantityUnitSerializer'
import { CVApi } from '@/services/cv/CVApi'

export class MeasuredQuantityUnitApi extends CVApi<MeasuredQuantityUnit> {
  private serializer: MeasuredQuantityUnitSerializer
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance)
    this.basePath = basePath
    this.serializer = new MeasuredQuantityUnitSerializer()
  }

  findAll (): Promise<MeasuredQuantityUnit[]> {
    return this.axiosApi.get(
      this.basePath,
      {
        params: {
          'page[size]': 10000,
          include: 'unit'
        }
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      this.serializer.included = response.included
      return this.serializer.convertJsonApiObjectListToModelList(response)
    })
  }

  async find (id: string): Promise<MeasuredQuantityUnit> {
    const rawResponse = await this.axiosApi.get(this.basePath + id + '?include=unit')
    const response = rawResponse.data
    this.serializer.included = response.included
    return this.serializer.convertJsonApiDataToModel(response.data)
  }

  async add (measuredQuantityUnit: MeasuredQuantityUnit): Promise<MeasuredQuantityUnit> {
    const data = this.serializer.convertModelToJsonApiData(measuredQuantityUnit)

    const rawResponse = await this.axiosApi.post(
      this.basePath,
      {
        data
      },
      {
        headers: {
          'Content-Type': 'application/vnd.api+json'
        }
      }
    )
    const response = rawResponse.data
    const id = response.data.id
    return await this.find(id)
  }
}
