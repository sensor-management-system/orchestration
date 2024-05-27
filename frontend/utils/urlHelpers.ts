/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

export function removeBaseUrl (url: string, baseUrl: string | undefined): string {
  if (!baseUrl) {
    return url
  }
  const splitted = url.split(baseUrl)
  const canditate = splitted[splitted.length - 1]

  // now also remove a first slash if necessary, as well as a trailing slash
  return removeFirstSlash(removeTrailingSlash(canditate))
}

export function removeFirstSlash (str: string): string {
  if (str.startsWith('/')) {
    return str.substring(1)
  }
  return str
}

export function removeTrailingSlash (str: string): string {
  if (str.endsWith('/')) {
    return str.substring(0, str.length - 1)
  }
  return str
}

export function getLastPathElement (str: string): string {
  const cleanedUrl = removeTrailingSlash(str)
  const splitted = cleanedUrl.split('/')
  return splitted[splitted.length - 1]
}

export function toRouterPath (callbackUri: string, routeBase = '/') {
  if (callbackUri) {
    const domainStartsAt = '://'
    const hostAndPath = callbackUri.substr(callbackUri.indexOf(domainStartsAt) + domainStartsAt.length)
    const routeBaseLength = routeBase === '/' ? 0 : routeBase.length
    return hostAndPath.substr(hostAndPath.indexOf(routeBase) + routeBaseLength)
  }
  return null
}

/**
 * checks whether the url contains the given protocols
 *
 * to be honest, it just checks whether the string starts with http(s):// or similar
 *
 * @param {string[]} allowedProtocols - the protocols to check
 * @param {string} url - the url to check
 * @returns {boolean | string} true when protocols are in the url, otherwise false
 */
export function protocolsInUrl (allowedProtocols: string[], url: string) {
  const protocols = allowedProtocols.join('|')
  const urlRegExp = new RegExp('^(' + protocols + ')://.+$', 'i')
  if (url && !url.match(urlRegExp)) {
    return false
  }
  return true
}
