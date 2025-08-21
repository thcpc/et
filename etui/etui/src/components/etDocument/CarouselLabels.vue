<script setup>
import { onMounted, ref, watch } from 'vue'
import { GlobalConst } from '@/core/const/enums.js'
import { httpPostJson } from '@/core/http.js'
import { etDocumentUrl } from '@/core/const/urls.js'

const data = defineProps(['categories','selectedLabels', "op", 'disableNew'])
const newLabelValue = ref(GlobalConst.UnKnown.EMPTY)
const currentCategory = ref(GlobalConst.UnKnown.ID)
const localSelectedLabels = ref([])
const emit = defineEmits(['updateSelectedLabels'])
const href = (category) => {
  return '#tabs-' + category.id + "-" + data.op.value
}

const id = (category) => {
  return 'tabs-' + category.id + "-" + data.op.value
}


const choseCategory = (id) => {
  currentCategory.value = id
}

const newLabel = () => {
  httpPostJson(
    etDocumentUrl.newLabel,
    {
      categoryId: currentCategory.value,
      name: newLabelValue.value,
    },
    (resp) => {
      data.categories.forEach((c, index) => {
        if (c.id === currentCategory.value) {
          c.labels.push(resp)
        }
      })
    },
  )
}


watch(
  () => data.selectedLabels,
  (newValue, oldValue) => {

    localSelectedLabels.value = data.selectedLabels
  },
  { flush: 'post' },
)

watch(
  () => localSelectedLabels.value,
  (newValue, oldValue) => {
    emit('updateSelectedLabels', localSelectedLabels.value)
  },
  { flush: 'post' },
)


watch(
  () => currentCategory.value,
  (newValue, oldValue) => {
    newLabelValue.value = GlobalConst.UnKnown.EMPTY
  },
  { flush: 'post' },
)

onMounted(() => {
  const modal = document.getElementById('CategoryTab')

  modal.addEventListener('hide.bs.tab', () => {
    newLabelValue.value = GlobalConst.UnKnown.EMPTY
  })
})

const tabClass = (index)=>{

  if(index === 0){
    return "tab-pane active show"
  }else{
    return "tab-pane"
  }
}

const linkClass = (index)=>{
  if(index === 0){
    return "nav-link active"
  }else{
    return "nav-link"
  }
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      <ul class="nav nav-tabs card-header-tabs nav-fill" data-bs-toggle="tabs" id="CategoryTab">
        <li v-for="(item, index) in data.categories" class="nav-item" :key="index">
          <a
            :href="href(item)"
            :class="linkClass(index)"
            data-bs-toggle="tab"
            @click="choseCategory(item.id)"
            >{{ item.name }}</a
          >
        </li>
      </ul>
    </div>
    <div class="card-body">
      <div class="tab-content">
        <div
          :class="tabClass(index)"
          v-for="(category, index) in data.categories"
          :id="id(category)"
          :key="index"
        >
          <div class="form-selectgroup form-selectgroup-pills">
            <label v-for="label in category.labels" class="form-selectgroup-item" :key="label">
              <input type="checkbox" :value="label.id" class="form-selectgroup-input" v-model="localSelectedLabels" />
              <span class="form-selectgroup-label">{{ label.name }}</span>
            </label>
          </div>
          <div class="card-body">
<!--            <div class="hr-text hr-text-center hr-text-spaceless">新标签</div>-->
          </div>
          <div v-show="data.disableNew.value===false" class="card-body">
            <div class="mb-9">
              <div class="row g-10">
                <div class="col-2">
                  <input type="text" class="form-control" v-model="newLabelValue" placeholder="添加新标签" />
                </div>
                <div class="col-1">
                  <a href="#" class="btn btn-icon" aria-label="Button" @click="newLabel()">
                    <!-- Download SVG icon from http://tabler-icons.io/i/search -->
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      class="icon icon-tabler icons-tabler-outline icon-tabler-location-plus"
                    >
                      <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                      <path d="M12 18l-2 -4l-7 -3.5a.55 .55 0 0 1 0 -1l18 -6.5l-3.361 9.308" />
                      <path d="M16 19h6" />
                      <path d="M19 16v6" />
                    </svg>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
