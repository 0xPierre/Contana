<script lang="ts" setup></script>

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
    <b-form-input placeholder="Rechercher un article" />
    <vue-perfect-scrollbar
      :settings="{
        maxScrollbarLength: 60,
        wheelPropagation: false
      }"
      class="articles-list"
      tagname="div"
    >
      <div
        class="d-flex justify-content-between cursor-pointer mx-1 mt-1"
        v-b-toggle:categorie-1
      >
        <h5 class="mb-50">Design</h5>
        <vue-feather :type="'chevron-up'" class="when-opened" size="18" />
        <vue-feather
          :type="'chevron-down'"
          class="when-closed"
          size="18"
        />
      </div>
      <b-collapse id="categorie-1" class="mt-50">
        <div class="draggable article mx-75">
          <vue-feather type="move" size="16" class="cursor-pointer" />
          <span> Site internet </span>
        </div>
      </b-collapse>
      <hr />
      <div class="draggable article mx-25">
        <vue-feather type="move" size="16" class="cursor-pointer" />
        <span> Site internet </span>
      </div>
      <div class="draggable article">
        <vue-feather type="move" size="16" class="cursor-pointer" />
        <span> Site internet </span>
      </div>
      <div class="draggable article">
        <vue-feather type="move" size="16" class="cursor-pointer" />
        <span> Site internet </span>
      </div>
      <div class="draggable article">
        <vue-feather type="move" size="16" class="cursor-pointer" />
        <span> Site internet </span>
      </div>
    </vue-perfect-scrollbar>

    <b-button v-ripple variant="flat-info" block class="mt-1">
      Gérer le catalogue
    </b-button>
  </b-collapse>
</template>
