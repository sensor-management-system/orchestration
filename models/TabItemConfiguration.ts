export interface ITabItem {
  name: string
  disabled?: boolean
}

export interface ITabItemRoute extends ITabItem {
  to: string
}

export interface ITabItemLink extends ITabItem {
  href: string
}

export type TabItemConfiguration = string | ITabItem | ITabItemRoute | ITabItemLink
