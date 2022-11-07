/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2022
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
import { DateTime } from 'luxon'

import { Attachment } from '@/models/Attachment'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { Contact } from '@/models/Contact'

import {
  DeviceSoftwareUpdateActionSerializer,
  PlatformSoftwareUpdateActionSerializer
} from '@/serializers/jsonapi/SoftwareUpdateActionSerializer'

import {
  IJsonApiEntityEnvelope,
  IJsonApiEntityListEnvelope,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiRelationships
} from '@/serializers/jsonapi/JsonApiTypes'

describe('SoftwareUpdateActionSerializer', () => {
  function getExampleObjectResponse (): IJsonApiEntityEnvelope {
    return {
      data: {
        type: 'device_software_update_action',
        attributes: {
          software_type_name: 'Program',
          version: 'fe23f4afc12f234sd',
          software_type_uri: 'http://rz-vm64.gfz-potsdam.de:8000/api/v1/softwaretypes/2/',
          repository_url: 'https://foo/bar',
          update_date: '2021-07-01T00:00:00',
          description: 'Test',
          created_at: '2021-06-14T14:47:53.554867',
          updated_at: null
        },
        relationships: {
          device: {
            links: {
              self: '/rdm/svm-api/v1/device-software-update-actions/3/relationships/device',
              related: '/rdm/svm-api/v1/devices/204'
            },
            data: {
              type: 'device',
              id: '204'
            }
          },
          contact: {
            links: {
              self: '/rdm/svm-api/v1/device-software-update-actions/3/relationships/contact',
              related: '/rdm/svm-api/v1/contacts/14'
            },
            data: {
              type: 'contact',
              id: '14'
            }
          },
          device_software_update_action_attachments: {
            links: {
              related: '/rdm/svm-api/v1/device-software-update-actions/3/relationships/device-software-update-action-attachments'
            },
            data: [

            ]
          }
        },
        id: '3',
        links: {
          self: '/rdm/svm-api/v1/device-software-update-actions/3'
        }
      },
      links: {
        self: '/rdm/svm-api/v1/device-software-update-actions/3'
      },
      included: [
        {
          type: 'contact',
          attributes: {
            family_name: 'Hanisch',
            given_name: 'Marc',
            website: '',
            email: 'marc.hanisch@gfz-potsdam.de'
          },
          relationships: {
            devices: {
              links: {
                related: '/rdm/svm-api/v1/contacts/14/relationships/devices'
              },
              data: [
                {
                  type: 'device',
                  id: '250'
                }
              ]
            },
            configurations: {
              links: {
                related: '/rdm/svm-api/v1/contacts/14/relationships/configurations'
              },
              data: [

              ]
            },
            platforms: {
              links: {
                related: '/rdm/svm-api/v1/contacts/14/relationships/platforms'
              },
              data: [

              ]
            },
            user: {
              links: {
                self: '/rdm/svm-api/v1/contacts/14/relationships/user'
              },
              data: {
                type: 'user',
                id: '6'
              }
            }
          },
          id: '14',
          links: {
            self: '/rdm/svm-api/v1/contacts/14'
          }
        }
      ],
      jsonapi: {
        version: '1.0'
      }
    }
  }

  function getExampleObjectListResponse (): IJsonApiEntityListEnvelope {
    return {
      data: [
        {
          type: 'device_software_update_action',
          id: '2',
          relationships: {
            device: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-actions/2/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            },
            contact: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-actions/2/relationships/contact',
                related: '/rdm/svm-api/v1/contacts/3'
              },
              data: {
                type: 'contact',
                id: '3'
              }
            },
            device_software_update_action_attachments: {
              links: {
                related: '/rdm/svm-api/v1/device-software-update-actions/2/relationships/device-software-update-action-attachments'
              },
              data: [
                {
                  type: 'device_software_update_action_attachment',
                  id: '1'
                },
                {
                  type: 'device_software_update_action_attachment',
                  id: '2'
                },
                {
                  type: 'device_software_update_action_attachment',
                  id: '3'
                }
              ]
            }
          },
          attributes: {
            software_type_name: 'Firmware',
            repository_url: 'https://foo/bar/baz',
            description: 'Some simple description!!!',
            update_date: '2021-06-30T00:00:00',
            software_type_uri: 'http://rz-vm64.gfz-potsdam.de:8000/api/v1/softwaretypes/1/',
            version: '1.9',
            created_at: '2021-06-14T12:18:06.531875'
          },
          links: {
            self: '/rdm/svm-api/v1/device-software-update-actions/2'
          }
        },
        {
          type: 'device_software_update_action',
          id: '1',
          relationships: {
            device: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-actions/1/relationships/device',
                related: '/rdm/svm-api/v1/devices/256'
              },
              data: {
                type: 'device',
                id: '256'
              }
            },
            contact: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-actions/1/relationships/contact',
                related: '/rdm/svm-api/v1/contacts/14'
              },
              data: {
                type: 'contact',
                id: '14'
              }
            },
            device_software_update_action_attachments: {
              links: {
                related: '/rdm/svm-api/v1/device-software-update-actions/1/relationships/device-software-update-action-attachments'
              },
              data: [

              ]
            }
          },
          attributes: {
            software_type_name: 'Firmware',
            repository_url: 'https://foo.bar',
            description: 'Some description',
            update_date: '2021-06-03T00:00:00',
            software_type_uri: 'http://rz-vm64.gfz-potsdam.de:8000/api/v1/softwaretypes/1/',
            version: '1.3'
          },
          links: {
            self: '/rdm/svm-api/v1/device-software-update-actions/1'
          }
        }
      ],
      links: {
        self: 'http://rz-vm64.gfz-potsdam.de:5000/rdm/svm-api/v1/device-software-update-actions?include=contact%2Cdevice_software_update_action_attachments.attachment'
      },
      included: [
        {
          type: 'contact',
          id: '3',
          attributes: {
            family_name: 'Brinckmann',
            given_name: 'Nils',
            email: 'nils.brinckmann@gfz-potsdam.de',
            website: 'https://www.gfz-potsdam.de/staff/nils-brinckmann/'
          },
          relationships: {
            user: {
              links: {
                self: '/rdm/svm-api/v1/contacts/3/relationships/user'
              },
              data: {
                type: 'user',
                id: '3'
              }
            }
          },
          links: {
            self: '/rdm/svm-api/v1/contacts/3'
          }
        },
        {
          type: 'device_software_update_action_attachment',
          relationships: {
            action: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-action-attachments/1/relationships/action',
                related: '/rdm/svm-api/v1/device-software-update-action-attachments/2'
              },
              data: {
                type: 'device_software_update_action',
                id: '2'
              }
            },
            attachment: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-action-attachments/1/relationships/attachment',
                related: '/rdm/svm-api/v1/device-attachments/53'
              },
              data: {
                type: 'device_attachment',
                id: '53'
              }
            }
          },
          id: '1',
          links: {
            self: '/rdm/svm-api/v1/device-software-update-action-attachments/1'
          }
        },
        {
          type: 'device_attachment',
          id: '53',
          attributes: {
            label: 'GFZ',
            url: 'https://www.gfz-potsdam.de'
          },
          relationships: {
            device: {
              links: {
                self: '/rdm/svm-api/v1/device-attachments/53/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            }
          },
          links: {
            self: '/rdm/svm-api/v1/device-attachments/53'
          }
        },
        {
          type: 'device_software_update_action_attachment',
          relationships: {
            action: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-action-attachments/2/relationships/action',
                related: '/rdm/svm-api/v1/device-software-update-action-attachments/2'
              },
              data: {
                type: 'device_software_update_action',
                id: '2'
              }
            },
            attachment: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-action-attachments/2/relationships/attachment',
                related: '/rdm/svm-api/v1/device-attachments/52'
              },
              data: {
                type: 'device_attachment',
                id: '52'
              }
            }
          },
          id: '2',
          links: {
            self: '/rdm/svm-api/v1/device-software-update-action-attachments/2'
          }
        },
        {
          type: 'device_attachment',
          id: '52',
          attributes: {
            label: 'Bar.baz',
            url: 'https://bar.baz'
          },
          relationships: {
            device: {
              links: {
                self: '/rdm/svm-api/v1/device-attachments/52/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            }
          },
          links: {
            self: '/rdm/svm-api/v1/device-attachments/52'
          }
        },
        {
          type: 'device_software_update_action_attachment',
          relationships: {
            action: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-action-attachments/3/relationships/action',
                related: '/rdm/svm-api/v1/device-software-update-action-attachments/2'
              },
              data: {
                type: 'device_software_update_action',
                id: '2'
              }
            },
            attachment: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-action-attachments/3/relationships/attachment',
                related: '/rdm/svm-api/v1/device-attachments/51'
              },
              data: {
                type: 'device_attachment',
                id: '51'
              }
            }
          },
          id: '3',
          links: {
            self: '/rdm/svm-api/v1/device-software-update-action-attachments/3'
          }
        },
        {
          type: 'device_attachment',
          id: '51',
          attributes: {
            label: 'Foo.de',
            url: 'https://foo.de'
          },
          relationships: {
            device: {
              links: {
                self: '/rdm/svm-api/v1/device-attachments/51/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            }
          },
          links: {
            self: '/rdm/svm-api/v1/device-attachments/51'
          }
        },
        {
          type: 'contact',
          id: '14',
          attributes: {
            family_name: 'Hanisch',
            given_name: 'Marc',
            email: 'marc.hanisch@gfz-potsdam.de',
            website: ''
          },
          relationships: {
            user: {
              links: {
                self: '/rdm/svm-api/v1/contacts/14/relationships/user'
              },
              data: {
                type: 'user',
                id: '6'
              }
            }
          },
          links: {
            self: '/rdm/svm-api/v1/contacts/14'
          }
        }
      ],
      meta: {
        count: 2
      },
      jsonapi: {
        version: '1.0'
      }
    }
  }

  function getExampleDeviceResponse (): IJsonApiEntityEnvelope {
    return {
      data: {
        type: 'device',
        attributes: {
          persistent_identifier: null,
          manufacturer_name: 'OTT Hydromet GmbH',
          model: 'SM1',
          updated_at: '2021-04-26T09:03:01.944689',
          device_type_name: 'Frequency/Time Domain Reflectometer (FTDR)(Soil moisture and temperature)',
          long_name: 'Adcon SM 1 soil moisture / temperature sensor',
          short_name: 'Adcon SM1 soil moisture / temperature sensor FTDR Zeitlow 1',
          website: 'http://www.adcon.com',
          status_name: 'In Use',
          manufacturer_uri: 'OTT Hydromet GmbH',
          created_at: '2021-01-18T07:07:24.360000',
          serial_number: '',
          device_type_uri: '',
          dual_use: false,
          description: '',
          status_uri: 'http://rz-vm64.gfz-potsdam.de:8000/api/v1/equipmentstatus/2/',
          inventory_number: ''
        },
        relationships: {
          device_properties: {
            links: {
              related: '/rdm/svm-api/v1/devices/204/relationships/device-properties'
            },
            data: [
              {
                type: 'device_property',
                id: '150'
              }
            ]
          },
          contacts: {
            links: {
              related: '/rdm/svm-api/v1/devices/204/relationships/contacts'
            },
            data: [
              {
                type: 'contact',
                id: '10'
              },
              {
                type: 'contact',
                id: '21'
              }
            ]
          },
          device_software_update_actions: {
            links: {
              related: '/rdm/svm-api/v1/devices/204/relationships/device-software-update-actions'
            },
            data: [
              {
                type: 'device_software_update_action',
                id: '2'
              },
              {
                type: 'device_software_update_action',
                id: '3'
              }
            ]
          },
          device_attachments: {
            links: {
              related: '/rdm/svm-api/v1/devices/204/relationships/device-attachments'
            },
            data: [
              {
                type: 'device_attachment',
                id: '51'
              },
              {
                type: 'device_attachment',
                id: '52'
              },
              {
                type: 'device_attachment',
                id: '53'
              }
            ]
          }
        },
        id: '204',
        links: {
          self: '/rdm/svm-api/v1/devices/204'
        }
      },
      links: {
        self: '/rdm/svm-api/v1/devices/204'
      },
      included: [
        {
          type: 'device_software_update_action',
          id: '2',
          relationships: {
            device: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-actions/2/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            },
            contact: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-actions/2/relationships/contact',
                related: '/rdm/svm-api/v1/contacts/3'
              },
              data: {
                type: 'contact',
                id: '3'
              }
            },
            device_software_update_action_attachments: {
              links: {
                related: '/rdm/svm-api/v1/device-software-update-actions/2/relationships/device-software-update-action-attachments'
              },
              data: [
                {
                  type: 'device_software_update_action_attachment',
                  id: '1'
                },
                {
                  type: 'device_software_update_action_attachment',
                  id: '2'
                },
                {
                  type: 'device_software_update_action_attachment',
                  id: '3'
                }
              ]
            }
          },
          attributes: {
            software_type_name: 'Firmware',
            repository_url: 'https://foo/bar/baz',
            description: 'Some simple description!!!',
            updated_at: '2021-06-14T14:37:42.105091',
            update_date: '2021-06-30T00:00:00',
            software_type_uri: 'http://rz-vm64.gfz-potsdam.de:8000/api/v1/softwaretypes/1/',
            version: '1.9',
            created_at: '2021-06-14T12:18:06.531875'
          },
          links: {
            self: '/rdm/svm-api/v1/device-software-update-actions/2'
          }
        },
        {
          type: 'device_software_update_action',
          id: '3',
          relationships: {
            device: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-actions/3/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            },
            contact: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-actions/3/relationships/contact',
                related: '/rdm/svm-api/v1/contacts/14'
              },
              data: {
                type: 'contact',
                id: '14'
              }
            },
            device_software_update_action_attachments: {
              links: {
                related: '/rdm/svm-api/v1/device-software-update-actions/3/relationships/device-software-update-action-attachments'
              },
              data: [

              ]
            }
          },
          attributes: {
            software_type_name: 'Program',
            repository_url: '',
            description: 'Test',
            updated_at: null,
            update_date: '2021-07-01T00:00:00',
            software_type_uri: 'http://rz-vm64.gfz-potsdam.de:8000/api/v1/softwaretypes/2/',
            version: 'fe23f4afc12f234sd',
            created_at: '2021-06-14T14:47:53.554867'
          },
          links: {
            self: '/rdm/svm-api/v1/device-software-update-actions/3'
          }
        }
      ],
      jsonapi: {
        version: '1.0'
      }
    }
  }

  function getExampleObjectResponseWithIncludedActionAttachments (): IJsonApiEntityEnvelope {
    return {
      data: {
        type: 'device_software_update_action',
        id: '2',
        relationships: {
          device: {
            links: {
              self: '/rdm/svm-api/v1/device-software-update-actions/2/relationships/device',
              related: '/rdm/svm-api/v1/devices/204'
            },
            data: {
              type: 'device',
              id: '204'
            }
          },
          contact: {
            links: {
              self: '/rdm/svm-api/v1/device-software-update-actions/2/relationships/contact',
              related: '/rdm/svm-api/v1/contacts/3'
            },
            data: {
              type: 'contact',
              id: '3'
            }
          },
          device_software_update_action_attachments: {
            links: {
              related: '/rdm/svm-api/v1/device-software-update-actions/2/relationships/device-software-update-action-attachments'
            },
            data: [
              {
                type: 'device_software_update_action_attachment',
                id: '1'
              },
              {
                type: 'device_software_update_action_attachment',
                id: '2'
              },
              {
                type: 'device_software_update_action_attachment',
                id: '3'
              }
            ]
          }
        },
        attributes: {
          software_type_name: 'Firmware',
          repository_url: 'https://foo/bar/baz',
          description: 'Some simple description!!!',
          updated_at: '2021-06-14T14:37:42.105091',
          update_date: '2021-06-30T00:00:00',
          software_type_uri: 'http://rz-vm64.gfz-potsdam.de:8000/api/v1/softwaretypes/1/',
          version: '1.9',
          created_at: '2021-06-14T12:18:06.531875'
        },
        links: {
          self: '/rdm/svm-api/v1/device-software-update-actions/2'
        }
      },
      links: {
        self: '/rdm/svm-api/v1/device-software-update-actions/2'
      },
      included: [
        {
          type: 'contact',
          id: '3',
          attributes: {
            family_name: 'Brinckmann',
            given_name: 'Nils',
            email: 'nils.brinckmann@gfz-potsdam.de',
            website: 'https://www.gfz-potsdam.de/staff/nils-brinckmann/'
          },
          relationships: {
            user: {
              links: {
                self: '/rdm/svm-api/v1/contacts/3/relationships/user'
              },
              data: {
                type: 'user',
                id: '3'
              }
            }
          },
          links: {
            self: '/rdm/svm-api/v1/contacts/3'
          }
        },
        {
          type: 'device_software_update_action_attachment',
          relationships: {
            action: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-action-attachments/1/relationships/action',
                related: '/rdm/svm-api/v1/device-software-update-action-attachments/2'
              },
              data: {
                type: 'device_software_update_action',
                id: '2'
              }
            },
            attachment: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-action-attachments/1/relationships/attachment',
                related: '/rdm/svm-api/v1/device-attachments/53'
              },
              data: {
                type: 'device_attachment',
                id: '53'
              }
            }
          },
          id: '1',
          links: {
            self: '/rdm/svm-api/v1/device-software-update-action-attachments/1'
          }
        },
        {
          type: 'device_attachment',
          id: '53',
          attributes: {
            label: 'GFZ',
            url: 'https://www.gfz-potsdam.de'
          },
          relationships: {
            device: {
              links: {
                self: '/rdm/svm-api/v1/device-attachments/53/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            }
          },
          links: {
            self: '/rdm/svm-api/v1/device-attachments/53'
          }
        },
        {
          type: 'device_software_update_action_attachment',
          relationships: {
            action: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-action-attachments/2/relationships/action',
                related: '/rdm/svm-api/v1/device-software-update-action-attachments/2'
              },
              data: {
                type: 'device_software_update_action',
                id: '2'
              }
            },
            attachment: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-action-attachments/2/relationships/attachment',
                related: '/rdm/svm-api/v1/device-attachments/52'
              },
              data: {
                type: 'device_attachment',
                id: '52'
              }
            }
          },
          id: '2',
          links: {
            self: '/rdm/svm-api/v1/device-software-update-action-attachments/2'
          }
        },
        {
          type: 'device_attachment',
          id: '52',
          attributes: {
            label: 'Bar.baz',
            url: 'https://bar.baz'
          },
          relationships: {
            device: {
              links: {
                self: '/rdm/svm-api/v1/device-attachments/52/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            }
          },
          links: {
            self: '/rdm/svm-api/v1/device-attachments/52'
          }
        },
        {
          type: 'device_software_update_action_attachment',
          relationships: {
            action: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-action-attachments/3/relationships/action',
                related: '/rdm/svm-api/v1/device-software-update-action-attachments/2'
              },
              data: {
                type: 'device_software_update_action',
                id: '2'
              }
            },
            attachment: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-action-attachments/3/relationships/attachment',
                related: '/rdm/svm-api/v1/device-attachments/51'
              },
              data: {
                type: 'device_attachment',
                id: '51'
              }
            }
          },
          id: '3',
          links: {
            self: '/rdm/svm-api/v1/device-software-update-action-attachments/3'
          }
        },
        {
          type: 'device_attachment',
          id: '51',
          attributes: {
            label: 'Foo.de',
            url: 'https://foo.de'
          },
          relationships: {
            device: {
              links: {
                self: '/rdm/svm-api/v1/device-attachments/51/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            }
          },
          links: {
            self: '/rdm/svm-api/v1/device-attachments/51'
          }
        }
      ],
      jsonapi: {
        version: '1.0'
      }
    }
  }

  describe('DeviceSoftwareUpdateActionSerializer', () => {
    describe('constructing and types', () => {
      it('should return \'device\' as its type', () => {
        const serializer = new DeviceSoftwareUpdateActionSerializer()
        expect(serializer.targetType).toEqual('device')
      })
      it('should return a correct action type name', () => {
        const serializer = new DeviceSoftwareUpdateActionSerializer()
        expect(serializer.getActionTypeName()).toEqual('device_software_update_action')
      })
      it('should return a the plural form of the action type name', () => {
        const serializer = new DeviceSoftwareUpdateActionSerializer()
        expect(serializer.getActionTypeNamePlural()).toEqual('device_software_update_actions')
      })
      it('should return a correction action attachment type name', () => {
        const serializer = new DeviceSoftwareUpdateActionSerializer()
        expect(serializer.getActionAttachmentTypeName()).toEqual('device_software_update_action_attachment')
      })
    })
    describe('#convertJsonApiObjectToModel', () => {
      it('should return a serialized software update action from an API response', () => {
        const contact = Contact.createFromObject({
          id: '14',
          givenName: 'Marc',
          familyName: 'Hanisch',
          email: 'marc.hanisch@gfz-potsdam.de',
          website: ''
        })
        const expectedAction = new SoftwareUpdateAction()
        expectedAction.id = '3'
        expectedAction.description = 'Test'
        expectedAction.softwareTypeName = 'Program'
        expectedAction.softwareTypeUrl = 'http://rz-vm64.gfz-potsdam.de:8000/api/v1/softwaretypes/2/'
        expectedAction.updateDate = DateTime.fromISO('2021-07-01T00:00:00', { zone: 'UTC' })
        expectedAction.contact = contact
        expectedAction.version = 'fe23f4afc12f234sd'
        expectedAction.repositoryUrl = 'https://foo/bar'

        const serializer = new DeviceSoftwareUpdateActionSerializer()
        const action = serializer.convertJsonApiObjectToModel(getExampleObjectResponse())

        expect(action).toEqual(expectedAction)
      })
    })
    describe('#convertJsonApiDataToModel', () => {
      it('should return a serialized software update action from an API response object', () => {
        const contact = Contact.createFromObject({
          id: '14',
          givenName: 'Marc',
          familyName: 'Hanisch',
          email: 'marc.hanisch@gfz-potsdam.de',
          website: ''
        })
        const expectedAction = new SoftwareUpdateAction()
        expectedAction.id = '3'
        expectedAction.description = 'Test'
        expectedAction.softwareTypeName = 'Program'
        expectedAction.softwareTypeUrl = 'http://rz-vm64.gfz-potsdam.de:8000/api/v1/softwaretypes/2/'
        expectedAction.updateDate = DateTime.fromISO('2021-07-01T00:00:00', { zone: 'UTC' })
        expectedAction.contact = contact
        expectedAction.version = 'fe23f4afc12f234sd'
        expectedAction.repositoryUrl = 'https://foo/bar'

        const serializer = new DeviceSoftwareUpdateActionSerializer()
        const data = getExampleObjectResponse().data
        const included = getExampleObjectResponse().included
        const action = serializer.convertJsonApiDataToModel(data, included as IJsonApiEntityWithOptionalAttributes[])

        expect(action).toEqual(expectedAction)
      })
    })
    describe('#convertJsonApiRelationshipsModelList', () => {
      it('should return a serialized list of software update actions from an list of included API entities', () => {
        const serializer = new DeviceSoftwareUpdateActionSerializer()
        const response = getExampleDeviceResponse()

        const relationships = response.data.relationships
        const included = response.included

        const expectedAction1 = new SoftwareUpdateAction()
        expectedAction1.id = '2'
        expectedAction1.description = 'Some simple description!!!'
        expectedAction1.softwareTypeName = 'Firmware'
        expectedAction1.softwareTypeUrl = 'http://rz-vm64.gfz-potsdam.de:8000/api/v1/softwaretypes/1/'
        expectedAction1.updateDate = DateTime.fromISO('2021-06-30T00:00:00', { zone: 'UTC' })
        expectedAction1.version = '1.9'
        expectedAction1.repositoryUrl = 'https://foo/bar/baz'

        const expectedAction2 = new SoftwareUpdateAction()
        expectedAction2.id = '3'
        expectedAction2.description = 'Test'
        expectedAction2.softwareTypeName = 'Program'
        expectedAction2.softwareTypeUrl = 'http://rz-vm64.gfz-potsdam.de:8000/api/v1/softwaretypes/2/'
        expectedAction2.updateDate = DateTime.fromISO('2021-07-01T00:00:00', { zone: 'UTC' })
        expectedAction2.version = 'fe23f4afc12f234sd'
        expectedAction2.repositoryUrl = ''

        const actionList = serializer.convertJsonApiRelationshipsModelList(relationships as IJsonApiRelationships, included as IJsonApiEntityWithOptionalAttributes[])

        expect(actionList).toHaveProperty('softwareUpdateActions')
        expect(actionList.softwareUpdateActions).toContainEqual(expectedAction1)
        expect(actionList.softwareUpdateActions).toContainEqual(expectedAction2)
      })
    })
    describe('#convertJsonApiObjectListToModelList', () => {
      it('should return a list of serialized software update actions from an API response', () => {
        const contact1 = Contact.createFromObject({
          id: '14',
          givenName: 'Marc',
          familyName: 'Hanisch',
          email: 'marc.hanisch@gfz-potsdam.de',
          website: ''
        })
        const contact2 = Contact.createFromObject({
          id: '3',
          givenName: 'Nils',
          familyName: 'Brinckmann',
          email: 'nils.brinckmann@gfz-potsdam.de',
          website: 'https://www.gfz-potsdam.de/staff/nils-brinckmann/'
        })
        const attachment1 = Attachment.createFromObject({
          id: '51',
          label: 'Foo.de',
          url: 'https://foo.de',
          isUpload: false
        })
        const attachment2 = Attachment.createFromObject({
          id: '52',
          label: 'Bar.baz',
          url: 'https://bar.baz',
          isUpload: false
        })
        const attachment3 = Attachment.createFromObject({
          id: '53',
          label: 'GFZ',
          url: 'https://www.gfz-potsdam.de',
          isUpload: false
        })

        const expectedAction1 = new SoftwareUpdateAction()
        expectedAction1.id = '2'
        expectedAction1.description = 'Some simple description!!!'
        expectedAction1.softwareTypeName = 'Firmware'
        expectedAction1.softwareTypeUrl = 'http://rz-vm64.gfz-potsdam.de:8000/api/v1/softwaretypes/1/'
        expectedAction1.updateDate = DateTime.fromISO('2021-06-30T00:00:00', { zone: 'UTC' })
        expectedAction1.version = '1.9'
        expectedAction1.repositoryUrl = 'https://foo/bar/baz'
        expectedAction1.contact = contact2
        expectedAction1.attachments = [
          attachment3,
          attachment2,
          attachment1
        ]

        const expectedAction2 = new SoftwareUpdateAction()
        expectedAction2.id = '1'
        expectedAction2.description = 'Some description'
        expectedAction2.softwareTypeName = 'Firmware'
        expectedAction2.softwareTypeUrl = 'http://rz-vm64.gfz-potsdam.de:8000/api/v1/softwaretypes/1/'
        expectedAction2.updateDate = DateTime.fromISO('2021-06-03T00:00:00', { zone: 'UTC' })
        expectedAction2.version = '1.3'
        expectedAction2.repositoryUrl = 'https://foo.bar'
        expectedAction2.contact = contact1

        const serializer = new DeviceSoftwareUpdateActionSerializer()
        const actionList = serializer.convertJsonApiObjectListToModelList(getExampleObjectListResponse())

        expect(actionList).toContainEqual(expectedAction1)
        expect(actionList).toContainEqual(expectedAction2)
      })
    })
    describe('#convertModelToJsonApiData', () => {
      it('should return a JSON API representation from a software update action model', () => {
        const contact = Contact.createFromObject({
          id: '14',
          givenName: 'Marc',
          familyName: 'Hanisch',
          email: 'marc.hanisch@gfz-potsdam.de',
          website: ''
        })

        const action = new SoftwareUpdateAction()
        action.id = '7'
        action.description = 'Bla'
        action.softwareTypeName = 'Firmware'
        action.softwareTypeUrl = 'https://foo/bar'
        action.updateDate = DateTime.fromISO('2021-05-23T00:00:00', { zone: 'UTC' })
        action.version = '10.2'
        action.repositoryUrl = 'https://git.gfz-potsdam.de/sms/frontend'
        action.contact = contact

        const expectedApiModel: IJsonApiEntityWithOptionalId = {
          type: 'device_software_update_action',
          id: '7',
          attributes: {
            description: 'Bla',
            software_type_name: 'Firmware',
            software_type_uri: 'https://foo/bar',
            update_date: '2021-05-23T00:00:00.000Z',
            version: '10.2',
            repository_url: 'https://git.gfz-potsdam.de/sms/frontend'
          },
          relationships: {
            device: {
              data: {
                type: 'device',
                id: '204'
              }
            },
            contact: {
              data: {
                type: 'contact',
                id: '14'
              }
            }
          }
        }

        const serializer = new DeviceSoftwareUpdateActionSerializer()
        const apiModel = serializer.convertModelToJsonApiData(action, '204')

        expect(apiModel).toEqual(expectedApiModel)
      })
    })
    describe('#convertModelToJsonApiRelationshipObject', () => {
      it('should return a JSON API relationships object from a software update action model', () => {
        const action = new SoftwareUpdateAction()
        action.id = '7'

        const expectedRelationship: IJsonApiRelationships = {
          device_software_update_action: {
            data: {
              id: '7',
              type: 'device_software_update_action'
            }
          }
        }
        const serializer = new DeviceSoftwareUpdateActionSerializer()
        const apiRelationship = serializer.convertModelToJsonApiRelationshipObject(action)

        expect(apiRelationship).toEqual(expectedRelationship)
      })
    })
    describe('#convertJsonApiIncludedActionAttachmentsToIdList', () => {
      it('should return a list of device_software_update_action_attachment ids / attachment ids mappings', () => {
        const expectedMappings = [
          {
            softwareUpdateActionAttachmentId: '1',
            attachmentId: '53'
          },
          {
            softwareUpdateActionAttachmentId: '2',
            attachmentId: '52'
          },
          {
            softwareUpdateActionAttachmentId: '3',
            attachmentId: '51'
          }
        ]
        const serializer = new DeviceSoftwareUpdateActionSerializer()
        const data = getExampleObjectResponseWithIncludedActionAttachments()
        const mappings = serializer.convertJsonApiIncludedActionAttachmentsToIdList(data.included as IJsonApiEntityWithOptionalAttributes[])

        expect(mappings).toEqual(expectedMappings)
      })
    })
  })

  describe('PlatformSoftwareUpdateActionSerializer', () => {
    describe('constructing and types', () => {
      it('should return \'platform\' as its type', () => {
        const serializer = new PlatformSoftwareUpdateActionSerializer()
        expect(serializer.targetType).toEqual('platform')
      })
      it('should return a correct action type name', () => {
        const serializer = new PlatformSoftwareUpdateActionSerializer()
        expect(serializer.getActionTypeName()).toEqual('platform_software_update_action')
      })
      it('should return a the plural form of the action type name', () => {
        const serializer = new PlatformSoftwareUpdateActionSerializer()
        expect(serializer.getActionTypeNamePlural()).toEqual('platform_software_update_actions')
      })
      it('should return a correction action attachment type name', () => {
        const serializer = new PlatformSoftwareUpdateActionSerializer()
        expect(serializer.getActionAttachmentTypeName()).toEqual('platform_software_update_action_attachment')
      })
    })
  })
})
