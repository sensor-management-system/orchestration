import {WebStorageStateStore} from "oidc-client";

export default {
  userStore: new WebStorageStateStore({store: window.localStorage}),
  authority: process.env.NUXT_ENV_AUTHORITY,
  client_id: process.env.NUXT_ENV_CLIENT_ID,
  redirect_uri: process.env.NUXT_ENV_REDIRECT_URI,
  response_type: process.env.NUXT_ENV_RESPONSE_TYPE ,
  scope: process.env.NUXT_ENV_SCOPE,
  post_logout_redirect_uri: process.env.NUXT_ENV_POST_LOGOUT_REDIRECT_URI,
  filterProtocolClaims: process.env.NUXT_ENV_FILTER_PROTOCOL_CLAIMS === 'true', //kleiner Trick, da man in der dpcker-compose.yaml kein boolean schreiben kann
  automaticSilentRenew:process.env.NUXT_ENV_AUTOMATIC_SILENT_RENEW === 'false', //kleiner Trick, da man in der dpcker-compose.yaml kein boolean schreiben kann
  silent_redirect_uri:process.env.NUXT_ENV_SILENT_REDIRECT_URI,
  popupWindowFeatures:'location=no,toolbar=no,width=500,height=600,left=100,top=100' //adjusted height
};

