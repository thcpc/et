<script setup>
import Document from '@/components/Document.vue'
import Navigation from "@/components/Navigation.vue";

</script>

<template>
  <navigation />
  <document :doc-id="$route.params.id" />
</template>
