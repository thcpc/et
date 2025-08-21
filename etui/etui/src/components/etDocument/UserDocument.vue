<script setup>
import {onMounted, ref} from "vue";
import DocumentPage from "@/components/etDocument/DocumentPage.vue";
import {httpGet} from "@/core/http.js";
import { GlobalConst } from '@/core/const/enums.js'
// import eventBus from "@/core/eventBus.js";
import SnapshotModal from "@/components/etDocument/modals/SnapshotModal.vue";
import { etDocumentUrl } from '@/core/const/urls.js'

const docProps = defineProps(["docId"])
const doc = ref({})
const pages = ref([])
const displayPageId = ref(GlobalConst.UnKnown.ID)
const displayPageName = ref(GlobalConst.UnKnown.STR)



onMounted(() => {
  httpGet(etDocumentUrl.getDocument, {docId: docProps.docId, includePage: true}, (resp) => {
    doc.value = resp.document
    pages.value = resp.pages
    displayPageId.value = pages.value[0].id
    displayPageName.value = pages.value[0].name
  })

})




const changeDisplayPage = (page)=>{
  displayPageId.value = page.id
  displayPageName.value = page.name

}
</script>

<template>
  <snapshot-modal :doc-id="docId"/>
  <div class="page" id="docApp">
    <!-- Navbar -->
    <div class="page-wrapper">
      <!-- DocumentPage header -->
      <div class="page-header d-print-none">
        <div class="container-xl">
          <div class="row g-2 align-items-center">
            <div class="col">
              <h2 class="page-title">
                {{doc.name}}
              </h2>
            </div>
          </div>
        </div>
      </div>
      <!-- DocumentPage body -->
      <div class="page-body">
        <div class="container-xl">
          <div class="card">
            <div class="row g-0">
              <div class="col-12 col-md-3 border-end">
                <div class="card-body">
                  <div class="list-group list-group-transparent">
                    <a href="#" class="list-group-item list-group-item-action d-flex align-items-center" v-for="(page,index) in pages" :key="index"
                       @click="()=> changeDisplayPage(page)">
                      {{page.name}}
                    </a>
                  </div>
                </div>
                <button class="btn" data-bs-toggle="modal" data-bs-target="#snapshotModal">快照标记</button>
              </div>
              <div class="col-12 col-md-9 d-flex flex-column">
                <document-page :page-id="displayPageId" :page-name="displayPageName"/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<style scoped>

</style>
