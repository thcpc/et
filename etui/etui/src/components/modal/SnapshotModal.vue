<script setup>
import { onMounted, ref } from 'vue'
import { UnKnown } from '@/core/enums.js'
import { httpPostJson } from '@/core/http.js'

const parentData = defineProps(['docId'])
const name = ref(UnKnown.EMPTY)
const description = ref(UnKnown.EMPTY)

const submit = () => {
  httpPostJson(
    '/document/api/new/snapshot',
    { name: name.value, description: description.value, docId: parentData.docId },
    (resp) => {
      $('#snapshotModal').modal('hide')
    },()=>{
      $('#snapshotModal').modal('hide')
    }
  )
}

onMounted(() => {
  const modal = document.getElementById('snapshotModal')

  modal.addEventListener('shown.bs.modal', () => {

    name.value = `${new Date().toLocaleString()} snapshot`
  })

  modal.addEventListener('hide.bs.modal', () => {
    name.value = UnKnown.EMPTY
    description.value = UnKnown.EMPTY
  })
})
</script>

<template>
  <div class="modal" id="snapshotModal" tabindex="-1" aria-hidden="true" role="dialog">
    <div class="modal-dialog modal-lg" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">创建快照</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label class="form-label required">快照名</label>
            <input
              type="text"
              class="form-control"
              name="example-required-input"
              placeholder="Required..."
              v-model="name"
            />
          </div>
          <div class="mb-3">
            <label class="form-label"
              >快照描述 <span class="form-label-description">56/100</span></label
            >
            <textarea
              class="form-control"
              name="example-textarea-input"
              rows="6"
              placeholder="Content.."
              v-model="description"
            >
Oh! Come and see the violence inherent in the system! Help, help, I'm being repressed! We shall say 'Ni' again to you, if you do not appease us. I'm not a witch. I'm not a witch. Camelot!</textarea
            >
          </div>
        </div>
        <div class="modal-footer">
          <a href="#" class="btn" @click="submit">创建</a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
