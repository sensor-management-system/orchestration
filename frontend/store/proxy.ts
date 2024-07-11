/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { ActionTree } from 'vuex'
import { RootState } from '@/store'

export interface IProxyState {
  // nothing for now
}

const state = (): IProxyState => ({
  // nothing for now
})

export type ProxyUrlAction = (attachmentUrl: string) => Promise<string>

const actions: ActionTree<IProxyState, RootState> = {
  async proxyUrl (_, url: string): Promise<string> {
    return await this.$api.proxy.getUrlViaProxy(url)
  }
}

export default {
  namespaced: true,
  state,
  actions
}
