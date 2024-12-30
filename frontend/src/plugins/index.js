/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

import 'normalize.css'


// Plugins
import vuetify from './vuetify'
import pinia from '@/stores'
import router from '@/router'

export function registerPlugins(app) {
  app
    .use(vuetify)
    .use(router)
    .use(pinia)
}
