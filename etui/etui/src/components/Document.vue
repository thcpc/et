<script setup>
import {onMounted, ref} from "vue";
import Page from "@/components/Page.vue";
import {httpGet} from "@/core/http.js";
import {UnKnown} from "@/core/enums.js";
import eventBus from "@/core/eventBus.js";
import SnapshotModal from "@/components/modal/SnapshotModal.vue";

const docProps = defineProps(["docId"])
const doc = ref({})
const pages = ref([])
const displayPageId = ref(UnKnown.ID)
const displayPageName = ref(UnKnown.STR)



onMounted(() => {
  httpGet('/document/api/document', {docId: docProps.docId, includePage: true}, (resp) => {
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
      <!-- Page header -->
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
      <!-- Page body -->
      <div class="page-body">
        <div class="container-xl">
          <div class="card">
            <div class="row g-0">
              <div class="col-12 col-md-3 border-end">
                <div class="card-body">
                  <div class="list-group list-group-transparent">
                    <a href="#" class="list-group-item list-group-item-action d-flex align-items-center" v-for="page in pages" @click="()=> changeDisplayPage(page)">
                      {{page.name}}
                    </a>
                  </div>
                </div>
                <button class="btn" data-bs-toggle="modal" data-bs-target="#snapshotModal">快照标记</button>
              </div>
              <div class="col-12 col-md-9 d-flex flex-column">
                <page :page-id="displayPageId" :page-name="displayPageName"/>
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
