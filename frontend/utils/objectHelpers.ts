/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

type IObject = {[idx: string]: any}

// normally we would just the spread operator
export function mergeObjectsAndMaybeOverwrite (objects: IObject[]): IObject {
  return objects.reduce(function (r: IObject, o: IObject) {
    Object.keys(o || {}).forEach(function (k) {
      r[k] = o[k]
    })
    return r
  }, {})
}
