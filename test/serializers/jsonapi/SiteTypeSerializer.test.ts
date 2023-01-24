/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
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
import { SiteType } from '@/models/SiteType'
import { SiteTypeSerializer } from '@/serializers/jsonapi/SiteTypeSerializer'

describe('SiteTypeSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            category: null,
            definition: 'Foo Bar',
            note: null,
            provenance: null,
            provenance_uri: null,
            status: 'Accepted',
            term: 'Abandoned meander'
          },
          id: '1',
          links: {
            self: 'https://localhost.localdomain/cv/api/v1/sitetypes/55/'
          },
          relationships: {
            site_usage: {
              data: {
                type: 'SiteUsage',
                id: '6'
              }
            },
            global_provenance: {
              data: null
            }
          },
          type: 'SiteType'
        }, {
          attributes: {
            category: 'categ',
            definition: 'Foo Bar Baz',
            note: 'note',
            provenance: 'prov',
            provenance_uri: 'uri',
            status: 'Accepted',
            term: 'Agroforestry'
          },
          id: '2',
          links: {
            self: 'https://localhost.localdomain/cv/api/v1/sitetypes/4/'
          },
          relationships: {
            site_usage: {
              data: {
                type: 'SiteUsage',
                id: '1'
              }
            },
            global_provenance: {
              data: {
                id: '1',
                type: 'GlobalProvenance'
              }
            }
          },
          type: 'SiteType'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedSiteType1 = SiteType.createFromObject({
        id: '1',
        name: 'Abandoned meander',
        uri: 'https://localhost.localdomain/cv/api/v1/sitetypes/55/',
        definition: 'Foo Bar',
        siteUsageId: '6',
        category: '',
        note: '',
        provenance: '',
        provenanceUri: '',
        globalProvenanceId: null
      })
      const expectedSiteType2 = SiteType.createFromObject({
        id: '2',
        name: 'Agroforestry',
        uri: 'https://localhost.localdomain/cv/api/v1/sitetypes/4/',
        definition: 'Foo Bar Baz',
        siteUsageId: '1',
        category: 'categ',
        note: 'note',
        provenance: 'prov',
        provenanceUri: 'uri',
        globalProvenanceId: '1'
      })

      const serializer = new SiteTypeSerializer()

      const siteType = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(siteType)).toBeTruthy()
      expect(siteType.length).toEqual(2)
      expect(siteType[0]).toEqual(expectedSiteType1)
      expect(siteType[1]).toEqual(expectedSiteType2)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should transform the model to json payload', () => {
      const siteType = SiteType.createFromObject({
        id: '2',
        name: 'Agroforestry',
        uri: 'https://localhost.localdomain/cv/api/v1/sitetypes/4/',
        definition: 'Foo Bar Baz',
        siteUsageId: '1',
        category: 'categ',
        note: 'note',
        provenance: 'prov',
        provenanceUri: 'uri',
        globalProvenanceId: '1'
      })

      const expectedResult = {
        attributes: {
          category: 'categ',
          definition: 'Foo Bar Baz',
          note: 'note',
          provenance: 'prov',
          provenance_uri: 'uri',
          term: 'Agroforestry'
        },
        id: '2',
        relationships: {
          site_usage: {
            data: {
              type: 'SiteUsage',
              id: '1'
            }
          },
          global_provenance: {
            data: {
              id: '1',
              type: 'GlobalProvenance'
            }
          }
        },
        type: 'SiteType'
      }

      const serializer = new SiteTypeSerializer()
      const result = serializer.convertModelToJsonApiData(siteType)

      expect(result).toEqual(expectedResult)
    })
  })
})
