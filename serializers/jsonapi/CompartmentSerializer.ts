import Compartment from '@/models/Compartment'

import { removeBaseUrl } from '@/utils/urlHelpers'

export default class CompartmentSerializer {
  private cvBaseUrl: string | undefined

  constructor (cvBaseUrl: string | undefined) {
    this.cvBaseUrl = cvBaseUrl
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: any): Compartment[] {
    return jsonApiObjectList.data.map((x: any) => this.convertJsonApiDataToModel(x))
  }

  convertJsonApiDataToModel (jsonApiData: any): Compartment {
    const id = jsonApiData.id
    const name = jsonApiData.attributes.name
    const url = removeBaseUrl(jsonApiData.links.self, this.cvBaseUrl)

    return Compartment.createWithData(id, name, url)
  }
}
