/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Erik Pongratz <erik.pongratz@ufz.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { multiLineString } from '@turf/helpers'
import { lineToPolygon } from '@turf/turf'
import kinks from '@turf/kinks'
import { ILatLng } from '@/models/Site'

export function hasSelfIntersection (coords: ILatLng[]): boolean {
  if (coords.length > 2) {
    const coordsList = coords.map(coord => [coord.lng, coord.lat])
    const multiLine = multiLineString([coordsList])
    const testPolygon = lineToPolygon(multiLine)
    // @ts-ignore
    const testKinks = kinks(testPolygon)

    return testKinks.features.length > 0
  } else {
    return false
  }
}
