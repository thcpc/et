<script setup>
import { RouterView } from 'vue-router'
import SummernoteModal from "@/components/SummernoteModal.vue";
import PlantUmlModal from "@/components/modal/PlantUmlModal.vue";
import NewParagraphModal from "@/components/modal/NewParagraphModal.vue";
import NewDocumentModal from "@/components/modal/NewDocumentModal.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import JwtModal from "@/components/modal/JwtModal.vue";
import ReAssigneeModal from "@/components/modal/ReAssigneeModal.vue";
import RollBackModal from "@/components/modal/RollBackModal.vue";
import AssignAutoTestTaskModal from "@/components/modal/tasks/AssignAutoTestTaskModal.vue";
</script>

<template>
  <assign-auto-test-task-modal />
  <roll-back-modal />
  <re-assignee-modal />
  <jwt-modal />
  <loading-spinner />
  <new-document-modal />
  <new-paragraph-modal />
  <plant-uml-modal />
  <summernote-modal />
  <RouterView />
</template>

<style scoped>

</style>
