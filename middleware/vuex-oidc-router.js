/*
Web client of the Sensor Management System software developed within
the Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
*/

export default function (context) {
  // We call this function every time we change the routes of our pages.
  // We use it here to prevent unauthorized access to our routes.
  // Basically we ask our Open ID Connect store if the user is allowed
  // to access our route.
  // Otherwise we redirect to the a plain page (like the index page).
  return new Promise((resolve) => {
    const redirect = (textToDisplay) => {
      if (textToDisplay) {
        context.store.commit('snackbar/setError', textToDisplay)
      }
      const indexPage = '/'
      return context.redirect(indexPage)
    }

    const accessPromise = context.store.dispatch('oidc/oidcCheckAccess', context.route)

    accessPromise.then((hasAccess) => {
      if (hasAccess) {
        // ok, we don't need to change anything
        resolve(true)
      } else {
        resolve(redirect('Unauthorized'))
      }
    }).catch((error) => {
      resolve(redirect(error))
    })
  })
}
