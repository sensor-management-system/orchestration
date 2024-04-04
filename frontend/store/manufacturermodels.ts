/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2024
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

import { Commit, GetterTree, ActionTree } from 'vuex'

import { RootState } from '@/store'

import { Contact } from '@/models/Contact'
import { ExportControl } from '@/models/ExportControl'
import { ManufacturerModel } from '@/models/ManufacturerModel'
import { IManufacturerModelSearchParams } from '@/modelUtils/ManufacturerModelSearchParams'
import { ExportControlAttachment } from '@/models/ExportControlAttachment'

const PAGE_SIZES = [
  25,
  50,
  100
]

export interface ManufacturermodelsState {
  manufacturerModel: ManufacturerModel | null
  exportControl: ExportControl | null
  exportControlAttachments: ExportControlAttachment[]
  exportControlAttachment: ExportControlAttachment | null
  exportControlCreatedByContact: Contact | null
  exportControlUpdatedByContact: Contact | null
  manufacturerModels: ManufacturerModel[]
  pageNumber: number
  pageSize: number
  totalCount: number
  totalPages: number
}

const state = (): ManufacturermodelsState => ({
  manufacturerModel: null,
  exportControl: null,
  exportControlAttachments: [],
  exportControlAttachment: null,
  exportControlCreatedByContact: null,
  exportControlUpdatedByContact: null,
  manufacturerModels: [],
  pageNumber: 1,
  pageSize: PAGE_SIZES[0],
  totalCount: 0,
  totalPages: 1
})

export type PageSizesGetter = number[]
export type PublicExportControlAttachmentsGetter = ExportControlAttachment[]
export type InternalExportControlAttachmentsGetter = ExportControlAttachment[]

const getters: GetterTree<ManufacturermodelsState, RootState> = {
  pageSizes: (): number[] => {
    return PAGE_SIZES
  },
  publicExportControlAttachments: (state: ManufacturermodelsState): ExportControlAttachment[] => {
    return state.exportControlAttachments.filter(x => !x.isExportControlOnly)
  },
  internalExportControlAttachments: (state: ManufacturermodelsState): ExportControlAttachment[] => {
    return state.exportControlAttachments.filter(x => x.isExportControlOnly)
  }
}

export type AddExportControlAttachmentAction = (params: { manufacturerModelId: string, attachment: ExportControlAttachment}) => Promise<ExportControlAttachment>
export type DeleteExportControlAttachmentAction = (attachmendId: string) => Promise<void>
export type DownloadAttachmentAction = (attachmentUrl: string) => Promise<Blob>
export type LoadExportControlAction = (params: { manufacturerModelId: string}) => Promise<void>
export type LoadExportControlAttachmentsAction = (manufacturerModelId: string) => Promise<void>
export type LoadExportControlAttachmentAction = (exportControlAttachmentId: string) => Promise<void>
export type LoadExportControlCreatedAndUpdatedByContactsAction = (exportControl: ExportControl | null) => Promise<void>
export type LoadManufacturerModelAction = (params: { manufacturerModelId: string}) => Promise<void>
export type SearchManufacturerModelsPaginatedAction = (params: IManufacturerModelSearchParams) => Promise<void>
export type SetPageNumberAction = (newPageNumber: number) => void
export type SetPageSizeAction = (newPageSize: number) => void
export type SaveExportControlAction = (exportControl: ExportControl) => Promise<ExportControl>
export type UpdateExportControlAttachmentAction = (params: { manufacturerModelId: string, attachment: ExportControlAttachment}) => Promise<ExportControlAttachment>
export type DeleteExportControlAction = (id: string) => Promise<void>

