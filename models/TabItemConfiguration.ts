export interface ITabItemRoute {
  name: string
  to: string
}

export interface ITabItemLink {
  name: string
  href: string
}

export type TabItemConfiguration = string | ITabItemRoute | ITabItemLink
