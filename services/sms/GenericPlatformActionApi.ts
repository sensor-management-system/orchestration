import {AxiosInstance} from "axios";
import {GenericDeviceActionSerializer, IGenericActionSerializer} from "@/serializers/jsonapi/GenericActionSerializer";

export class GenericPlatformActionApi {
  private axiosApi: AxiosInstance
  private serializer: IGenericActionSerializer

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
    this.serializer = new GenericDeviceActionSerializer()
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(id)
  }
}
