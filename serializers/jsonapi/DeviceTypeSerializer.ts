import DeviceType from '@/models/DeviceType'

import { removeBaseUrl } from '@/utils/urlHelpers'

export default class DeviceTypeSerializer {
    private cvBaseUrl: string | undefined

    constructor (cvBaseUrl: string | undefined) {
      this.cvBaseUrl = cvBaseUrl
    }

    convertJsonApiObjectListToModelList (jsonApiObjectList: any): DeviceType[] {
      return jsonApiObjectList.data.map((x: any) => this.convertJsonApiDataToModel(x))
    }

    convertJsonApiDataToModel (jsonApiData: any): DeviceType {
      const id = jsonApiData.id
      const name = jsonApiData.attributes.name
      const url = removeBaseUrl(jsonApiData.links.self, this.cvBaseUrl)

      return DeviceType.createWithData(id, name, url)
    }
}
