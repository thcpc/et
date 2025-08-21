<script setup>

import { EditorState } from '@codemirror/state'

import {onMounted, ref} from 'vue'
import { EditorView } from '@codemirror/view'

const paragraphProps = defineProps(['paragraph'])

import { basicSetup } from "codemirror";
import { encode } from 'plantuml-encoder';
import eventBus from "@/core/eventBus.js";
import { httpPostJson } from "@/core/http.js";
import { etDocumentUrl } from '@/core/const/urls.js'
import { etDocumentEvent } from '@/core/const/events.js'

// const plantUMLHighlightStyle = HighlightStyle.define([
//   { tag: tags.keyword, color: '#00f' }, // 关键字为蓝色
//   { tag: tags.comment, color: '#888' }, // 注释为灰色
//   { tag: tags.string, color: '#a11' }, // 字符串为红色
//   { tag: tags.operator, color: '#f50' }, // 操作符为橙色
// ])
const plantUMLImage = ref('');
const isDisplayImage = ref(true)
const editorContainer = ref(null)
let editorView = null
const edit = () => {
  if (!editorView) {
    isDisplayImage.value = false
    const state = EditorState.create({
      doc: paragraphProps.paragraph.contents,
      extensions: [
        basicSetup,
        // syntaxHighlighting(plantUMLHighlightStyle),
        EditorView.updateListener.of((update) => {
          if (update.docChanged) {
            // const content = update.state.doc.toString()
            paragraphProps.paragraph.contents = update.state.doc.toString()
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

onMounted(()=>{
  const encoded = encode(paragraphProps.paragraph.contents);
  plantUMLImage.value = `http://www.plantuml.com/plantuml/svg/${encoded}`;
})

const preview = ()=>{
  eventBus.$emit(etDocumentEvent.previewPlantuml, paragraphProps.paragraph.contents)
}

const save = () => {
  httpPostJson(
    etDocumentUrl.updateParagraph,
    {
      paragraphId: paragraphProps.paragraph.id,
      contents: paragraphProps.paragraph.contents,
    },
    (resp) => {
      // paragraphProps.paragraph.contents = $('#' + paragraphId()).summernote('code')
      isDisplayImage.value = true
      if (editorView) {
        editorView.destroy()
        editorView = null
        const encoded = encode(paragraphProps.paragraph.contents);
        plantUMLImage.value = `http://www.plantuml.com/plantuml/svg/${encoded}`;
      }
    },
  )
}

const paragraphId = () => {
  return 'paragraph' + paragraphProps.paragraph.id
}

const editId = ()=>{
  return 'paragraphEdit' + paragraphProps.paragraph.id
}
const saveId = ()=>{
  return 'paragraphSave' + paragraphProps.paragraph.id
}
const previewId = ()=>{
  return 'paragraphPreview' + paragraphProps.paragraph.id
}


</script>

<template>
<!--  <div class="StackedListItem StackedListItem&#45;&#45;item StackedListItem&#45;&#45;isDraggable">-->
    <div class="StackedListContent">
      <button :id="editId()" class="btn btn-primary" @click="edit" type="button">edit</button>
      <button :id="saveId()" class="btn btn-primary" @click="save" type="button">save</button>
      <button :id="previewId()" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#plantUmlModal" @click="preview" type="button">preview</button>
      <div :id="paragraphId()">
        <div v-show="!isDisplayImage" ref="editorContainer"></div>
        <img v-show="isDisplayImage" :src="plantUMLImage" alt="PlantUML Diagram">
      </div>
      <div class="Pattern Pattern--typeHalftone"></div>
      <div class="Pattern Pattern--typePlaced"></div>
    </div>
<!--  </div>-->
</template>

<style scoped>
.CodeMirror {
  border: 1px solid #ddd;
  height: auto;
}
</style>
