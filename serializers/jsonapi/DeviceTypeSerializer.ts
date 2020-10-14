import DeviceType from '@/models/DeviceType'

import { IJsonApiObjectListWithLinks, IJsonApiDataWithIdAndLinks } from '@/serializers/jsonapi/JsonApiTypes'

import { removeBaseUrl } from '@/utils/urlHelpers'

export class DeviceTypeSerializer {
    private cvBaseUrl: string | undefined

    constructor (cvBaseUrl: string | undefined) {
      this.cvBaseUrl = cvBaseUrl
    }

    convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiObjectListWithLinks): DeviceType[] {
      return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
    }

    convertJsonApiDataToModel (jsonApiData: IJsonApiDataWithIdAndLinks): DeviceType {
      const id = jsonApiData.id
      const name = jsonApiData.attributes.name
      const url = removeBaseUrl(jsonApiData.links.self, this.cvBaseUrl)

      return DeviceType.createWithData(id, name, url)
    }
}
