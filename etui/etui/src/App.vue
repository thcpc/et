<script setup>
import { RouterView } from 'vue-router'
// import SummernoteModal from "@/components/etDocument/SummernoteModal.vue";
// import PlantUmlModal from "@/components/etDocument/modals/PlantUmlModal.vue";
// import NewParagraphModal from "@/components/etDocument/modals/NewParagraphModal.vue";
// import NewDocumentModal from "@/components/etDocument/modals/NewDocumentModal.vue";
import LoadingSpinner from "@/components/common/LoadingSpinner.vue";
import JwtModal from "@/components/common/modals/JwtModal.vue";
// import ReAssigneeModal from "@/components/etDocument/modals/ReAssigneeModal.vue";
// import RollBackModal from "@/components/etDocument/modals/RollBackModal.vue";
// import AssignAutoTestTaskModal from "@/components/etDocument/modals/tasks/AssignAutoTestTaskModal.vue";
</script>

<template>
  <jwt-modal />
  <loading-spinner />
  <RouterView />
</template>

<style scoped>

</style>
