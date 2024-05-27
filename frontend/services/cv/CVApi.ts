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
import { IPaginationLoader } from '@/utils/PaginatedLoader'

export abstract class CVApi<T> {
  protected axiosApi: AxiosInstance

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
  }

  protected loadPaginated (loader: IPaginationLoader<T>): Promise<T[]> {
    let result: T[] = loader.elements
    const promise = new Promise<T[]>((resolve, reject) => {
      if (!loader.funToLoadNext) {
        resolve(result)
        return
      }
      loader.funToLoadNext().then((nextLoader) => {
        this.loadPaginated(nextLoader).then((loadedEntities) => {
          result = [...result, ...loadedEntities] as T[]
          resolve(result)
        })
      }).catch((_error) => {
        reject(_error)
      })
    })
    return promise
  }
}
