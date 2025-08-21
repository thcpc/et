<script setup>
import { httpGet, httpPostJson } from '@/core/http.js'
import { onMounted, ref } from 'vue'
import eventBus from '@/core/eventBus.js'
import CarouselLabels from '@/components/etDocument/CarouselLabels.vue'
import { etDocumentConst } from '@/core/const/enums.js'
import { etDocumentUrl } from '@/core/const/urls.js'
import { etDocumentEvent } from '@/core/const/events.js'


const documentName = defineModel()

const businessCategories = ref([])
const selectedLabels = ref([])
const currentPage = ref(1)
const functionCategories = ref([])

const submit = () => {
  httpPostJson(
    etDocumentUrl.newDocument,
    {
      name: documentName.value,
      labels: selectedLabels.value,
    },
    (resp) => {
      eventBus.$emit(etDocumentEvent.refreshDocumentList, 1)
      $('#newDocument').modal('hide')
    },
    () => {
      $('#newDocument').modal('hide')
    },
  )
}

const updateSelectedLabel = (selected) => {
  selectedLabels.value = selected
}

const nextPage = () => {
  currentPage.value += 1
  const myCarouselElement = document.querySelector('#new-carousel-indicators')
  let carousel = new bootstrap.Carousel(myCarouselElement)
  carousel.next()
}

const prePage = () => {
  currentPage.value -= 1
  const myCarouselElement = document.querySelector('#new-carousel-indicators')
  let carousel = new bootstrap.Carousel(myCarouselElement)
  carousel.prev()
}

onMounted(() => {
  const modal = document.getElementById('newDocument')

  modal.addEventListener('shown.bs.modal', () => {
    currentPage.value = 1
    httpGet(etDocumentUrl.getLabels, {}, (resp) => {
      businessCategories.value = resp.filter((c) => c.category_type === etDocumentConst.Business)
      functionCategories.value = resp.filter((c) => c.category_type === etDocumentConst.Function)
    })
  })

  modal.addEventListener('hide.bs.modal', () => {
    currentPage.value = 1
    const e = bootstrap.Carousel.getInstance(document.getElementById('new-carousel-indicators'))
    if (e) {
      e.to('0')
    }
  })
})

const title = () => {
  return ['基础信息', '功能标签', '业务标签'][currentPage.value - 1]
}
</script>

<template>
  <div class="modal" id="newDocument" tabindex="-1" aria-hidden="true" role="dialog">
    <div class="modal-dialog modal-full-width modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title() }}</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div id="new-carousel-indicators" class="carousel carousel-dark slide">
            <!--            <div class="carousel-indicators">-->
            <!--              <button type="button" data-bs-target="#carousel-indicators" data-bs-slide-to="0" class=" active"></button>-->
            <!--              <button type="button" data-bs-target="#carousel-indicators" data-bs-slide-to="1" class=""></button>-->
            <!--            </div>-->
            <div class="carousel-inner">
              <div class="carousel-item active">
                <div class="mb-3">
                  <label class="form-label required">文档名</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="documentName"
                    name="example-required-input"
                    placeholder="文档名"
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label"
                    >文档概述 <span class="form-label-description">56/100</span></label
                  >
                  <textarea
                    class="form-control"
                    name="example-textarea-input"
                    rows="6"
                    placeholder="概述文档目的,功能"
                  >
Oh! Come and see the violence inherent in the system! Help, help, I'm being repressed! We shall say 'Ni' again to you, if you do not appease us. I'm not a witch. I'm not a witch. Camelot!</textarea
                  >
                </div>
                <!--                <input v-model="documentName" />-->
              </div>
              <div class="carousel-item">
                <carousel-labels
                  :categories="functionCategories"
                  @update-selected-labels="updateSelectedLabel"
                  :selected-labels="selectedLabels"
                  :op="ref('new')"
                  :disable-new="ref(true)"
                />
              </div>
              <div class="carousel-item">
                <carousel-labels
                  :categories="businessCategories"
                  @update-selected-labels="updateSelectedLabel"
                  :selected-labels="selectedLabels"
                  :op="ref('new')"
                  :disable-new="ref(false)"
                />
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button v-show="currentPage > 1" type="button" class="btn" @click="prePage()">
            上一步
          </button>
          <button v-show="currentPage < 3" type="button" class="btn active" @click="nextPage()">
            下一步
          </button>
          <a v-show="currentPage > 2" href="#" class="btn" @click="submit()">提交</a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
