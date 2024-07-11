/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { AxiosInstance } from 'axios'
import { IManufacturerModelSearchParams } from '@/modelUtils/ManufacturerModelSearchParams'
import { Manufacturer } from '@/models/Manufacturer'
import { ManufacturerModel } from '@/models/ManufacturerModel'
import { ManufacturerModelSerializer } from '@/serializers/jsonapi/ManufacturerModelSerializer'
import { ExportControl } from '@/models/ExportControl'
import { ExportControlSerializer } from '@/serializers/jsonapi/ExportControlSerializer'
import { ExportControlAttachment } from '@/models/ExportControlAttachment'
import { ExportControlAttachmentSerializer } from '@/serializers/jsonapi/ExportControlAttachmentSerializer'

export interface includeRelationships {
  includeExportControl: boolean
}

export interface SearchResult {
  elements: ManufacturerModel[]
  totalCount: number
}

export class ManufacturerModelApi {
  private axiosApi: AxiosInstance
  private readonly basePath: string
  private serializer: ManufacturerModelSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.serializer = new ManufacturerModelSerializer()
  }

  async searchPaginated (
    searchParams: IManufacturerModelSearchParams,
    pageNumber: number,
    pageSize: number,
    included: includeRelationships
  ): Promise<SearchResult> {
    const includeList: string[] = []
    if (included.includeExportControl) {
      includeList.push('export_control')
    }

    const filterSettings: any[] = []
    if (searchParams.manufacturers.length > 0) {
      filterSettings.push(
        {
          name: 'manufacturer_name',
          op: 'in_',
          val: searchParams.manufacturers.map((m: Manufacturer) => m.name)
        }
      )
    }
    if (searchParams.dualUseSearchOption === 'yes') {
      filterSettings.push({
        name: 'export_control.dual_use',
        op: 'eq',
        val: true
      })
    } else if (searchParams.dualUseSearchOption === 'no') {
      filterSettings.push({
        name: 'export_control.dual_use',
        op: 'eq',
        val: false
      })
    } else if (searchParams.dualUseSearchOption === 'unspecified') {
      filterSettings.push({
        name: 'export_control.dual_use',
        op: 'eq',
        val: null
      })
    }

    const filterParams: {[key: string]: any} = {}
    if (searchParams.searchText) {
      filterParams.q = searchParams.searchText
    }

    if (filterSettings.length > 0) {
      filterParams.filter = JSON.stringify(filterSettings)
    }

    const rawResponse = await this.axiosApi.get(this.basePath, {
      params: {
        'page[size]': pageSize,
        'page[number]': pageNumber,
        include: includeList.join(','),
        sort: 'manufacturer_name,model',
        ...filterParams

      }
    })
    const rawData = rawResponse.data
    const elements: ManufacturerModel[] = this.serializer.convertJsonApiObjectListToModelList(rawData)
    const totalCount = rawData.meta.count
    return {
      elements,
      totalCount
    }
  }

  async findById (manufacturerModelId: string, included: includeRelationships): Promise<ManufacturerModel> {
    const includeList: string[] = []
    if (included.includeExportControl) {
      includeList.push('export_control')
    }

    const rawResponse = await this.axiosApi.get(this.basePath + '/' + manufacturerModelId, {
      params: {
        include: includeList.join(',')
      }
    })
    const rawData = rawResponse.data
    return this.serializer.convertJsonApiObjectToModel(rawData)
  }

  async findExportControlByManufacturerModelIdOrNewOne (manufacturerModelId: string): Promise<ExportControl> {
    const rawResponse = await this.axiosApi.get(`${this.basePath}/${manufacturerModelId}/export-control`)
    const rawData = rawResponse.data
    const exportControlList = new ExportControlSerializer().convertJsonApiObjectListToModelList(rawData)
    if (exportControlList.length > 0) {
      return exportControlList[0]
    }
    const newOne = new ExportControl()
    newOne.manufacturerModelId = manufacturerModelId
    return newOne
  }

  async findByManufacturerNameAndModel (manufacturerModelName: string, model: string, included: includeRelationships): Promise<ManufacturerModel | null> {
    const includeList: string[] = []
    if (included.includeExportControl) {
      includeList.push('export_control')
    }

    const filterSettings: any[] = [
      {
        name: 'manufacturer_name',
        op: 'eq',
        val: manufacturerModelName
      },
      {
        name: 'model',
        op: 'eq',
        val: model
      }
    ]
    const filterParams = JSON.stringify(filterSettings)

    const rawResponse = await this.axiosApi.get(this.basePath, {
      params: {
        include: includeList.join(','),
        filter: filterParams

      }
    })
    const rawData = rawResponse.data
    const elements: ManufacturerModel[] = this.serializer.convertJsonApiObjectListToModelList(rawData)
    if (elements.length > 0) {
      return elements[0]
    }
    return null
  }

  async findRelatedExportControlAttachments (manufacturerModelId: string): Promise<ExportControlAttachment[]> {
    const url = this.basePath + '/' + manufacturerModelId + '/export-control-attachments'
    const params = {
      'page[size]': 10000
    }
    const rawServerResponse = await this.axiosApi.get(url, { params })
    return new ExportControlAttachmentSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
  }
}
