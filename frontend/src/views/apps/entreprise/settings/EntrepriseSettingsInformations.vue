<script lang="ts" setup>
import { useFormValidation } from '@/composables/formValidation'
import { notify, notifyApiError } from '@/helpers/notify'
import entreprise from '@/router/routes/entreprise'
import { useEntrepriseStore } from '@/stores/apps/Entreprise'
import { required, email } from '@vuelidate/validators'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const isLoading = ref(false)
const entrepriseStore = useEntrepriseStore()
const router = useRouter()

const { formState, v$ } = useFormValidation(
  {
    name: entrepriseStore.entreprise?.name || '',
    email: entrepriseStore.entreprise?.email || '',
    phone: entrepriseStore.entreprise?.phone || '',
    address: entrepriseStore.entreprise?.address || '',
    city: entrepriseStore.entreprise?.city || '',
    zip_code: entrepriseStore.entreprise?.zip_code || '',
    country: entrepriseStore.entreprise?.country || '',
    siren: entrepriseStore.entreprise?.siren || '',
    num_rcs: entrepriseStore.entreprise?.num_rcs || '',
    vat_number: entrepriseStore.entreprise?.vat_number || '',
    iban: entrepriseStore.entreprise?.iban || '',
    bic: entrepriseStore.entreprise?.bic || '',
    bank: entrepriseStore.entreprise?.bank || '',
    ape: entrepriseStore.entreprise?.ape || '',
    forme: entrepriseStore.entreprise?.forme || '',
    capital: entrepriseStore.entreprise?.capital || ''
  },
  {
    name: { required },
    email: { required, email }
  }
)

const updateInformations = async () => {
  // const validated = await v$.value.$validate()
  // if (!validated) return

  isLoading.value = true
  try {
    const { data } =
      await entrepriseStore.updateEntrepriseInformations(formState)

    if (data.status === 'success') {
      console.log(entrepriseStore.entreprise?.slug, data.data.slug)
      if (entrepriseStore.entreprise?.slug !== data.data.slug) {
        console.log('update slug')
        router.replace({
          name: 'entreprise-settings',
          params: { entrepriseSlug: data.data.slug }
        })
      }
      entrepriseStore.entreprise = data.data
      entrepriseStore.selectedEntrepriseSlug = data.data.slug
      notify('Votre entreprise a été mise à jour', 'success')
    } else {
      notifyApiError(data.errors)
    }
  } catch {
    notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}
</script>

<template>
  <b-overlay :show="isLoading">
    <b-card title="Informations générales">
      <b-form @submit.prevent="updateInformations">
        <b-row>
          <b-col md="6">
            <b-form-group label="Dénomination de votre entreprise">
              <b-form-input
                placeholder="Entreprise Dupond"
                v-model="formState.name"
              />
              <small
                v-show="v$.name.$errors.length > 0"
                class="text-danger"
              >
                Dénomination de votre entreprise requise
              </small>
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Adresse email">
              <b-form-input
                placeholder="john.doe@gmail.com"
                v-model="formState.email"
              />
              <small
                v-show="v$.email.$errors.length > 0"
                class="text-danger"
              >
                Adresse email invalide
              </small>
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Numéro de téléphone">
              <b-form-input
                placeholder="0712345678"
                v-model="formState.phone"
              />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Pays">
              <b-form-input
                placeholder="France"
                v-model="formState.country"
              />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Ville">
              <b-form-input placeholder="Paris" v-model="formState.city" />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Code postal">
              <b-form-input
                placeholder="71000"
                v-model="formState.zip_code"
              />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Adresse">
              <b-form-input
                placeholder="11 rue des champs élysées"
                v-model="formState.address"
              />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Numéro RCS">
              <b-form-input
                placeholder="RCS PARIS B 517 403 572"
                v-model="formState.num_rcs"
              />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Numéro de TVA intracommunautaire">
              <b-form-input
                placeholder="FR 32 123456789"
                v-model="formState.vat_number"
              />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Iban">
              <b-form-input
                placeholder="FR76 3000 1005 5000 0123 4567 890"
                v-model="formState.iban"
              />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="BIC">
              <b-form-input placeholder="BIC" v-model="formState.bic" />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Banque">
              <b-form-input
                placeholder="Crédit mutuel"
                v-model="formState.bank"
              />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Code APE">
              <b-form-input placeholder="0112Z" v-model="formState.ape" />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Forme">
              <b-form-input placeholder="EI" v-model="formState.forme" />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Siren">
              <b-form-input
                placeholder="951234567"
                v-model="formState.siren"
              />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Capital social">
              <b-input-group>
                <b-form-input
                  placeholder="10 000"
                  v-model="formState.capital"
                />
                <b-input-group-append is-text>€</b-input-group-append>
              </b-input-group>
            </b-form-group>
          </b-col>
        </b-row>
        <b-button v-ripple variant="primary" type="submit">
          Enregistrer
        </b-button>
      </b-form>
    </b-card>
  </b-overlay>
</template>
