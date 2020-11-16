/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
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

export function toRouterPath (callbackUri: string, routeBase = '/') {
  if (callbackUri) {
    const domainStartsAt = '://'
    const hostAndPath = callbackUri.substr(callbackUri.indexOf(domainStartsAt) + domainStartsAt.length)
    const routeBaseLength = routeBase === '/' ? 0 : routeBase.length
    return hostAndPath.substr(hostAndPath.indexOf(routeBase) + routeBaseLength)
  }
  return null
}
