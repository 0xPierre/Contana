import { useToast } from 'vue-toastification'
import ToastificationContent from '@/components/toastification/ToastificationContent.vue'
import Swal from 'sweetalert2'
import type { SweetAlertIcon } from 'sweetalert2'

const toast = useToast()
const notify = (
  title: string | undefined,
  type = 'success',
  message = ''
) => {
  toast({
    component: ToastificationContent,
    props: {
      title: title ? title : 'Notification',
      icon: type === 'success' ? 'check-circle' : 'alert-triangle',
      variant: type,
      text: message
    }
  })
}

const notifyApiError = (
  errors: { [key: string]: string[] } | undefined
) => {
  if (!errors) return
  const err = Object.values(errors)

  if (err.length > 0) {
    notify(err[0][0], 'danger')
  }
}

const swalAlert = async (
  title: string,
  type: SweetAlertIcon = 'warning',
  text: string = '',
  confirmButtonText: string = 'Oui'
) => {
  return Swal.fire({
    title,
    text,
    icon: type,
    showCancelButton: type === 'warning',
    confirmButtonText:
      type === 'question' || type === 'warning' ? confirmButtonText : 'Ok',
    cancelButtonText: 'Non',
    customClass: {
      confirmButton: 'btn btn-primary',
      cancelButton: 'btn btn-outline-danger ml-1'
    },
    buttonsStyling: false
  })
}
export { notify, notifyApiError, swalAlert }
