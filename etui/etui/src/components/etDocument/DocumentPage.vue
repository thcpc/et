<script setup>
import { onMounted, onUpdated, ref, watch } from 'vue'
// import Paragraph from "@/components/FullTextParagraph.vue";
import { httpGet, httpPostJson } from '@/core/http.js'
import { etDocumentConst, GlobalConst } from '@/core/const/enums.js'
import PlantUmlParagraph from '@/components/etDocument/PlantUmlParagraph.vue'
import FullTextParagraph from '@/components/etDocument/FullTextParagraph.vue'
import eventBus from '@/core/eventBus.js'
import { v4 as uuidv4 } from 'uuid'
import { etDocumentUrl } from '@/core/const/urls.js'
import { etDocumentEvent } from '@/core/const/events.js'
const pageProps = defineProps(['pageId', 'pageName'])
const localPageId = ref(GlobalConst.UnKnown.ID)
const localPageName = ref(GlobalConst.UnKnown.STR)
const paragraphs = ref([])
let sortable = null

onMounted(() => {
  initFlexbox()
  eventBus.$on(etDocumentEvent.appendNewParagraph, appendNewParagraph)
})

const isFullText = (paragraph) => {
  return paragraph.paragraphType === etDocumentConst.FullText
}
const initFlexbox = () => {
  if (sortable != null) {
    sortable.destroy()
    sortable = null
  }

  const containerSelector = '#SimpleList'
  const containers = document.querySelectorAll(containerSelector)

  sortable = new Draggable.Sortable(containers, {
    draggable: '.StackedListItem--isDraggable',
    group: 'shared',
    sort: true,
    // mirror: {
    //   appendTo: containerSelector,
    //   constrainDimensions: true,
    // },
  })

  sortable.on('sortable:stop', (evt) => {
    if (evt.newIndex - evt.oldIndex !== 0) {
      const regex = /StackedListItem--item(\d+)/
      const match = evt.data.dragEvent.data.source.className.match(regex)

      if (match) {
        const paragraph_id = Number(match[1])
        paragraphs.value.forEach((paragraph) => {
          if (paragraph.id === paragraph_id) {
            paragraph.order = evt.newIndex + 1
          } else {
            if (evt.newIndex - evt.oldIndex > 0) {
              // 从上往下拖
              if (paragraph.order > evt.oldIndex + 1 && paragraph.order <= evt.newIndex + 1) {
                paragraph.order = paragraph.order - 1
              }
            } else {
              // 从下往上拖
              if (paragraph.order >= evt.newIndex + 1 && paragraph.order < evt.oldIndex + 1) {
                paragraph.order = paragraph.order + 1
              }
            }
          }
        })
      } else {
        console.log('未找到匹配的数字')
      }
      let changeOrders = paragraphs.value.map((e) => ({ id: e.id, order: e.order }))
      httpPostJson(etDocumentUrl.moveParagraph, { changeOrders: changeOrders }, () => {})
    }
  })
}

const appendNewParagraph = (newParagraph) => {
  if (newParagraph.changePageId === localPageId.value) {
    paragraphs.value.push(newParagraph.paragraph)
    // initFlexbox()
  }
}

onUpdated(() => {
  initFlexbox()
  // sortable.option("refresh")
})

const uuid = () => {
  return uuidv4()
}

const newParagraph = () => {
  eventBus.$emit(etDocumentEvent.newParagraph, pageProps.pageId)
}

watch(
  () => pageProps.pageId,
  (newValue, oldValue) => {
    httpGet(etDocumentUrl.getPage, { pageId: pageProps.pageId }, (resp) => {
      paragraphs.value = resp
      console.log(paragraphs.value)
      // sortable.option("sort", true)
    })
  },
  { flush: 'post' },
)

watch(
  () => pageProps.pageName,
  (newValue, oldValue) => {
    localPageName.value = newValue
  },
  { flush: 'post' },
)

watch(
  () => paragraphs.value,
  (newValue, oldValue) => {
    initFlexbox()
  },
  { flush: 'post' },
)

const deleteParagraph = (paragraphId) => {
  const index = paragraphs.value.findIndex((e) => e.id === paragraphId)
  if (index !== -1) {
    paragraphs.value.splice(index, 1)
  }
}

const stackedListItemClass = (paragraph) => {
  return `StackedListItem StackedListItem--item${paragraph.id} StackedListItem--isDraggable tabindex='1'`
}
</script>

<template>
  <div class="card-header">
    <h3 class="card-title">{{ localPageName }}</h3>
    <div class="card-actions">
      <a
        href="#"
        class="btn btn-primary"
        data-bs-toggle="modal"
        data-bs-target="#newParagraph"
        @click="newParagraph()"
      >
        <!-- Download SVG icon from http://tabler-icons.io/i/plus -->
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="icon"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          stroke-width="2"
          stroke="currentColor"
          fill="none"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path stroke="none" d="M0 0h24v24H0z" fill="none" />
          <path d="M12 5l0 14" />
          <path d="M5 12l14 0" />
        </svg>
        Add new
      </a>
    </div>
  </div>
  <div class="card-body">
    <section class="SimpleList">
      <article id="SimpleList" class="StackedListWrapper StackedListWrapper--hasScrollIndicator">
        <div v-for="paragraph in paragraphs" :key="uuid()" :class="stackedListItemClass(paragraph)">
          <div v-if="isFullText(paragraph)">
            <full-text-paragraph :paragraph="paragraph" @deleteSelf="deleteParagraph" />
          </div>
          <div v-else>
            <plant-uml-paragraph :paragraph="paragraph" @deleteSelf="deleteParagraph" />
          </div>
        </div>
      </article>
    </section>
  </div>
</template>

<style scoped></style>
