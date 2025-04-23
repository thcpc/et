<script setup>
import {computed, onMounted, ref} from 'vue'
import { UnKnown } from '@/core/enums.js'
import {httpGet, httpPostJson} from "@/core/http.js";
import eventBus from "@/core/eventBus.js";

const selectUser = ref(UnKnown.ID)
const assigneeInfo = ref({})
const comment = ref("")

onMounted(()=>{
  eventBus.$on('reAssigneeTask', (assignee) => {
    assigneeInfo.value = assignee
  })
  const modal = document.getElementById('reAssigneeModal');
  modal.addEventListener('hide.bs.modal', ()=>{
    selectDestroy()
  });
  modal.addEventListener('shown.bs.modal', ()=>{
    tomSelectSingleton()
  })
})


const selectDestroy = ()=>{
  var ti = document.getElementById("reAssigneeSelect").tomselect
  if (ti) {
    ti.destroy()
  }
}

const reAssignee = ()=>{
  httpPostJson("/task/api/reAssignee",{
      task_id: assigneeInfo.value.task_id,
      new_assignee_id: selectUser.value,
      old_assignee_id: assigneeInfo.value.user_id,
      comment: comment.value
  },(resp)=>{
    $("#reAssigneeModal").modal("hide")
    eventBus.$emit('refresh-document-list')
  },()=>{})
}
const tomSelectSingleton = () => {
  selectDestroy()
  newTomSelect()
}

const newTomSelect = () => {

  new TomSelect('#reAssigneeSelect', {
    valueField: 'id',
    searchField: ['name'],
    labelField: 'name',
    placeholder: "输入你要转给的人",
    load: function(query, callback) {
      var self = this;
      if( self.loading > 1 ){
        callback();
        return;
      }
      httpGet("/user/api/users",{},(response)=>{
        callback(response);
        self.settings.load = null;

      })
    },
    render: {
      option: function (data, escape) {
        return `<div class="py-2 d-flex">
							<div class="mb-1">
							<span class="dropdown-item-indicator">
								<span class="h5">
									${ escape(data.name) }
								</span>
							</span>
							</div>
						</div>`;
      },
      item: function (data, escape) {
        return '<div>' + data.name + '</div>';
      }
    }
  });
}


const words = computed(()=>{
  return `${comment.value.length}/100`
})




</script>

<template>
  <div class="modal modal-blur fade" id="reAssigneeModal" tabindex="-1" role="dialog" aria-hidden="true">
    <div class="modal-dialog modal-sm modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-body">
          <label class="form-label required">任务接受人</label>
          <div class="input-group mb-2">
            <select
              class="form-select"
              id="reAssigneeSelect"
              v-model="selectUser"
              autocomplete="off"
            ></select>


          </div>
          <label class="form-label">备注 <span class="form-label-description">{{words}}</span></label>
          <textarea class="form-control" name="example-textarea-input" maxlength="100" rows="3" v-model="comment" placeholder="如有备注,请简要说明"></textarea>
        </div>
        <div class="modal-footer">
          <button class="btn btn-primary btn-sm" @click="reAssignee()">确认</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
