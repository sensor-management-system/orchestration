/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Erik Pongratz <erik.pongratz@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
