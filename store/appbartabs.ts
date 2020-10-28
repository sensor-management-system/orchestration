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
export interface IAppbarTabsStore {
  tabs: string[],
  active: null | number
}

/**
 * The initial state of the AppbarTabsStore
 *
 * @return {IAppbarTabsStore} the state object
 */
export const state = (): IAppbarTabsStore => {
  return {
    tabs: [],
    active: null
  }
}

export const mutations = {
  /**
   * Sets the tabs for an AppBar
   *
   * When the tabs are set and are not empty, the active tab is set
   * automatically to the first tab
   *
   * @param {IAppbarTabsStore} state - the current state
   * @param {string[]} tabs - the tabs to set
   */
  setTabs (state: IAppbarTabsStore, tabs: string[]): void {
    state.tabs = tabs
    state.active = tabs.length > 0 ? 0 : null
  },
  /**
   * Sets the active tab
   *
   * When the tabs are empty or active is lt 0 or gt the length of the tabs,
   * active is set to null
   *
   * @param {IAppbarTabsStore} state - the current state
   * @param {null | number} active - the index of the active tab, null if none is selected
   */
  setActive (state: IAppbarTabsStore, active: null | number): void {
    // if the index of the active tab is out of range, set it to null
    if (!state.tabs.length || (active !== null && (active < 0 || active + 1 > state.tabs.length))) {
      active = null
    }
    state.active = active
  }
}
