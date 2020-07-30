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
