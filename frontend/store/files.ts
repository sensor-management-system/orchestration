/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { GetterTree, ActionTree } from 'vuex'
import { IUploadResult } from '@/services/sms/UploadApi'

import { RootState } from '@/store'

const UPLOAD_SIZE_LIMIT = 200 * 1024 * 1024

export interface IFilesState {
  uploadSizeLimit: number
}
const state = (): IFilesState => ({
  uploadSizeLimit: UPLOAD_SIZE_LIMIT
})
const getters: GetterTree<IFilesState, RootState> = {
}
const actions: ActionTree<IFilesState, RootState> = {
  async uploadFile (_nonUsedContext, file: File): Promise<IUploadResult> {
    return await this.$api.upload.file(file)
  },
  async uploadBlob (_nonUsedContext, { blob, filename }: {blob: Blob, filename: string}): Promise<IUploadResult> {
    return await this.$api.upload.blob(blob, filename)
  }
}
const mutations = {
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
