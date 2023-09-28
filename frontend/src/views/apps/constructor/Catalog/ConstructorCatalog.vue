<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { useConstructorStore } from '@/stores/apps/Constructor.ts'
import CatalogCategories from '@/views/apps/constructor/Catalog/CatalogCategories.vue'
import { notify, swalAlert } from '@/helpers/notify.ts'
import { v4 as uuidv4 } from 'uuid'
import draggable from 'vuedraggable'
import {
  CatalogCategory,
  CatalogTemplate,
  Section,
  SectionsType
} from '@/types/constructor.types.ts'
import SectionArticle from '@/components/constructor/sections/SectionArticle.vue'

const constructorStore = useConstructorStore()
const isLoading = ref(false)

const props = defineProps<{
  clone: (
    section: Omit<
      Section<
        SectionsType.Article | SectionsType.Title | SectionsType.Subtotal
      >,
      'id'
    >
  ) => {}
}>()
const emit = defineEmits(['update-dragging'])

onBeforeMount(async () => {
  await constructorStore.getCatalog()
})

const catalogModal = ref(null)
const catalogSearchString = ref('')
const constructorSearchString = ref('')

const searchTemplatesForCatalog = computed(() => {
  const templates = [
    ...constructorStore.catalog.templates_without_category
  ]
  constructorStore.catalog.categories.forEach((category) => {
    templates.push(...category.templates)
  })

  return templates.filter((template) => {
    return template.name
      .toLowerCase()
      .includes(catalogSearchString.value.toLowerCase())
  })
})

const searchTemplatesForConstructor = computed(() => {
  const templates = [
    ...constructorStore.catalog.templates_without_category
  ]

  constructorStore.catalog.categories.forEach((category) => {
    templates.push(...category.templates)
  })

  return templates.filter((template) => {
    return template.name
      .toLowerCase()
      .includes(constructorSearchString.value.toLowerCase())
  })
})

const openCatalogModal = () => {
  catalogModal.value.show()
  catalogSearchString.value = ''
}

const categoryModal = ref(null)
const categoryLocal = ref<{
  id: number | null
  name: string
}>({
  id: null,
  name: ''
})
const isCategoryCreateUpdateLoading = ref(false)

const addCategoryOpenModal = () => {
  categoryModal.value.show()
  categoryLocal.value = {
    id: null,
    name: ''
  }
}
const openModalUpdateCategory = (category: CatalogCategory) => {
  categoryLocal.value = category
  categoryLocal.value = { ...categoryLocal.value }
  categoryModal.value.show()
}

const templateModal = ref(null)
const templateLocal = ref<CatalogTemplate>({
  id: null,
  name: '',
  values: {
    title: '',
    description: '',
    unitPriceHT: 0,
    vatRate: 20,
    quantity: 1,
    articleType: 'service',
    discount: 0,
    discountType: null,
    discountDescription: '',
    unit: '',
    displayPriceInfos: true
  },
  category_id: null
})
const isTemplateCreateUpdateLoading = ref(false)

const addTemplateOpenModal = (category: CatalogCategory | null = null) => {
  templateModal.value.show()
  templateLocal.value = {
    id: null,
    name: '',
    values: {
      title: '',
      description: '',
      unitPriceHT: 0,
      vatRate: 20,
      quantity: 1,
      articleType: 'service',
      discount: 0,
      discountType: null,
      discountDescription: '',
      unit: '',
      displayPriceInfos: true
    },
    category_id: category?.id ?? null
  }
}

const updateTemplateOpenModal = (template: CatalogTemplate) => {
  templateLocal.value = template
  templateModal.value.show()
}

const handleCategoryCreateUpdate = async () => {
  isCategoryCreateUpdateLoading.value = true
  try {
    if (categoryLocal.value.id > 0) {
      await constructorStore.updateCatalogCategory(categoryLocal.value)
      categoryModal.value.hide()
    } else {
      await constructorStore.createCatalogCategory(categoryLocal.value)
      categoryModal.value.hide()
    }
  } catch (e) {
    notify('Une erreur est survenue', 'danger')
  }
  isCategoryCreateUpdateLoading.value = false
}

