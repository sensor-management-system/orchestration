/*
  With this one we can filter for equality or ilike

  For example:
  {
      name: 'short_name',
      op: 'ilike',
      val: '%Boeken%'
  }
*/
export interface IFlaskJSONAPISimpleFilter {
  name: string,
  op: string,
  val: string
}

export type IFlaskJSONAPIFilter = IFlaskJSONAPISimpleFilter
