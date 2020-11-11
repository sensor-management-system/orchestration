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

/* The following comment should indicate how an json api response can look like:

      const jsonApiObject: any = {
        data: {
          type: 'device',
          attributes: {
            serial_number: '0000001',
            properties: [{
              compartment_name: 'Climate',
              unit_uri: '',
              sampling_media_name: 'Other',
              compartment_uri: 'variabletype/Climate',
              property_name: 'Water vapor concentration',
              accuracy: null,
              measuring_range_min: null,
              measuring_range_max: null,
              label: 'water vapor',
              property_uri: 'variablename/Water%20vapor%20concentration',
              id: '39',
              unit_name: '',
              failure_value: null,
              sampling_media_uri: 'medium/Other'
            }, {
              compartment_name: 'a',
              unit_uri: 'b',
              sampling_media_name: 'c',
              compartment_uri: 'd',
              property_name: 'e',
              accuracy: 1,
              measuring_range_min: 2,
              measuring_range_max: 3,
              label: 'f',
              property_uri: 'g',
              id: '40',
              unit_name: 'j',
              failure_value: 4,
              sampling_media_uri: 'k'
            }],
            device_type_name: null,
            model: 'test model',
            description: 'My first test device',
            attachments: [{
              label: 'test label',
              url: 'http://test.test',
              id: '1'
            }],
            status_uri: null,
            website: null,
            updated_at: '2020-08-28T13:00:46.295058+00:00',
            long_name: 'Device long name',
            created_at: '2020-08-28T13:00:46.295058+00:00',
            inventory_number: '0000001',
            manufacturer_name: null,
            device_type_uri: null,
            customfields: [{
              id: '44',
              key: 'a',
              value: 'b'
            }],
            short_name: 'Device short name',
            status_name: null,
            dual_use: true,
            persistent_identifier: '0000001',
            manufacturer_uri: null
          },
          relationships: {
            updated_by: {
              links: {
                self: '/rdm/svm-api/v1/devices/1/relationships/updatedUser'
              }
            },
            contacts: {
              links: {
                self: '/rdm/svm-api/v1/devices/1/relationships/contacts',
                related: '/rdm/svm-api/v1/devices/1/contacts'
              },
              data: [{
                type: 'contact',
                id: '1'
              }]
            },
            events: {
              links: {
                self: '/rdm/svm-api/v1/devices/1/relationships/events',
                related: '/rdm/svm-api/v1/events?device_id=1'
              }
            },
            created_by: {
              links: {
                self: '/rdm/svm-api/v1/devices/1/relationships/createdUser',
                related: '/rdm/svm-api/v1/users/1'
              }
            }
          },
          id: '1',
          links: {
            self: '/rdm/svm-api/v1/devices/1'
          }
        },
        links: {
          self: '/rdm/svm-api/v1/devices/1'
        },
        included: [{
          type: 'contact',
          relationships: {
            configurations: {
              links: {
                self: '/rdm/svm-api/v1/contacts/1/relationships/configurations',
                related: '/rdm/svm-api/v1/configurations?contact_id=1'
              }
            },
            user: {
              links: {
                self: '/rdm/svm-api/v1/contacts/1/relationships/user',
                related: '/rdm/svm-api/v1/contacts/1/users'
              },
              data: {
                type: 'user',
                id: '[<User 1>]'
              }
            },
            devices: {
              links: {
                self: '/rdm/svm-api/v1/contacts/1/relationships/devices',
                related: '/rdm/svm-api/v1/devices?contact_id=1'
              }
            },
            platforms: {
              links: {
                self: '/rdm/svm-api/v1/contacts/1/relationships/platforms',
                related: '/rdm/svm-api/v1/contacts/1/platforms'
              }
            }
          },
          attributes: {
            given_name: 'Max',
            email: 'test@test.test',
            website: null,
            family_name: 'Mustermann'
          },
          id: '1',
          links: {
            self: '/rdm/svm-api/v1/contacts/1'
          }
        }],
        jsonapi: {
          version: '1.0'
        }
      }

  The data can also be an array in case that we query for a list (of devices
  in this example).

  We don't want to use the full set of attributes given by the json api - just
  the amount that is necessary to extract or store all the information that
  we currenlty work with.

  There may also be schemas out there for a json api as well.
*/

export type IJsonApiAttributes = {[idx: string]: any }

export interface IJsonApiLinkDict {
    self: string
}

export type IJsonApiNestedElement = {[idx: string]: any}

export interface IJsonApiTypeId {
    type: string
    id: string
}

export interface IJsonApiTypeIdDataList {
    data: IJsonApiTypeId[]
}

export type IJsonApiTypeIdDataListDict = {[idx: string]: IJsonApiTypeIdDataList}

export interface IJsonApiData {
    attributes: IJsonApiAttributes
    type: string
    relationships: IJsonApiTypeIdDataListDict
}

export interface IJsonApiDataWithOptionalId extends IJsonApiData {
    id?: string
}

export interface IJsonApiDataWithId extends IJsonApiData {
    id: string
}

export interface IJsonApiDataWithIdAndLinks extends IJsonApiDataWithId {
    links: IJsonApiLinkDict
}

export interface IJsonApiTypeIdAttributes extends IJsonApiTypeId {
    attributes: IJsonApiAttributes
}

export interface IJsonApiTypeIdAttributesWithOptionalRelationships extends IJsonApiTypeIdAttributes {
    relationships?: IJsonApiTypeIdDataListDict
}

export interface IJsonApiObject {
    data: IJsonApiDataWithId
    included: IJsonApiTypeIdAttributes[]
}

export interface IJsonApiObjectList {
    data: IJsonApiDataWithId[],
    included: IJsonApiTypeIdAttributes[]
}

export interface IJsonApiObjectListWithLinks {
    data: IJsonApiDataWithIdAndLinks[]
}