const deleteCategory = async (category: CatalogCategory) => {
  const { value } = await swalAlert(
    'Êtes-vous sûr de vouloir supprimer cette catégorie ?',
    'warning',
    'Tous les articles de la catégorie seront supprimés'
  )
  if (!value) return

  isLoading.value = true

  try {
    await constructorStore.deleteCatalogCategory(category)
  } catch {
    notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}

const handleTemplateCreateUpdate = async () => {
  isTemplateCreateUpdateLoading.value = true
  try {
    if (templateLocal.value.id > 0) {
      await constructorStore.updateCatalogTemplate(templateLocal.value)
      templateModal.value.hide()
    } else {
      await constructorStore.createCatalogTemplate(templateLocal.value)
      templateModal.value.hide()
    }
  } catch {
    notify('Une erreur est survenue', 'danger')
  }
  isTemplateCreateUpdateLoading.value = false
}

const deleteTemplate = async (template: CatalogTemplate) => {
  const { value } = await swalAlert(
    'Êtes-vous sûr de vouloir supprimer cet article ?'
  )
  if (!value) return

  isTemplateCreateUpdateLoading.value = true

  try {
    await constructorStore.deleteCatalogTemplate(template)
    templateModal.value.hide()
  } catch (e) {
    notify('Une erreur est survenue', 'danger')
  }

  isTemplateCreateUpdateLoading.value = false
}
</script>

<template>
  <div
    class="d-flex justify-content-between cursor-pointer"
    v-b-toggle:catalog-collapse
  >
    <h5 class="mb-50">Catalogue</h5>
    <vue-feather :type="'chevron-up'" class="when-opened" size="18" />
    <vue-feather :type="'chevron-down'" class="when-closed" size="18" />
  </div>

  <b-collapse id="catalog-collapse">
    <b-form-input
      placeholder="Rechercher un article"
      v-model="constructorSearchString"
    />
    <vue-perfect-scrollbar
      :settings="{
        maxScrollbarLength: 60,
        wheelPropagation: false
      }"
      class="articles-list"
      tagname="div"
    >
      <template v-if="constructorSearchString.length > 0">
        <div v-if="searchTemplatesForConstructor.length === 0">
          Aucun article trouvé
        </div>
        <div v-else class="mt-1">
          <div
            v-for="template in searchTemplatesForConstructor"
            class="draggable article mx-25"
          >
            <vue-feather type="move" size="16" class="cursor-pointer" />
            <span> {{ template.name }}</span>
          </div>
          <hr />
        </div>
      </template>

      <template v-else>
        <div v-for="category in constructorStore.catalog.categories">
          <div
            class="d-flex justify-content-between cursor-pointer mx-1 mt-1"
            :key="`cat-` + category.id"
            v-b-toggle="`categorie-` + category.id"
          >
            <h5 class="mb-50">{{ category.name }}</h5>
            <vue-feather
              :type="'chevron-up'"
              class="when-opened"
              size="18"
            />
            <vue-feather
              :type="'chevron-down'"
              class="when-closed"
              size="18"
            />
          </div>
          <b-collapse :id="`categorie-` + category.id" class="mt-50">
            <draggable
              :list="
                category.templates.map((template) => {
                  return {
                    title: template.name,
                    type: SectionsType.Article,
                    values: template.values,
                    component: SectionArticle
                  }
                })
              "
              item-key="type"
              div="div"
              :group="{
                name: 'sections',
                pull: 'clone',
                put: false,
                sort: false
              }"
              @start="emit('update-dragging', true)"
              @end="emit('update-dragging', false)"
              :clone="props.clone"
            >
              <template #item="{ element }">
                <div class="draggable article mx-75">
                  <vue-feather
                    type="move"
                    size="16"
                    class="cursor-pointer"
                  />
                  <span>{{ element.title }}</span>
                </div>
              </template>
            </draggable>
          </b-collapse>
          <hr />
        </div>
        <draggable
          :list="
            constructorStore.catalog.templates_without_category.map(
              (template) => {
                return {
                  title: template.name,
                  type: SectionsType.Article,
                  values: template.values,
                  component: SectionArticle
                }
              }
            )
          "
          item-key="type"
          div="div"
          :group="{
            name: 'sections',
            pull: 'clone',
            put: false,
            sort: false
          }"
          @start="emit('update-dragging', true)"
          @end="emit('update-dragging', false)"
          :clone="props.clone"
        >
          <template #item="{ element }">
            <div class="draggable article mx-75">
              <vue-feather type="move" size="16" class="cursor-pointer" />
              <span>{{ element.title }}</span>
            </div>
          </template>
        </draggable>
      </template>
    </vue-perfect-scrollbar>

    <b-button
      v-ripple
      variant="flat-info"
      block
      class="mt-1"
      @click="openCatalogModal"
    >
      Gérer le catalogue
    </b-button>
  </b-collapse>

  <b-modal ref="catalogModal" title="Catalogue" size="lg">
    <b-overlay :show="isLoading">
      <div class="mb-1">
        <b-row>
          <b-col md="5">
            <b-form-group label="Rechercher un article">
              <b-form-input
                v-model="catalogSearchString"
                placeholder="Rechercher un article par nom"
              />
            </b-form-group>
          </b-col>
          <b-col>
            <div
              class="d-flex justify-content-center justify-content-md-end"
              style="gap: 1rem"
            >
              <b-button
                variant="outline-primary"
                class="btn-with-icon"
                v-ripple
                @click="addCategoryOpenModal"
              >
                <vue-feather type="plus-square" size="16" />
                <span class="ml-50"> Ajouter une catégorie </span>
              </b-button>
              <b-button
                variant="primary"
                class="btn-with-icon"
                v-ripple
                @click="addTemplateOpenModal"
              >
                <vue-feather type="plus-circle" size="16" />
                <span class="ml-50"> Ajouter un article </span>
              </b-button>
            </div>
          </b-col>
        </b-row>
      </div>

      <div v-if="constructorSearchString">
        <div v-if="searchTemplatesForCatalog.length === 0">
          Aucun article
        </div>
        <div v-else>
          <b-row>
            <b-col
              v-for="template in searchTemplatesForCatalog"
              :key="`template` + template.id"
              md="4"
            >
              <div
                class="template-item cursor-pointer"
                @click="updateTemplateOpenModal(template)"
              >
                <h5>
                  {{ template.name }}
                </h5>
                <vue-feather type="arrow-right" />
              </div>
            </b-col>
          </b-row>
          <hr />
        </div>
      </div>

      <template v-else>
        <div
          v-for="category in constructorStore.catalog.categories"
          :key="`cat` + category.id"
        >
          <div class="d-flex justify-content-between mt-2">
            <div>
              <h4>
                {{ category.name }}
              </h4>
            </div>
            <div class="d-flex" style="gap: 1rem">
              <div @click="addTemplateOpenModal(category)">
                <vue-feather
                  type="plus-circle"
                  class="text-primary cursor-pointer"
                />
              </div>
              <div @click="openModalUpdateCategory(category)">
                <vue-feather type="edit" class="cursor-pointer" />
              </div>
              <div @click="deleteCategory(category)">
                <vue-feather
                  type="trash"
                  class="cursor-pointer text-danger"
                />
              </div>
            </div>
          </div>

          <div v-if="category.templates.length === 0">Aucun article</div>
          <div v-else>
            <b-row>
              <b-col
                v-for="template in category.templates"
                :key="`template` + template.id"
                md="4"
              >
                <div
                  class="template-item cursor-pointer"
                  @click="updateTemplateOpenModal(template)"
                >
                  <h5>
                    {{ template.name }}
                  </h5>
                  <vue-feather type="arrow-right" />
                </div>
              </b-col>
            </b-row>
            <hr />
          </div>
        </div>

        <h4 class="mt-2">Articles sans catégorie</h4>
        <div
          v-if="
            constructorStore.catalog.templates_without_category.length ===
            0
          "
        >
          Aucun article
        </div>
        <b-row v-else>
          <b-col
            v-for="template in constructorStore.catalog
              .templates_without_category"
            :key="`template` + template.id"
            md="4"
          >
            <div
              class="template-item cursor-pointer"
              @click="updateTemplateOpenModal(template)"
            >
              <h5>
                {{ template.name }}
              </h5>
              <vue-feather type="arrow-right" />
            </div>
          </b-col>
        </b-row>
        <hr />
      </template>
    </b-overlay>
    <template #modal-footer="{ cancel }">
      <b-button variant="outline-secondary" v-ripple @click="cancel">
        Fermer
      </b-button>
    </template>
  </b-modal>

  <b-modal
    :title="
      categoryLocal.id > 0
        ? 'Modifier la catégorie'
        : 'Ajouter une catégorie'
    "
    ref="categoryModal"
  >
    <b-overlay :show="isCategoryCreateUpdateLoading">
      <b-form-group label="Nom de la catégorie">
        <b-form-input
          v-model="categoryLocal.name"
          placeholder="Nom de la catégorie"
        />
      </b-form-group>
    </b-overlay>
    <template #modal-footer="{ cancel }">
      <b-button variant="outline-secondary" v-ripple @click="cancel">
        Annuler
      </b-button>
      <b-button
        variant="primary"
        v-ripple
        :disabled="
          categoryLocal.name.length === 0 || isCategoryCreateUpdateLoading
        "
        @click="handleCategoryCreateUpdate"
      >
        Enregistrer
      </b-button>
    </template>
  </b-modal>

  <b-modal
    :title="
      templateLocal.id > 0 ? 'Modifier l\'article' : 'Ajouter un article'
    "
    ref="templateModal"
    size="lg"
  >
    <b-overlay :show="isTemplateCreateUpdateLoading">
      <b-row>
        <b-col md="6">
          <b-form-group label="Nom de l'article">
            <b-form-input
              v-model="templateLocal.name"
              placeholder="Nom de l'article"
            />
          </b-form-group>
        </b-col>
        <b-col md="6">
          <b-form-group label="Catégorie de l'article">
            <v-select
              v-model="templateLocal.category_id"
              :options="[
                {
                  label: 'Aucune catégorie',
                  value: null
                },
                ...constructorStore.catalog.categories.map((category) => {
                  return {
                    label: category.name,
                    value: category.id
                  }
                })
              ]"
              :reduce="(option) => option.value"
              :clearable="false"
            />
          </b-form-group>
        </b-col>
      </b-row>

      <b-card>
        <SectionArticle :is-template="true" :section="templateLocal" />
      </b-card>
    </b-overlay>
    <template #modal-footer="{ cancel }">
      <b-button variant="outline-secondary" v-ripple @click="cancel">
        Annuler
      </b-button>
      <b-button
        class="btn-with-icon"
        variant="outline-danger"
        @click="deleteTemplate(templateLocal)"
      >
        Supprimer
      </b-button>
      <b-button
        variant="primary"
        v-ripple
        :disabled="
          templateLocal.name.length === 0 || isTemplateCreateUpdateLoading
        "
        @click="handleTemplateCreateUpdate"
      >
        Enregistrer
      </b-button>
    </template>
  </b-modal>
</template>

<style>
.template-item {
  cursor: pointer;
  padding: 1em;
  border: 1px solid #ebe9f1;
  border-radius: 6px;
  box-shadow: 0 0.125rem 0.25rem rgba(34, 41, 47, 0.15);
  display: flex;
  justify-content: space-between;
}
</style>
