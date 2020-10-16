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

/*
  With this one we can filter for equality or ilike

  For example:
  {
      name: 'short_name',
      op: 'ilike',
      val: '%Boeken%'
  }
*/

// see here for more
// https://flask-rest-jsonapi.readthedocs.io/en/latest/filtering.html
export type IFlaskJSONAPISimpleFilterOp =
  'like' | 'ilike' | 'notilike' | 'notlike'| 'eq' | 'ne' | 'ge' | 'gt' | 'le' | 'lt'

export type IFlaskJSONAPIGroupFilterOp =
  'in_' | 'notin_'

export interface IFlaskJSONAPISimpleFilter {
  name: string,
  op: IFlaskJSONAPISimpleFilterOp,
  val: string
}

export interface IFlaskJSONAPISimpleGroupFilter {
  name: string,
  op: IFlaskJSONAPIGroupFilterOp,
  val: string[]
}

export interface IFlaskJSONAPIOrFilter {
  or: IFlaskJSONAPIFilter[]
}

export type IFlaskJSONAPIFilter =
  IFlaskJSONAPISimpleFilter |
  IFlaskJSONAPIOrFilter |
  IFlaskJSONAPISimpleGroupFilter
