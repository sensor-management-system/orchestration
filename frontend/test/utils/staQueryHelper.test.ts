/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2025
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { getStaQueryStringByQueryParams } from '@/utils/staQueryHelper'

describe('getStaQueryStringByQueryParams', () => {
  it('should return valid query with filter parameter', () => {
    expect(getStaQueryStringByQueryParams({
      filter: 'foo eq bar'
    })).toEqual('?$filter=foo eq bar')
  })
  it('should return valid query with top parameter', () => {
    expect(getStaQueryStringByQueryParams({
      top: 42
    })).toEqual('?$top=42')
    expect(getStaQueryStringByQueryParams({
      top: '42'
    })).toEqual('?$top=42')
  })
  it('should return valid query with skip parameter', () => {
    expect(getStaQueryStringByQueryParams({
      skip: 42
    })).toEqual('?$skip=42')
    expect(getStaQueryStringByQueryParams({
      skip: '42'
    })).toEqual('?$skip=42')
  })
  it('should return valid query with flat select parameter', () => {
    expect(getStaQueryStringByQueryParams({
      select: ['@iot.selfLink', 'name', '@iot.id', 'properties']
    })).toEqual('?$select=@iot.selfLink,name,@iot.id,properties')
  })
  it('should return valid query with nested select parameter', () => {
    expect(getStaQueryStringByQueryParams({
      select: ['properties/jsonld.id']
    })).toEqual('?$select=properties/jsonld.id')
  })
  it('should return valid query with orderby parameter', () => {
    expect(getStaQueryStringByQueryParams({
      orderby: 'id asc'
    })).toEqual('?$orderby=id asc')
  })
  it('should return valid query with expand parameter', () => {
    expect(getStaQueryStringByQueryParams({
      expand: ['Datastreams', 'Things']
    })).toEqual('?$expand=Datastreams,Things')
  })
  it('should return valid query with count parameter', () => {
    expect(getStaQueryStringByQueryParams({
      count: true
    })).toEqual('?$count=true')
    expect(getStaQueryStringByQueryParams({
      count: false
    })).toEqual('?$count=false')
  })
  it('should return valid query with multiple parameters', () => {
    expect(getStaQueryStringByQueryParams({
      top: 42,
      select: ['name'],
      expand: ['Datastreams', 'Things']
    })).toEqual('?$top=42&$select=name&$expand=Datastreams,Things')
  })
})
