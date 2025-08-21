<script setup>
import UserDocument from '@/components/etDocument/UserDocument.vue'
import AppNavigation from "@/components/common/AppNavigation.vue";
import NewParagraphModal from '@/components/etDocument/modals/NewParagraphModal.vue'
import SummernoteModal from '@/components/etDocument/SummernoteModal.vue'
import PlantUmlModal from '@/components/etDocument/modals/PlantUmlModal.vue'

</script>

<template>

  <plant-uml-modal />
  <summernote-modal />
  <new-paragraph-modal />
  <app-navigation />
  <user-document :doc-id="$route.params.id" />
</template>
