<script setup>
import {onMounted} from "vue";

const props = defineProps(["paragraph"])
const initSummernote = ()=>{
  // $(`#editorId`).summernote({
  //   placeholder: '请输入内容',
  //   height: 300,
  //   callbacks: {
  //     onChange: function (contents) {
  //       // self.$emit('input', contents); // 将内容传递给父组件
  //       console.log(contents)
  //     },
  //     onImageUpload: function (files){
  //       const formData = new FormData();
  //       formData.append('file', files[0]);
  //     }
  //   },
  // });
  $(`#editorId`).summernote({
    airMode: true,
    callbacks: {
      onChange: function (contents) {
        // self.$emit('input', contents); // 将内容传递给父组件
        console.log(contents)
      },
    },
  });
}

const destroySummernote = () =>{
  $(`#editorId`).summernote('destroy');
}

onMounted(()=>{
  const modal = document.getElementById('SummernoteModal');
  modal.addEventListener('show.bs.modal', initSummernote);
  modal.addEventListener('hidden.bs.modal',destroySummernote)
})

</script>

<template>
  <div class="modal modal-blur fade" id="SummernoteModal" tabindex="-1" role="dialog" aria-hidden="true">
    <div class="modal-dialog modal-xl modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">修改</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div id="editorId"></div>
        </div>

        <div class="modal-footer">
          <a href="#" class="btn btn-link link-secondary" data-bs-dismiss="modal">
            取消
          </a>
          <a href="#" class="btn btn-primary ms-auto" data-bs-dismiss="modal">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24"
                 stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
              <path d="M12 5l0 14"/>
              <path d="M5 12l14 0"/>
            </svg>
            更新
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
