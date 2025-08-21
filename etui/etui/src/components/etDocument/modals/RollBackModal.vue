<script setup>
import {computed, onMounted, ref} from 'vue'

import { httpPostJson} from "@/core/http.js";
import eventBus from "@/core/eventBus.js";
import { etDocumentUrl } from '@/core/const/urls.js'
import { etDocumentEvent } from '@/core/const/events.js'

const taskInfo = ref({})
const comment = ref("")
onMounted(()=>{
  eventBus.$on(etDocumentEvent.rollBackTask, (task) => {
    taskInfo.value = task
    console.log(taskInfo.value.id)
  })
})



const rollBack = ()=>{
  httpPostJson(etDocumentUrl.taskRollBack,{
      task_id: taskInfo.value.id,
      comment: comment.value
  },(resp)=>{
    $("#rollBackModal").modal("hide")
    eventBus.$emit(etDocumentEvent.refreshDocumentList)
  },()=>{})
}

const words = computed(()=>{
  return `${comment.value.length}/100`
})


</script>

<template>
  <div class="modal modal-blur fade" id="rollBackModal" tabindex="-1" role="dialog" aria-hidden="true">
    <div class="modal-dialog modal-sm modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-body">
          <div class="modal-status bg-danger"></div>
          <label class="form-label required">退回说明 <span class="form-label-description">{{words}}</span></label>
          <textarea class="form-control" name="example-textarea-input" maxlength="100" v-model="comment" rows="3" placeholder="请说明退回原因"></textarea>
        </div>
        <div class="modal-footer">
          <button class="btn btn-danger btn-sm" @click="rollBack()">退回</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
