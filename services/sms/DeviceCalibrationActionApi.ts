/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */
import { AxiosInstance } from 'axios'

import { Attachment } from '@/models/Attachment'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { DeviceCalibrationActionSerializer } from '@/serializers/jsonapi/DeviceCalibrationActionSerializer'
import { DeviceCalibrationActionAttachmentApi } from '@/services/sms/DeviceCalibrationActionAttachmentApi'
import { DeviceCalibrationDevicePropertyApi } from '@/services/sms/DeviceCalibrationDevicePropertyApi'
import { DeviceProperty } from '@/models/DeviceProperty'

export class DeviceCalibrationActionApi {
  private axiosApi: AxiosInstance
  private serializer: DeviceCalibrationActionSerializer
  private attachmentApi: DeviceCalibrationActionAttachmentApi
  private propertyApi: DeviceCalibrationDevicePropertyApi

  constructor (axiosInstace: AxiosInstance, attachmentApi: DeviceCalibrationActionAttachmentApi, propertyApi: DeviceCalibrationDevicePropertyApi) {
    this.axiosApi = axiosInstace
    this.serializer = new DeviceCalibrationActionSerializer()
    this.attachmentApi = attachmentApi
    this.propertyApi = propertyApi
  }

  async findById (id: string): Promise<DeviceCalibrationAction> {
    const response = await this.axiosApi.get(id, {
      params: {
        include: [
          'contact',
          'device_calibration_attachments.attachment',
          'device_property_calibrations',
          'device_property_calibrations.device_property'

        ].join(',')
      }
    })
    const data = response.data
    return this.serializer.convertJsonApiObjectToModel(data)
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(id)
  }

  async add (deviceId: string, action: DeviceCalibrationAction): Promise<DeviceCalibrationAction> {
    const url = ''
    const data = this.serializer.convertModelToJsonApiData(action, deviceId)
    const response = await this.axiosApi.post(url, { data })
    const savedAction = this.serializer.convertJsonApiObjectToModel(response.data)

    if (savedAction.id) {
      const attachmentPromises = action.attachments.map((attachment: Attachment) => this.attachmentApi.add(savedAction.id as string, attachment))
      const measuredQuantityPromises = action.measuredQuantities.map((measuredQuantity: DeviceProperty) => this.propertyApi.add(savedAction.id as string, measuredQuantity))
      const promises = [...attachmentPromises, ...measuredQuantityPromises]
      await Promise.all(promises)
    }
    return savedAction
  }

  async update (deviceId: string, action: DeviceCalibrationAction): Promise<DeviceCalibrationAction> {
    if (!action.id) {
      throw new Error('no id for the DeviceCalirbationAction')
    }
    // load the stored action to get a list of the current attachments before update
    const attRawResponse = await this.axiosApi.get(action.id, {
      params: {
        include: [
          'device_calibration_attachments.attachment',
          'device_property_calibrations',
          'device_property_calibrations.device_property'
        ].join(',')
      }
    })
    const attResponseData = attRawResponse.data
    const included = attResponseData.included

    // get the relations between attachments and device action attachments
    const linkedAttachments: { [attachmentId: string]: string } = {}
    const linkedMeasuredQuantities: { [devicePropertyId: string]: string } = {}
    if (included) {
      const attachmentRelations = this.serializer.convertJsonApiIncludedActionAttachmentsToIdList(included)
      // convert to object to gain faster access to its members
      attachmentRelations.forEach((rel) => {
        linkedAttachments[rel.attachmentId] = rel.deviceCalibrationActionAttachmentId
      })

      const propertyRelationships = this.serializer.convertJsonApiIncludedDevicePropertioesToIdList(included)
      propertyRelationships.forEach((rel) => {
        linkedMeasuredQuantities[rel.devicePropertyId] = rel.devicePropertyCalibrationId
      })
    }

    // update the action
    const data = this.serializer.convertModelToJsonApiData(action, deviceId)
    const actionResponse = await this.axiosApi.patch(action.id, { data })

    // find new attachments
    const newAttachments: Attachment[] = []
    action.attachments.forEach((attachment: Attachment) => {
      if (attachment.id && linkedAttachments[attachment.id]) {
        return
      }
      newAttachments.push(attachment)
    })
    // and same for the device properties aka measured quanitities
    const newMeasuredQuantities: DeviceProperty[] = []
    action.measuredQuantities.forEach((measuredQuantity: DeviceProperty) => {
      if (measuredQuantity.id && linkedMeasuredQuantities[measuredQuantity.id]) {
        return
      }
      newMeasuredQuantities.push(measuredQuantity)
    })

    // find deleted attachments
    const deviceActionAttachmentsToDelete: string[] = []
    for (const attachmentId in linkedAttachments) {
      if (action.attachments.find((i: Attachment) => i.id === attachmentId)) {
        continue
      }
      deviceActionAttachmentsToDelete.push(linkedAttachments[attachmentId])
    }
    const devicePropertyCalibrationsToDelete: string[] = []
    for (const devicePropertyId in linkedMeasuredQuantities) {
      if (action.measuredQuantities.find((i: DeviceProperty) => i.id === devicePropertyId)) {
        continue
      }
      devicePropertyCalibrationsToDelete.push(linkedMeasuredQuantities[devicePropertyId])
    }

    // when there are no new attachments, newPromises is empty, which is okay
    const newAttachmentPromises = newAttachments.map((attachment: Attachment) => this.attachmentApi.add(action.id as string, attachment))
    // when there are no deleted attachments, deletedPromises is empty, which is okay
    const deletedAttachmentPromises = deviceActionAttachmentsToDelete.map((id: string) => this.attachmentApi.delete(id))
    // And same for the device properties
    const newMeasuredQuantityPromises = newMeasuredQuantities.map((measuredQuantity: DeviceProperty) => this.propertyApi.add(action.id as string, measuredQuantity))
    const deletedMeasuredQuantities = devicePropertyCalibrationsToDelete.map((id: string) => this.propertyApi.delete(id))

    await Promise.all([
      ...deletedAttachmentPromises,
      ...deletedMeasuredQuantities,
      ...newAttachmentPromises,
      ...newMeasuredQuantityPromises
    ])

    return this.serializer.convertJsonApiObjectToModel(actionResponse.data)
  }
}
