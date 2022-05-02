import { Commit } from 'vuex'
import { IUploadResult } from '@/services/sms/UploadApi'
const state = {}

const getters = {}

const actions = {
  uploadFile ({ _commit }: {_commit: Commit}, file: File): Promise<IUploadResult> {
    return this.$api.upload.file(file)
  }
}

const mutations = {}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
