/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { Commit, ActionTree } from 'vuex'
import { RawLocation } from 'vue-router'
import { RootState } from '@/store'
import { TabItemConfiguration } from '@/models/TabItemConfiguration'

export interface IAppbarState {
  activeTab: null | number
  tabs: TabItemConfiguration[]
  title: string
  showBackButton: boolean
  backTo: RawLocation
}

/**
 * The initial state of the AppbarTabsStore
 *
 * @return {IAppbarState} the state object
 */
const state = (): IAppbarState => {
  return {
    activeTab: null,
    tabs: [] as TabItemConfiguration[],
    title: '',
    showBackButton: false,
    backTo: '' as RawLocation
  }
}

const mutations = {
  /**
   * Sets the title of the AppBar
   *
   * @param {IAppbarState} state - the current state
   * @param {string} title - the title of the AppBar
   */
  setTitle (state: IAppbarState, title: string): void {
    state.title = title
  },
  /**
   * Sets the tabs for an AppBar
   *
   * When the tabs are set and are not empty, the active tab is set
   * automatically to the first tab
   *
   * @param {IAppbarState} state - the current state
   * @param {string[]} tabs - the tabs to set
   */
  setTabs (state: IAppbarState, tabs: TabItemConfiguration[]): void {
    state.tabs = tabs
    state.activeTab = tabs.length > 0 ? 0 : null
  },
  /**
   * Sets the active tab
   *
   * When the tabs are empty or active is lt 0 or gt the length of the tabs,
   * active is set to null
   *
   * @param {IAppbarState} state - the current state
   * @param {null | number} active - the index of the active tab, null if none is selected
   */
  setActiveTab (state: IAppbarState, active: null | number): void {
    // if the index of the active tab is out of range, set it to null
    if (!state.tabs.length || (active !== null && (active < 0 || active + 1 > state.tabs.length))) {
      active = null
    }
    state.activeTab = active
  },
  setShowBackButton (state: IAppbarState, show: boolean): void {
    state.showBackButton = show
  },
  setBackTo (state: IAppbarState, to: RawLocation): void {
    state.backTo = to
  }
}

type StoreContext = {
  commit: (mutation: string, payload: any) => void,
  dispatch: (action: string, payload: any) => void
}

export type InitAction = (payload: Partial<IAppbarState>) => void
export type SetDefaultsAction = () => void
export type SetTitleAction = (title: string) => void
export type SetTabsAction = (tabs: TabItemConfiguration[]) => void
export type SetActiveTabAction = (active: null | number) => void
export type SetShowBackButtonAction = (show: boolean) => void
export type SetBackToAction = (to: RawLocation) => void

const actions: ActionTree<IAppbarState, RootState> = {
  /**
   * initializes the Appbar
   *
   * calls the mutations for every property in the payload
   *
   * @param {StoreContext} context - the context of the store
   * @param {Partial<IAppbarState>} payload - the payload which must be a partial of IAppbarStore
   */
  init (context: StoreContext, payload: Partial<IAppbarState>): void {
    context.commit('setTitle', payload.title || '')
    context.commit('setTabs', payload.tabs || [])
    context.commit('setActiveTab', payload.activeTab || null)
    context.commit('setShowBackButton', payload.showBackButton || false)
    context.commit('setBackTo', payload.backTo || '')
  },
  /**
   * sets the Appbar to its default settings
   *
   * @param {StoreContext} context - the context of the store
   */
  setDefaults (context: StoreContext): void {
    context.dispatch('init', state())
  },
  setTitle ({ commit }: { commit: Commit }, title: string): void {
    commit('setTitle', title)
  },
  setTabs ({ commit }: { commit: Commit }, tabs: TabItemConfiguration[]): void {
    commit('setTabs', tabs)
  },
  setActiveTab ({ commit }: { commit: Commit }, active: null | number): void {
    commit('setActiveTab', active)
  },
  setShowBackButton ({ commit }: { commit: Commit }, show: boolean): void {
    commit('setShowBackButton', show)
  },
  setBackTo ({ commit }: { commit: Commit }, to: RawLocation): void {
    commit('setBackTo', to)
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations
}
