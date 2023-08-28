/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2022
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
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
