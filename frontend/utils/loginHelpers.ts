/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Erik Pongratz (UFZ, erik.pongratz@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
 *   (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
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
import { Context } from '@nuxt/types'

/**
 * the key under which the route is stored in the localStorage
 */
export const AUTH_LOCAL_STORAGE_KEY_REDIRECT_URI = 'auth.login_callback_redirect_uri'

/**
 * saves a route in the localStorage
 *
 * @param {string} route - the route to save
 * @return {boolean} true when the route was sucessfully saved, otherwise false
 */
export const saveRoute = (route: string): boolean => {
  try {
    localStorage.setItem(AUTH_LOCAL_STORAGE_KEY_REDIRECT_URI, route)
  } catch (error) {
    return false
  }
  return true
}

/**
 * saves the current route in the localStorage
 *
 * @param {Context} context - a Nuxt context
 * @return {boolean} true when the route was sucessfully saved, otherwise false
 */
export const saveCurrentRoute = (context: Context): boolean => {
  return saveRoute(context.route.path)
}

/**
 * returns the saved route from the localStorage
 *
 * @return {string | boolean} returns the route, false if the route can't be found
 */
export const getSavedRoute = (): string | boolean => {
  const route = localStorage.getItem(AUTH_LOCAL_STORAGE_KEY_REDIRECT_URI)
  if (route) {
    return route
  }
  return false
}

/**
 * removes and returns the saved route from the localStorage
 *
 * @return {string | boolean} returns the route, false if the route can't be found
 */
export const removeSavedRoute = (): string | boolean => {
  const route = getSavedRoute()
  localStorage.removeItem(AUTH_LOCAL_STORAGE_KEY_REDIRECT_URI)
  return route
}
