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
import { TabItemConfiguration } from '@/models/TabItemConfiguration'
import {Commit} from 'vuex'

export interface IAppbarStore {
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
 * @return {IAppbarStore} the state object
 */
export const state = (): IAppbarStore => {
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

export const mutations = {
  /**
   * Sets the title of the AppBar
   *
   * @param {IAppbarStore} state - the current state
   * @param {string} title - the title of the AppBar
   */
  setTitle (state: IAppbarStore, title: string): void {
    state.title = title
  },
  /**
   * Sets the tabs for an AppBar
   *
   * When the tabs are set and are not empty, the active tab is set
   * automatically to the first tab
   *
   * @param {IAppbarStore} state - the current state
   * @param {string[]} tabs - the tabs to set
   */
  setTabs (state: IAppbarStore, tabs: TabItemConfiguration[]): void {
    state.tabs = tabs
    state.activeTab = tabs.length > 0 ? 0 : null
  },
  /**
   * Sets the active tab
   *
   * When the tabs are empty or active is lt 0 or gt the length of the tabs,
   * active is set to null
   *
   * @param {IAppbarStore} state - the current state
   * @param {null | number} active - the index of the active tab, null if none is selected
   */
  setActiveTab (state: IAppbarStore, active: null | number): void {
    // if the index of the active tab is out of range, set it to null
    if (!state.tabs.length || (active !== null && (active < 0 || active + 1 > state.tabs.length))) {
      active = null
    }
    state.activeTab = active
  },
  /**
   * Hides or shows the save button
   *
   * @param {IAppbarStore} state - the current state
   * @param {boolean} hidden - whether to hide or show the save button
   */
  setSaveBtnHidden (state: IAppbarStore, hidden: boolean): void {
    state.saveBtnHidden = hidden
  },
  /**
   * Disables the save button
   *
   * @param {IAppbarStore} state - the current state
   * @param {boolean} disabled - whether to hide or show the save button
   */
  setSaveBtnDisabled (state: IAppbarStore, disabled: boolean): void {
    state.saveBtnDisabled = disabled
  },
  /**
   * Hides or shows the cancel button
   *
   * @param {IAppbarStore} state - the current state
   * @param {boolean} hidden - whether to hide or show the cancel button
   */
  setCancelBtnHidden (state: IAppbarStore, hidden: boolean): void {
    state.cancelBtnHidden = hidden
  },
  /**
   * Disables the cancel button
   *
   * @param {IAppbarStore} state - the current state
   * @param {boolean} disabled - whether to hide or show the cancel button
   */
  setCancelBtnDisabled (state: IAppbarStore, disabled: boolean): void {
    state.cancelBtnDisabled = disabled
  }
}

type StoreContext = {
  commit: (mutation: string, payload: any) => void,
  dispatch: (action: string, payload: any) => void
}

export const actions = {
  /**
   * initializes the Appbar
   *
   * calls the mutations for every property in the payload
   *
   * @param {StoreContext} context - the context of the store
   * @param {Partial<IAppbarStore>} payload - the payload which must be a partial of IAppbarStore
   */
  init (context: StoreContext, payload: Partial<IAppbarStore>): void {
    if (typeof payload.title !== 'undefined') {
      context.commit('setTitle', payload.title)
    }
    if (typeof payload.tabs !== 'undefined') {
      context.commit('setTabs', payload.tabs)
    }
    if (typeof payload.activeTab !== 'undefined') {
      context.commit('setActiveTab', payload.activeTab)
    }
    if (typeof payload.saveBtnHidden !== 'undefined') {
      context.commit('setSaveBtnHidden', payload.saveBtnHidden)
    }
    if (typeof payload.saveBtnDisabled !== 'undefined') {
      context.commit('setSaveBtnDisabled', payload.saveBtnDisabled)
    }
    if (typeof payload.cancelBtnHidden !== 'undefined') {
      context.commit('setCancelBtnHidden', payload.cancelBtnHidden)
    }
    if (typeof payload.cancelBtnDisabled !== 'undefined') {
      context.commit('setCancelBtnDisabled', payload.cancelBtnDisabled)
    }
  },
  initContactsIndexAppBar({commit}:{commit:Commit}){
    commit('setTitle','Contacts');
    commit('setTabs',[])
    commit('setCancelBtnHidden',true)
    commit('setSaveBtnHidden',true)
  },
  initPlatformsIndexAppBar({commit}:{commit:Commit}){
    commit('setTitle','Platforms');
    commit('setTabs',[
      'Search',
      'Extended Search'
    ])
    commit('setCancelBtnHidden',true)
    commit('setSaveBtnHidden',true)
  },
  initDevicesIndexAppBar({commit}:{commit:Commit}){
    commit('setTitle','Devices');
    commit('setTabs',[
      'Search',
      'Extended Search'
    ])
    commit('setCancelBtnHidden',true)
    commit('setSaveBtnHidden',true)
  },
  initConfigurationsIndexAppBar({commit}:{commit:Commit}){
    commit('setTitle','Configurations');
    commit('setTabs',[
      'Search',
      'Extended Search'
    ])
    commit('setCancelBtnHidden',true)
    commit('setSaveBtnHidden',true)
  },
  initContactsNewAppBar({commit}:{commit:Commit}){
    commit('setTitle','Add Contact');
    commit('setTabs',[])
    commit('setCancelBtnHidden',true)
    commit('setSaveBtnHidden',true)
  },
  initPlatformsNewAppBar({commit}:{commit:Commit}){
    commit('setTitle','Add Platform');
    commit('setTabs',[
      {
        to: '/platforms/new',
        name: 'Basic Data'
      },
      {
        name: 'Contacts',
        disabled: true
      },
      {
        name: 'Attachments',
        disabled: true
      }
    ])
    commit('setCancelBtnHidden',true)
    commit('setSaveBtnHidden',true)
  },
  initDevicesNewAppBar({commit}:{commit:Commit}){
    commit('setTitle','Add Device');
    commit('setTabs',[
      {
        to: '/devices/new',
        name: 'Basic Data'
      },
      {
        name: 'Contacts',
        disabled: true
      },
      {
        name: 'Measured Quantities',
        disabled: true
      },
      {
        name: 'Custom Fields',
        disabled: true
      },
      {
        name: 'Attachments',
        disabled: true
      },
      {
        name: 'Actions',
        disabled: true
      }
    ])
    commit('setCancelBtnHidden',true)
    commit('setSaveBtnHidden',true)
  },
  initConfigurationsNewAppBar({commit}:{commit:Commit}){
    commit('setTitle','Add Configuration');
    commit('setTabs',[
      {
        to: '/configurations/new',
        name: 'Basic Data'
      },
      {
        name: 'Contacts',
        disabled: true
      },
      {
        name: 'Platforms and Devices',
        disabled: true
      },
      {
        name: 'Locations',
        disabled: true
      },
      {
        name: 'Actions',
        disabled: true
      }
    ])
    commit('setCancelBtnHidden',true)
    commit('setSaveBtnHidden',true)
  },

  /**
   * sets the Appbar to its default settings
   *
   * @param {StoreContext} context - the context of the store
   */
  setDefaults (context: StoreContext): void {
    context.dispatch('init', state())
  }
}
