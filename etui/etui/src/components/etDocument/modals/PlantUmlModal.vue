<script setup>
import {onMounted, ref} from "vue";
import {encode} from "plantuml-encoder";
import eventBus from "@/core/eventBus.js";
import { etDocumentEvent } from '@/core/const/events.js'

const plantUMLImage = ref('');

onMounted(()=>{
  eventBus.$on(etDocumentEvent.previewPlantuml, (imageContent) => {
    const encoded = encode(imageContent);
    plantUMLImage.value = `http://www.plantuml.com/plantuml/svg/${encoded}`;
  });

  const modal = document.getElementById('plantUmlModal');
  modal.addEventListener('hide.bs.modal', ()=>{plantUMLImage.value=""});


})

</script>

<template>
  <div class="modal" id="plantUmlModal" tabindex="-1" aria-hidden="true" role="dialog">
    <div class="modal-dialog modal-lg" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">配置</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <img :src="plantUMLImage" alt="PlantUML Diagram">
        </div>
        <div class="modal-footer">
          <a href="#" class="btn" data-bs-dismiss="modal">Close</a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
