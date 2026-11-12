/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'
import { CVApi } from '@/services/cv/CVApi'

import { ISerializer } from '@/serializers/jsonapi/ISerializer'

export abstract class ExtendableCVApi<T> extends CVApi<T> {
  protected basePath: string
  protected serializer: ISerializer<T>

  constructor (axiosInstance: AxiosInstance, basePath: string, serializer: ISerializer<T>) {
    super(axiosInstance)
    this.basePath = basePath
    this.serializer = serializer
  }

  async findAll (currentUserEMail: string | null, commonParams: {[idx: string]: any} = {}): Promise<T[]> {
    const requests = [
      this.axiosApi.get(
        this.basePath,
        {
          params: {
            'page[size]': 10000,
            'filter[status.iexact]': 'ACCEPTED',
            sort: 'term',
            ...commonParams
          }
        }
      )
    ]
    if (currentUserEMail) {
      requests.push(
        this.axiosApi.get(
          this.basePath,
          {
            params: {
              'page[size]': 10000,
              'filter[status.iexact]': 'PENDING',
              'filter[requested_by_email]': currentUserEMail,
              sort: 'term',
              ...commonParams
            }
          }
        )
      )
    }
    const rawResponses = await Promise.all(requests)
    const result: T[] = []
    for (const rawResponse of rawResponses) {
      const response = rawResponse.data
      const entries = this.serializer.convertJsonApiObjectListToModelList(response)
      result.push(...entries)
    }
    return result
  }

  async add (t: T): Promise<T> {
    const data = this.serializer.convertModelToJsonApiData(t)

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
    return this.serializer.convertJsonApiDataToModel(response.data)
  }
}
