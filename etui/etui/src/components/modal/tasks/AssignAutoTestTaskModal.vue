<script setup>
import {computed, onMounted, ref} from "vue";
import eventBus from "@/core/eventBus.js";
import {httpGet, httpPostJson} from "@/core/http.js";
import {UnKnown} from "@/core/enums.js";
const taskInfo = ref({})
const selectUser = ref(UnKnown.ID)

onMounted(()=>{
  eventBus.$on('AssigneeAutoTestTask', (task) => {
    taskInfo.value = task
    $('#assigneeAutoTestTaskModal').modal("show")
  })
  const modal = document.getElementById('assigneeAutoTestTaskModal');
  modal.addEventListener('hide.bs.modal', ()=>{
    selectDestroy()
  });
  modal.addEventListener('shown.bs.modal', ()=>{
    tomSelectSingleton()
  })
})


const selectDestroy = ()=>{
  var ti = document.getElementById("assigneeAutoTestTaskSelect").tomselect
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
    $("#assigneeAutoTestTaskModal").modal("hide")
    eventBus.$emit('refresh-document-list')
  },()=>{})
}
const tomSelectSingleton = () => {
  selectDestroy()
  newTomSelect()
}

const newTomSelect = () => {

  new TomSelect('#assigneeAutoTestTaskSelect', {
    valueField: 'id',
    searchField: ['name'],
    labelField: 'name',
    placeholder: "输入用户名",
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




</script>

<template>
  <div class="modal modal-blur fade" id="assigneeAutoTestTaskModal" tabindex="-1" role="dialog" aria-hidden="true">
    <div class="modal-dialog modal-sm modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-body">
          <label class="form-label required">关联用例的人</label>
          <div class="input-group mb-2">
            <select
              class="form-select"
              id="assigneeAutoTestTaskSelect"
              v-model="selectUser"
              autocomplete="off"
            ></select>

          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-primary btn-sm" @click="reAssignee()">完成</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
