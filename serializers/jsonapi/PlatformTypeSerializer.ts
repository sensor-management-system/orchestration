import PlatformType from '@/models/PlatformType'

import { removeBaseUrl } from '@/utils/urlHelpers'

export default class PlatformTypeSerializer {
    private cvBaseUrl: string | undefined

    constructor (cvBaseUrl: string | undefined) {
      this.cvBaseUrl = cvBaseUrl
    }

    convertJsonApiObjectListToModelList (jsonApiObjectList: any): PlatformType[] {
      return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
    }

    convertJsonApiDataToModel (jsonApiData: any): PlatformType {
      const id = jsonApiData.id
      const name = jsonApiData.attributes.name
      const url = removeBaseUrl(jsonApiData.links.self, this.cvBaseUrl)

      return PlatformType.createWithData(id, name, url)
    }
}