const actions: ActionTree<ManufacturermodelsState, RootState> = {
  async searchManufacturerModelsPaginated (
    {
      commit,
      state
    }: { commit: Commit, state: ManufacturermodelsState },
    searchParams: IManufacturerModelSearchParams
  ): Promise<void> {
    const { elements, totalCount } = await this.$api.manufacturerModels.searchPaginated(
      searchParams,
      state.pageNumber,
      state.pageSize,
      {
        includeExportControl: true
      }
    )
    commit('setManufacturerModels', elements)
    const totalPages = Math.ceil(totalCount / state.pageSize)
    commit('setTotalPages', totalPages)
    commit('setTotalCount', totalCount)
  },
  async loadManufacturerModel ({ commit }: { commit: Commit }, { manufacturerModelId }: { manufacturerModelId: string}): Promise<void> {
    const manufacturerModel = await this.$api.manufacturerModels.findById(
      manufacturerModelId,
      { includeExportControl: false }
    )
    commit('setManufacturerModel', manufacturerModel)
  },
  async loadExportControl ({ commit }: { commit: Commit }, { manufacturerModelId }: { manufacturerModelId: string }) {
    const exportControl = await this.$api.manufacturerModels.findExportControlByManufacturerModelIdOrNewOne(manufacturerModelId)
    commit('setExportControl', exportControl)
  },
  async loadExportControlAttachments ({ commit }: { commit: Commit }, manufacturerModelId: string): Promise<void> {
    const exportControlAttachments = await this.$api.manufacturerModels.findRelatedExportControlAttachments(manufacturerModelId)
    commit('setExportControlAttachments', exportControlAttachments)
  },
  async loadExportControlAttachment ({ commit }: { commit: Commit }, exportControlAttachmentId: string): Promise<void> {
    const exportControlAttachment = await this.$api.exportControlAttachments.findById(exportControlAttachmentId)
    commit('setExportControlAttachment', exportControlAttachment)
  },
  async downloadAttachment (_, attachmentUrl: string): Promise<Blob> {
    return await this.$api.exportControlAttachments.getFile(attachmentUrl)
  },
  updateExportControlAttachment (_, { manufacturerModelId, attachment }: { manufacturerModelId: string, attachment: ExportControlAttachment }): Promise<ExportControlAttachment> {
    return this.$api.exportControlAttachments.update(manufacturerModelId, attachment)
  },
  deleteExportControlAttachment (_, attachmentId: string): Promise<void> {
    return this.$api.exportControlAttachments.deleteById(attachmentId)
  },
  addExportControlAttachment (_, { manufacturerModelId, attachment }: { manufacturerModelId: string, attachment: ExportControlAttachment}): Promise<ExportControlAttachment> {
    return this.$api.exportControlAttachments.add(manufacturerModelId, attachment)
  },
  async loadExportControlCreatedAndUpdatedByContacts ({ commit }: { commit: Commit }, exportControl: ExportControl | null): Promise<void> {
    if (!exportControl) {
      commit('setExportControlCreatedByContact', null)
      commit('setExportControlUpdatedByContact', null)
      return
    }
    if (!exportControl.createdByUserId) {
      commit('setExportControlCreatedByContact', null)
    } else {
      const createdByContact = await this.$api.contacts.findContactByUserId(exportControl.createdByUserId)
      commit('setExportControlCreatedByContact', createdByContact)
    }
    if (!exportControl.updatedByUserId) {
      commit('setExportControlUpdatedByContact', null)
    } else {
      const updatedByContact = await this.$api.contacts.findContactByUserId(exportControl.updatedByUserId)
      commit('setExportControlUpdatedByContact', updatedByContact)
    }
  },
  saveExportControl (_, exportControl: ExportControl): Promise<ExportControl> {
    return this.$api.exportControl.save(exportControl)
  },
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number) {
    commit('setPageNumber', newPageNumber)
  },
  setPageSize ({ commit }: { commit: Commit }, newPageSize: number) {
    commit('setPageSize', newPageSize)
  },
  deleteExportControl (_, id: string): Promise<void> {
    return this.$api.exportControl.deleteById(id)
  }
}

export type SetExportControlAttachmentsMutation = (exportControlAttachments: ExportControlAttachment[]) => Promise<void>
const mutations = {
  setManufacturerModel (state: ManufacturermodelsState, manufacturerModel: ManufacturerModel) {
    state.manufacturerModel = manufacturerModel
  },
  setExportControl (state: ManufacturermodelsState, exportControl: ExportControl) {
    state.exportControl = exportControl
  },
  setManufacturerModels (state: ManufacturermodelsState, manufacturerModels: ManufacturerModel[]) {
    state.manufacturerModels = manufacturerModels
  },
  setExportControlAttachments (state: ManufacturermodelsState, exportControlAttachment: ExportControlAttachment[]) {
    state.exportControlAttachments = exportControlAttachment
  },
  setExportControlAttachment (state: ManufacturermodelsState, exportControlAttachment: ExportControlAttachment) {
    state.exportControlAttachment = exportControlAttachment
  },
  setExportControlCreatedByContact (state: ManufacturermodelsState, exportControlCreatedByContact: Contact | null) {
    state.exportControlCreatedByContact = exportControlCreatedByContact
  },
  setExportControlUpdatedByContact (state: ManufacturermodelsState, exportControlUpdatedByContact: Contact | null) {
    state.exportControlUpdatedByContact = exportControlUpdatedByContact
  },
  setPageNumber (state: ManufacturermodelsState, pageNumber: number) {
    state.pageNumber = pageNumber
  },
  setPageSize (state: ManufacturermodelsState, pageSize: number) {
    state.pageSize = pageSize
  },
  setTotalCount (state: ManufacturermodelsState, totalCount: number) {
    state.totalCount = totalCount
  },
  setTotalPages (state: ManufacturermodelsState, totalPages: number) {
    state.totalPages = totalPages
  }
}
export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
