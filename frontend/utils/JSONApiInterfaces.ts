/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
  // We really want to do a possible recursive type definition here
  // eslint-disable-next-line no-use-before-define
  or: IFlaskJSONAPIFilter[]
}

export type IFlaskJSONAPIFilter =
  IFlaskJSONAPISimpleFilter |
  IFlaskJSONAPIOrFilter |
  IFlaskJSONAPISimpleGroupFilter
