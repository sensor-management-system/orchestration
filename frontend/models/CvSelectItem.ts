/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
export interface ICvSelectItem {
  uri: string
  name: string
  definition: string
  id: string | null
}

export class CvSelectItem implements ICvSelectItem {
  uri: string
  name: string
  definition: string
  id: string | null

  constructor (data: ICvSelectItem) {
    this.uri = data.uri
    this.name = data.name
    this.definition = data.definition
    this.id = data.id
  }

  toString (): string {
    return this.name
  }
}

/**
  * checks wheter the value has a non-empty definition property
  *
  * @param {[TODO:type]} item - the item to check for
  * @returns {boolean} returns true when the definition property exists and is not falsy
  */
export function hasDefinition (value: { definition?: string }): boolean {
  return value && !!value.definition
}
