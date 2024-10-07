/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { AxiosInstance } from 'axios'
import { TsmLinkingSerializer } from '@/serializers/jsonapi/TsmLinkingSerializer'
import { TsmLinking } from '@/models/TsmLinking'
import { TsmLinkingInvolvedDeviceApi } from '@/services/sms/TsmLinkingInvolvedDeviceApi'

export class TsmLinkingApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private involvedDevicesApi: TsmLinkingInvolvedDeviceApi
  private serializer: TsmLinkingSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, involvedDevicesApi: TsmLinkingInvolvedDeviceApi) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.involvedDevicesApi = involvedDevicesApi
    this.serializer = new TsmLinkingSerializer()
  }

  getRelatedTsmLinkings (configurationId: string): Promise<TsmLinking[]> {
    const url = '/configurations/' + configurationId + '/datastream-links'
    const params = {
      'page[size]': 10000,
      include: [
        'device_mount_action',
        'device_mount_action.device',
        'device_property',
        'tsm_endpoint',
        'involved_devices'
      ].join(',')
    }
    return this.axiosApi.get(url, { params }).then((rawResponse) => {
      const rawData = rawResponse.data
      return this.serializer.convertJsonApiObjectListToModelList(rawData)
    })
  }

  findById (id: string): Promise<TsmLinking> {
    const url = this.basePath + '/' + id

    const params = {
      include: [
        'device_mount_action',
        'device_mount_action.device',
        'device_property',
        'tsm_endpoint',
        'involved_devices'
      ].join(',')
    }

    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return this.serializer.convertJsonApiObjectToModel(rawServerResponse.data)
    })
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  async add (tsmLinking: TsmLinking): Promise<string> {
    const url = this.basePath
    const data = this.serializer.convertModelToJsonApiData(tsmLinking)
    const response = await this.axiosApi.post(url, { data })
    const tsmLinkingId = response.data.data.id
    // After we got the id for the new tsm linking we can add the links to the
    // other involved devices.
    for (const involvedDevice of tsmLinking.involvedDevices) {
      await this.involvedDevicesApi.add(involvedDevice, tsmLinkingId)
    }
    return tsmLinkingId
  }

  async update (tsmLinking: TsmLinking): Promise<string> {
    if (!tsmLinking.id) {
      throw new Error('no id for the TsmLinking')
    }
    // Get the currently involved devices.
    const existingLinking = await this.findById(tsmLinking.id)
    const existingInvolvedDevices = existingLinking.involvedDevices

    for (const existingInvoledDevice of existingInvolvedDevices) {
      let toDelete = false
      let toUpdate = false
      const idx = tsmLinking.involvedDevices.findIndex(newOne => newOne.deviceId === existingInvoledDevice.deviceId)
      if (idx > -1) {
        const newOne = tsmLinking.involvedDevices[idx]
        if (existingInvoledDevice.orderIndex !== newOne.orderIndex) {
          existingInvoledDevice.orderIndex = newOne.orderIndex
          toUpdate = true
        }
      } else {
        toDelete = true
      }
      if (toDelete) {
        await this.involvedDevicesApi.delete(existingInvoledDevice)
      } else if (toUpdate) {
        await this.involvedDevicesApi.update(existingInvoledDevice, tsmLinking.id)
      }
    }
    for (const involvedDevice of tsmLinking.involvedDevices) {
      if (!existingInvolvedDevices.find(d => d.deviceId === involvedDevice.deviceId)) {
        await this.involvedDevicesApi.add(involvedDevice, tsmLinking.id)
      }
    }

    const url = this.basePath + '/' + tsmLinking.id
    const data = this.serializer.convertModelToJsonApiData(tsmLinking)
    const response = await this.axiosApi.patch(url, { data })
    return response.data.data.id
  }

  async delete (tsmLinking: TsmLinking): Promise<void> {
    if (!tsmLinking.id) {
      throw new Error('no id for the TsmLinking')
    }
    const url = this.basePath + '/' + tsmLinking.id
    return await this.axiosApi.delete<string, void>(url)
  }
}
