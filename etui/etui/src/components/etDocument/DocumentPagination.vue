<script setup>
import { ref, watch } from 'vue'

const data = defineProps(['totalPage', 'currentPage', 'perCount', 'count'])
const pageRangeStart = ref(0)
const paginationPage = ref([])
const emit = defineEmits(['goPage'])

watch(
  () => data.totalPage,
  (newValue, oldValue) => {
    paginationPage.value = Array.from({ length: newValue }, (_, index) => index + 1)
  },
)

const goPageNo = (offset) => {
  return pageRangeStart.value + offset
}

const goPage = (offset) => {
  let pageNo = goPageNo(offset)
  emit('goPage', pageNo)
}

const nextPage = () => {
  pageRangeStart.value = pageRangeStart.value + 1
}

const prevPage = () => {
  pageRangeStart.value = pageRangeStart.value - 1
}

const prevClass = () => {
  if (pageRangeStart.value > 0) {
    return 'page-item'
  } else {
    return 'page-item disabled'
  }
}

const nextClass = () => {
  if (pageRangeStart.value + paginationPage.value.length < data.totalPage) {
    return 'page-item'
  } else {
    return 'page-item disabled'
  }
}
</script>

<template>
  <p class="m-0 text-secondary">
    Showing <span>1</span> to <span>{{ data.count }}</span> of <span>{{ data.perCount }}</span>
    entries
  </p>
  <ul class="pagination m-0 ms-auto">
    <li :class="prevClass()">
      <a class="page-link" href="#" tabindex="-1" aria-disabled="true" @click="prevPage()">
        <!-- Download SVG icon from http://tabler-icons.io/i/chevron-left -->
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
          <path d="M15 6l-6 6l6 6" />
        </svg>
        prev
      </a>
    </li>
    <li class="page-item" v-for="index in paginationPage" :key="index">
      <a class="page-link" href="#" @click="goPage(index)">{{ goPageNo(index) }}</a>
    </li>
    <!--    <li class="page-item"><a class="page-link" href="#">1</a></li>-->
    <!--    <li class="page-item active"><a class="page-link" href="#">2</a></li>-->
    <!--    <li class="page-item"><a class="page-link" href="#">3</a></li>-->
    <!--    <li class="page-item"><a class="page-link" href="#">4</a></li>-->
    <!--    <li class="page-item"><a class="page-link" href="#">5</a></li>-->
    <li :class="nextClass()">
      <a class="page-link" href="#" @click="nextPage()">
        next
        <!-- Download SVG icon from http://tabler-icons.io/i/chevron-right -->
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
          <path d="M9 6l6 6l-6 6" />
        </svg>
      </a>
    </li>
  </ul>
</template>

<style scoped></style>
