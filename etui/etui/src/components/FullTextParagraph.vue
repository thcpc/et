<script setup>
import { Constant } from '@/core/enums.js'
import { httpDelete, httpPostJson } from '@/core/http.js'
import Editor from "@toast-ui/editor";
import Viewer from '@toast-ui/editor/dist/toastui-editor-viewer';
import {onMounted} from "vue";

const paragraphProps = defineProps(['paragraph'])

const emit = defineEmits(['deleteSelf'])

let markDownEditor = null
let markDownViewer = null
const edit = () => {
  destroyViewer()
  if(!markDownEditor){
    markDownEditor = new Editor({
      el: document.querySelector('#' + paragraphId()),
      initialValue: paragraphProps.paragraph.contents,
      initialEditType: 'markdown',
      previewStyle: 'vertical'
    });
    markDownEditor.setMarkdown(paragraphProps.paragraph.contents)
  }
}

const destroyViewer = ()=>{
  if(markDownViewer) {
    markDownViewer.destroy()
    markDownViewer = null
  }
}

const destroyEditor = ()=>{
  if(markDownEditor) {
    markDownEditor.destroy()
    markDownEditor = null
    $('#' + paragraphId()).removeAttr("style")


  }
}

const createView = ()=>{
  if(!markDownViewer){
    markDownViewer = new Viewer({
      el: document.querySelector('#' + paragraphId()),
      height: 'auto'
    });
    markDownViewer.setMarkdown(paragraphProps.paragraph.contents)

  }
}


onMounted(()=>{
  createView()
})

const save = () => {
  // let contents = $('#' + paragraphId()).summernote('code')
  let contents = markDownEditor.getMarkdown()

  httpPostJson(
    '/document/api/update/paragraph',
    {
      paragraphId: paragraphProps.paragraph.id,
      contents: contents,
    },
    (resp) => {
      paragraphProps.paragraph.contents = contents
      destroyEditor()
      createView()
      // if(markDownEditor.isMarkdownMode()){
      //   markDownEditor.changeMode("preview")
      // }

      // $('#' + paragraphId()).summernote('destroy')
    },
  )
}

const paragraphId = () => {
  return 'paragraph' + paragraphProps.paragraph.id
}

const editId = () => {
  return 'paragraphEdit' + paragraphProps.paragraph.id
}
const saveId = () => {
  return 'paragraphSave' + paragraphProps.paragraph.id
}

const removeParagraph = () => {
  httpDelete(
    '/document/api/delete/paragraph',
    { paragraphId: paragraphProps.paragraph.id },
    (resp) => {
      emit('deleteSelf', paragraphProps.paragraph.id)
    },
  )
}

const stackedListItemClass = () => {
  return `StackedListItem StackedListItem--item${paragraphProps.paragraph.id} StackedListItem--isDraggable tabindex='1'`
}
</script>

<template>
  <!--  <div :class="stackedListItemClass()">-->
  <div class="StackedListContent">
    <button :id="editId()" class="btn btn-primary" @click="edit" type="button">Edit</button>
    <button :id="saveId()" class="btn btn-primary" @click="save" type="button">Save</button>
    <button href="#" class="btn" @click="removeParagraph">Delete</button>
    <div :id="paragraphId()">
<!--      <div v-html="paragraphProps.paragraph.contents"></div>-->
    </div>
  </div>
  <!--  </div>-->
</template>

<style scoped></style>
