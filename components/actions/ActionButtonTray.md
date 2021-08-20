The action button tray can be used to display an *apply* and a *cancel* button
for all action forms.

## Usage

### Standard Usage

```vue
<template>
  <ActionButtonTray
    cancel-url="/"
  />
</template>
```

### Disabled Apply Button

The *apply* button can be disabled by providing `true` to the property
`isSaving`. This is usually used during a asynchronous API action:

```vue
<template>
  <ActionButtonTray
    cancel-url="/"
    :is-saving="true"
  />
</template>
```

### Hidden Apply Button

The *apply* button can be also hidden by providing `false` to the `show-apply`
property:

```vue
<template>
  <ActionButtonTray
    cancel-url="/"
    :show-apply="false"
  />
</template>
```

