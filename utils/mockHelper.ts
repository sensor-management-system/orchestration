import { DateTime } from 'luxon'

function * idGenerator (index: number) {
  while(true){
    yield index.toString()
    index++
  }
}

const idIterator = idGenerator(1)

function getEntity (type:string) {
  let id = idIterator.next().value
  return {
    'id': id,
    'type': 'platform',
    'attributes': {
      'short_name': `${type}_${id}`
    }
  }
}

export const mockCurrentConfiguration = [
  {
    'action': {
      'id': idIterator.next().value,
      'type': 'platform_mount_action',
      'attributes': {
        'offset_y': 0.0,
        'description': '',
        'offset_x': 0.0,
        'updated_at': null,
        'offset_z': 0.0,
        'begin_date': '2022-04-11T12:08:13.000000'
      }
    },
    'entity': getEntity('platform'),
    'children': [
      {
        'action': {
          'id': idIterator.next().value,
          'type': 'device_mount_action',
          'attributes': {
            'offset_y': 0.0,
            'description': '',
            'offset_x': 0.0,
            'updated_at': null,
            'offset_z': 0.0,
            'begin_date': '2022-04-11T12:08:13.000000'
          }
        },
        'entity': getEntity('device'),
        'children': []
      },
      {
        'action': {
          'id': idIterator.next().value,
          'type': 'platform_mount_action',
          'attributes': {
            'offset_y': 0.0,
            'description': '',
            'offset_x': 0.0,
            'updated_at': null,
            'offset_z': 0.0,
            'begin_date': '2022-04-11T12:08:13.000000'
          }
        },
        'entity': getEntity('platform'),
        'children': [
          {
            'action': {
              'id': idIterator.next().value,
              'type': 'device_mount_action',
              'attributes': {
                'offset_y': 0.0,
                'description': '',
                'offset_x': 0.0,
                'updated_at': null,
                'offset_z': 0.0,
                'begin_date': '2022-04-11T12:08:13.000000'
              }
            },
            'entity': getEntity('device'),
            'children': []
          }
        ]
      }
    ]
  },
  {
    'action': {
      'id': idIterator.next().value,
      'type': 'platform_unmount_action',
      'attributes': {
        'description': '',
        'end_date': '2022-04-11T12:08:13.000000'
      }
    },
    'entity': getEntity('platform'),
    'children': []
  }
]

export const mockMountingActions = [
  {
    'timepoint': DateTime.fromISO('2022-04-14T05:40:00.000Z'),
    'label': '2022-04-14 05:40 - Mount | Platform X'
  },
  {
    'timepoint': DateTime.fromISO('2022-05-06T06:00:00.000Z'),
    'label': '2022-05-06 06:00 - Mount | Platform Y'
  },
]
