/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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
import { Commit, ActionTree } from 'vuex'
import { RootState } from '@/store'
import { TabItemConfiguration } from '@/models/TabItemConfiguration'

export interface IAppbarState {
  activeTab: null | number,
  cancelBtnDisabled: boolean,
  cancelBtnHidden: boolean,
  saveBtnDisabled: boolean,
  saveBtnHidden: boolean,
  tabs: TabItemConfiguration[],
  title: string
}

/**
 * The initial state of the AppbarTabsStore
 *
 * @return {IAppbarState} the state object
 */
const state = (): IAppbarState => {
  return {
    activeTab: null,
    cancelBtnDisabled: false,
    cancelBtnHidden: true,
    saveBtnDisabled: false,
    saveBtnHidden: true,
    tabs: [] as TabItemConfiguration[],
    title: ''
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
  /**
   * Hides or shows the save button
   *
   * @param {IAppbarState} state - the current state
   * @param {boolean} hidden - whether to hide or show the save button
   */
  setSaveBtnHidden (state: IAppbarState, hidden: boolean): void {
    state.saveBtnHidden = hidden
  },
  /**
   * Disables the save button
   *
   * @param {IAppbarState} state - the current state
   * @param {boolean} disabled - whether to hide or show the save button
   */
  setSaveBtnDisabled (state: IAppbarState, disabled: boolean): void {
    state.saveBtnDisabled = disabled
  },
  /**
   * Hides or shows the cancel button
   *
   * @param {IAppbarState} state - the current state
   * @param {boolean} hidden - whether to hide or show the cancel button
   */
  setCancelBtnHidden (state: IAppbarState, hidden: boolean): void {
    state.cancelBtnHidden = hidden
  },
  /**
   * Disables the cancel button
   *
   * @param {IAppbarState} state - the current state
   * @param {boolean} disabled - whether to hide or show the cancel button
   */
  setCancelBtnDisabled (state: IAppbarState, disabled: boolean): void {
    state.cancelBtnDisabled = disabled
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
export type SetSaveBtnHiddenAction = (hidden: boolean) => void
export type SetSaveBtnDisabledAction = (disabled: boolean) => void
export type SetCancelBtnHiddenAction = (hidden: boolean) => void
export type SetCancelBtnDisabledAction = (disabled: boolean) => void

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
    context.commit('setSaveBtnHidden', payload.saveBtnHidden || true)
    context.commit('setSaveBtnDisabled', payload.saveBtnDisabled || true)
    context.commit('setCancelBtnHidden', payload.cancelBtnHidden || true)
    context.commit('setCancelBtnDisabled', payload.cancelBtnDisabled || true)
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
  setSaveBtnHidden ({ commit }: { commit: Commit }, hidden: boolean): void {
    commit('setSaveBtnHidden', hidden)
  },
  setSaveBtnDisabled ({ commit }: { commit: Commit }, disabled: boolean): void {
    commit('setSaveBtnDisabled', disabled)
  },
  setCancelBtnHidden ({ commit }: { commit: Commit }, hidden: boolean): void {
    commit('setCancelBtnHidden', hidden)
  },
  setCancelBtnDisabled ({ commit }: { commit: Commit }, disabled: boolean): void {
    commit('setCancelBtnDisabled', disabled)
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations
}
