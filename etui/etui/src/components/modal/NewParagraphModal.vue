<script setup>
import { Constant, UnKnown } from '@/core/enums.js'
import { onMounted, ref, watch } from 'vue'
import eventBus from '@/core/eventBus.js'
import { encode } from 'plantuml-encoder'
import { EditorState } from '@codemirror/state'
import { basicSetup } from 'codemirror'
import { syntaxHighlighting } from '@codemirror/language'
import { EditorView } from '@codemirror/view'
import {httpGet, httpPostForm, httpPostJson} from '@/core/http.js'
import Editor from '@toast-ui/editor';

const pageId = ref(UnKnown.ID)
const paragraphType = ref(Constant.FullText)

const paragraphContent = ref('')
const paragraphImage = ref('')
// const isDisplayImage = ref(true)
const editorContainer = ref(null)
const isPreview = ref(false)

onMounted(() => {
  eventBus.$on('newParagraph', (id) => {
    pageId.value = id
  })

  const modal = document.getElementById('newParagraph')
  modal.addEventListener('hide.bs.modal', () => {

    clearData()
    if (paragraphType.value === Constant.FullText) {
      destroyFullText()
    } else if (paragraphType.value === Constant.PlantUml) {
      destroyPlantuml()
    }
    paragraphType.value = Constant.FullText


  })

  modal.addEventListener('shown.bs.modal', () => {

    createFullText()
  })
})

const clearData = ()=>{
  pageId.value = UnKnown.ID
  isPreview.value = false
  editorContainer.value = null
  paragraphContent.value = ""
  paragraphImage.value = ""
}

const preview = () => {
  isPreview.value = true
  if (paragraphType.value === Constant.PlantUml) {
    destroyPlantuml()
    const encoded = encode(paragraphContent.value)
    paragraphImage.value = `http://www.plantuml.com/plantuml/svg/${encoded}`
  }
  // } else if (paragraphType.value === Constant.FullText) {
  //   destroyFullText()
  // }
}

const edit = () => {
  isPreview.value = false
  if (paragraphType.value === Constant.PlantUml) {
    createPlantuml()
  } else if (paragraphType.value === Constant.FullText) {
    createFullText()
  }
}

let markDownEditor = null
const createFullText = () => {

  if(!markDownEditor){
    markDownEditor = new Editor({
      el: document.querySelector('#paragraphEditor'),
      initialValue: paragraphContent.value,
      previewStyle: 'vertical'
    });
  }

  // $('#paragraphEditor').summernote({
  //   focus: true,
  // })
}

const destroyFullText = () => {
  // paragraphContent.value = $('#paragraphEditor').summernote('code')
  // $('#paragraphEditor').summernote('destroy')
  if (markDownEditor) {
    paragraphContent.value = markDownEditor.getMarkdown()
    markDownEditor.destroy()
    markDownEditor = null
  }
}

const submit = () =>{
  let contents = ""
  if(paragraphType.value === Constant.PlantUml){
    contents = paragraphContent.value
  }else if(paragraphType.value === Constant.FullText){
    // contents = $('#paragraphEditor').summernote('code')
    contents = markDownEditor.getMarkdown()
  }
  httpPostJson('/document/api/new/paragraph', {contents: contents, pageId: pageId.value, paragraphType: paragraphType.value},(resp)=>{
    $('#newParagraph').modal('hide');
    eventBus.$emit("appendNewParagraph", {changePageId: pageId.value, paragraph: {id:resp.id, order:resp.order, contents:contents,paragraphType: resp.paragraphType}})
  },()=>{
    $('#newParagraph').modal('hide');
  })
}





let editorView = null
const createPlantuml = () => {
  if (!editorView) {
    const state = EditorState.create({
      doc: paragraphContent.value,
      extensions: [
        basicSetup,
        // syntaxHighlighting(plantUMLHighlightStyle),
        EditorView.updateListener.of((update) => {
          if (update.docChanged) {
            // const content = update.state.doc.toString()
            paragraphContent.value = update.state.doc.toString()
          }
        }),
      ],
    })
    editorView = new EditorView({
      state,
      parent: editorContainer.value,
    })
  }
}

watch(
  () => paragraphType.value,
  (newValue, oldValue) => {
    if (newValue === Constant.FullText) {
      destroyPlantuml()
      createFullText()
    } else if (newValue === Constant.PlantUml) {
      destroyFullText()
      createPlantuml()
    }

  },
  { flush: 'post' },
)

const destroyPlantuml = () => {
  if (editorView) {
    editorView.destroy()
    editorView = null
  }
}
</script>

<template>
  <div class="modal" id="newParagraph" tabindex="-1" aria-hidden="true" role="dialog">
    <div class="modal-dialog modal-lg" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">配置</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <select class="form-select" v-model="paragraphType">
            <option :value="Constant.FullText">富文本</option>
            <option :value="Constant.PlantUml">PlantUml</option>
          </select>
          <div v-show="paragraphType === Constant.FullText">
            <div id="paragraphEditor"></div>
          </div>
          <div v-show="paragraphType === Constant.PlantUml">
            <div v-show="!isPreview" ref="editorContainer"></div>
            <img v-show="isPreview" :src="paragraphImage" alt="PlantUML Diagram" />
          </div>
        </div>
        <div class="modal-footer">
          <a v-show="isPreview === false" href="#" class="btn" @click="preview()">Preview</a>
          <a v-show="isPreview === true" href="#" class="btn" @click="edit()">Edit</a>

          <a href="#" class="btn" @click="submit()">Save</a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
