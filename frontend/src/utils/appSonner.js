import { toast } from 'vuetify-sonner'

export default {
  success(message, duration = 2000) {
    toast(message, {
      cardProps: {
        color: 'success',
      },
      prependIcon: 'mdi-check-circle',
      duration: duration,
    })
  },
  error(message, duration = 2000) {
    toast(message, {
      cardProps: {
        color: 'error',
      },
      prependIcon: 'mdi-cancel',
      duration,
    })
  },
  info(message, duration = 2000) {
    toast(message, {
      cardProps: {
        color: 'info',
      },
      prependIcon: 'mdi-alert-circle',
      duration,
    })
  },
  warning(message, duration = 2000) {
    toast(message, {
      cardProps: {
        color: 'warning',
      },
      prependIcon: 'mdi-alert',
      duration,
    })
  },
}
