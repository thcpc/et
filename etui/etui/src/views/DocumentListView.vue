<script setup>
import { onMounted, ref } from 'vue'
import { httpDelete, httpGet } from '@/core/http.js'
import eventBus from '@/core/eventBus.js'
import { useRouter } from 'vue-router'
import { dateFormat } from '@/core/utils.js'
import {DocTab, TaskType, UnKnown} from '@/core/enums.js'
import EditDocumentModal from '@/components/modal/EditDocumentModal.vue'
import Pagination from '@/components/Pagination.vue'
import Navigation from '@/components/Navigation.vue'

const documents = ref([])
const router = useRouter()
const editDocumentID = ref(UnKnown.ID)
const perCount = ref(7)
const totalPage = ref(0)
const currentTab = ref(DocTab.User)
const currentPageNo = ref(1)

onMounted(() => {
  // eventBus.$on('appendNewDocument', appendNewDocument)
  get_user_documents()
  eventBus.$on('refresh-document-list', refresh)
})

const get_documents = (url, pageNo, tab) => {
  httpGet(url, { pageNo: pageNo, perCount: perCount.value }, (resp) => {
    documents.value = resp.documents
    currentPageNo.value = pageNo
    totalPage.value = resp.totalPage
    currentTab.value = tab
  })
}

const get_all_documents = () => {
  get_documents('/document/api/documents', 1, DocTab.All)
}

const get_user_documents = () => {
  get_documents('/document/api/user/documents', 1, DocTab.User)
}

const get_user_task = () => {
  get_documents('/task/api/user/tasks', 1, DocTab.Task)
}

const refresh = (pageNo) => {
  let no = currentPageNo.value
  if(pageNo){
    no = pageNo
  }
  console.log(no)
  if (currentTab.value === DocTab.All) {
    get_documents('/document/api/documents', no, DocTab.All)
  } else if (currentTab.value === DocTab.User) {
    get_documents('/document/api/user/documents', no, DocTab.User)
  } else if (currentTab.value === DocTab.Task) {
    get_documents('/task/api/user/tasks', no, DocTab.Task)
  }
}

const goPageAll = (pageNo) => {
  get_documents('/document/api/documents', pageNo, DocTab.All)
}

const goPageUser = (pageNo) => {
  get_documents('/document/api/user/documents', pageNo, DocTab.User)
}

const goUserTask = (pageNo) => {
  get_documents('/task/api/user/tasks', pageNo, DocTab.Task)
}

const newWindow = (doc) => {
  return router.resolve({ name: 'testCaseDetail', params: { id: doc.id } }).href
}

const reAssignee = (assignee) =>{
  eventBus.$emit("reAssigneeTask", assignee)

}

const rollBack = (task) => {
  eventBus.$emit("rollBackTask", task)
}


const openEditDocument = (doc) => {
  editDocumentID.value = doc.id
}

const closeEditDocument = () => {
  editDocumentID.value = UnKnown.ID
  refresh()
}

const appendNewDocument = (document) => {
  documents.value.push(document)
}

const deleteDocument = (document) => {
  httpDelete('/document/api/delete/document', { documentId: document.id }, () => {
    const index = documents.value.findIndex((e) => e.id === document.id)
    if (index !== -1) {
      documents.value.splice(index, 1)
    }
  })
}

const taskStatus = (state) => {
  if (state === 0) {
    return '待办'
  } else if (state === 1) {
    return '待机'
  } else if (state === 3) {
    return '完成'
  }
}

const doTask = (task)=>{
  if(task.task_type === TaskType.AssignAutoTask){
    eventBus.$emit("AssigneeAutoTestTask", task)
  }
}

const labelSpanClass = (label) => {
  if (label.startsWith('#EDC')) {
    return 'badge bg-blue text-blue-fg'
  } else if (label.startsWith('#CRF DESIGN')) {
    return 'badge bg-azure text-azure-fg'
  } else if (label.startsWith('#PV')) {
    return 'badge bg-indigo text-indigo-fg'
  } else if (label.startsWith('#CTMS')) {
    return 'badge bg-purple text-purple-fg'
  } else if (label.startsWith('#eTMF')) {
    return 'badge bg-pink text-pink-fg'
  } else if (label.startsWith('#ADMIN')) {
    return 'badge bg-red text-red-fg'
  } else if (label.startsWith('#CMD')) {
    return 'badge bg-orange text-orange-fg'
  } else if (label.startsWith('#ProCheck')) {
    return 'badge bg-yellow text-yellow-fg'
  } else if (label.startsWith('#Medical Coding')) {
    return 'badge bg-lime text-lime-fg'
  } else if (label.startsWith('#Medical Image')) {
    return 'badge bg-green text-green-fg'
  } else if (label.startsWith('#IRC')) {
    return 'badge bg-teal text-teal-fg'
  } else if (label.startsWith('#其它')) {
    return 'badge bg-cyan text-cyan-fg'
  } else if (label.startsWith('@')) {
    return 'badge bg-dark text-dark-fg'
  }
}
</script>

<template>
  <edit-document-modal :id="editDocumentID" @close="closeEditDocument" />
  <div class="page">
    <navigation />
    <header class="navbar-expand-md">
      <div class="collapse navbar-collapse" id="navbar-menu">
        <div class="navbar">
          <div class="container-xl">
            <div class="row offset-9">
              <div class="my-2 my-md-0 flex-grow-1 flex-md-grow-0 order-first order-md-last">
                <a
                  href="#"
                  class="btn btn-primary"
                  data-bs-toggle="modal"
                  data-bs-target="#newDocument"
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
                  创建新文档
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
    <div class="page-wrapper-full">
      <div class="page-body">
        <div class="container-xl">
          <div class="row row-cards">
            <div class="col-md-12">
              <div class="card">
                <div class="card-header">
                  <ul class="nav nav-tabs card-header-tabs nav-fill" data-bs-toggle="tabs">
                    <li class="nav-item">
                      <a
                        href="#tabs-home"
                        class="nav-link"
                        data-bs-toggle="tab"
                        @click="get_all_documents()"
                      >
                        <!-- Download SVG icon from http://tabler-icons.io/i/home -->
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          class="icon me-2"
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
                          <path d="M5 12l-2 0l9 -9l9 9l-2 0" />
                          <path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-7" />
                          <path d="M9 21v-6a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v6" />
                        </svg>
                        所有文档</a
                      >
                    </li>
                    <li class="nav-item">
                      <a
                        href="#tabs-mine"
                        class="nav-link active"
                        data-bs-toggle="tab"
                        @click="get_user_documents()"
                      >
                        <!-- Download SVG icon from http://tabler-icons.io/i/user -->
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          class="icon me-2"
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
                          <path d="M8 7a4 4 0 1 0 8 0a4 4 0 0 0 -8 0" />
                          <path d="M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" />
                        </svg>
                        我写的</a
                      >
                    </li>
                    <li class="nav-item">
                      <a
                        href="#tabs-task"
                        class="nav-link"
                        data-bs-toggle="tab"
                        @click="get_user_task()"
                      >
                        <!-- Download SVG icon from http://tabler-icons.io/i/activity -->
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          class="icon me-2"
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
                          <path d="M3 12h4l3 8l4 -16l3 8h4" />
                        </svg>
                        需要我处理的</a
                      >
                    </li>
                  </ul>
                </div>
                <div class="card-body">
                  <div class="tab-content">
                    <div class="tab-pane" id="tabs-home">
                      <div class="card" v-if="currentTab === DocTab.All">
                        <div class="card-header">
                          <div class="input-icon">
                            <span class="input-icon-addon">
                              <!-- Download SVG icon from http://tabler-icons.io/i/search -->
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
                                <path d="M10 10m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0" />
                                <path d="M21 21l-6 -6" />
                              </svg>
                            </span>
                            <input
                              type="text"
                              value=""
                              class="form-control"
                              placeholder="Search…"
                              aria-label="Search in website"
                            />
                          </div>
                        </div>
                        <div class="card-body">
                          <div class="table-responsive">
                            <table
                              class="table card-table table-vcenter text-nowrap datatable align-middle"
                            >
                              <thead>
                                <tr>
                                  <th class="w-1">No.</th>
                                  <th>文档名</th>
                                  <th>作者</th>
                                  <th>标签</th>
                                  <th>状态</th>
                                  <th>更新时间</th>
                                  <th></th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr v-for="doc in documents" :key="doc.id">
                                  <td>
                                    <span class="text-secondary">{{ doc.id }}</span>
                                  </td>
                                  <td>
                                    <a :href="newWindow(doc)" target="_blank">{{ doc.name }}</a>
                                  </td>
                                  <td>{{ doc.author }}</td>
                                  <td>
                                    <div class="badges-list">
                                      <span
                                        :class="labelSpanClass(label)"
                                        v-for="label in doc.labels"
                                        >{{ label }}</span
                                      >
                                    </div>
                                  </td>
                                  <td></td>
                                  <td>{{ dateFormat(doc.modify_dt) }}</td>
                                  <td class="text-end">
                                    <div class="btn-list flex-nowrap">
                                      <a
                                        href="#"
                                        class="btn"
                                        data-bs-toggle="modal"
                                        data-bs-target="#editDocument"
                                        @click="openEditDocument(doc)"
                                      >
                                        编辑
                                      </a>
                                      <a
                                        href="#"
                                        class="btn btn-danger"
                                        @click="deleteDocument(doc)"
                                      >
                                        删除
                                      </a>
                                    </div>
                                  </td>
                                </tr>
                              </tbody>
                            </table>
                          </div>
                        </div>

                        <div class="card-footer d-flex align-items-center">
                          <pagination
                            @go-page="goPageAll"
                            :per-count="perCount"
                            :total-page="totalPage"
                          />
                        </div>
                      </div>
                    </div>
                    <div class="tab-pane active show" id="tabs-mine">
                      <div class="card" v-if="currentTab === DocTab.User">
                        <div class="card-header">
                          <div class="input-icon">
                            <span class="input-icon-addon">
                              <!-- Download SVG icon from http://tabler-icons.io/i/search -->
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
                                <path d="M10 10m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0" />
                                <path d="M21 21l-6 -6" />
                              </svg>
                            </span>
                            <input
                              type="text"
                              value=""
                              class="form-control"
                              placeholder="Search…"
                              aria-label="Search in website"
                            />
                          </div>
                        </div>
                        <div class="card-body">
                          <div class="table-responsive">
                            <table
                              class="table card-table table-vcenter text-nowrap datatable align-middle"
                            >
                              <thead>
                                <tr>
                                  <th class="w-1">No.</th>
                                  <th>文档名</th>
                                  <th>作者</th>
                                  <th>标签</th>
                                  <th>状态</th>
                                  <th>更新时间</th>
                                  <th></th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr v-for="doc in documents" :key="doc.id">
                                  <td>
                                    <span class="text-secondary">{{ doc.id }}</span>
                                  </td>
                                  <td>
                                    <a :href="newWindow(doc)" target="_blank">{{ doc.name }}</a>
                                  </td>
                                  <td>{{ doc.author }}</td>
                                  <td>
                                    <div class="badges-list">
                                      <span
                                        :class="labelSpanClass(label)"
                                        v-for="label in doc.labels"
                                        >{{ label }}</span
                                      >
                                    </div>
                                  </td>
                                  <td></td>
                                  <td>{{ dateFormat(doc.modify_dt) }}</td>
                                  <td class="text-end">
                                    <div class="btn-list flex-nowrap">
                                      <a
                                        href="#"
                                        class="btn"
                                        data-bs-toggle="modal"
                                        data-bs-target="#editDocument"
                                        @click="openEditDocument(doc)"
                                      >
                                        编辑
                                      </a>
                                      <a
                                        href="#"
                                        class="btn btn-danger"
                                        @click="deleteDocument(doc)"
                                      >
                                        删除
                                      </a>
                                    </div>
                                  </td>
                                </tr>
                              </tbody>
                            </table>
                          </div>
                        </div>

                        <div class="card-footer d-flex align-items-center">
                          <pagination
                            @go-page="goPageUser"
                            :per-count="perCount"
                            :total-page="totalPage"
                          />
                        </div>
                      </div>
                    </div>
                    <div class="tab-pane" id="tabs-task">
                      <div class="card" v-if="currentTab === DocTab.Task">
                        <div class="card-header">
                          <div class="input-icon">
                            <span class="input-icon-addon">
                              <!-- Download SVG icon from http://tabler-icons.io/i/search -->
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
                                <path d="M10 10m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0" />
                                <path d="M21 21l-6 -6" />
                              </svg>
                            </span>
                            <input
                              type="text"
                              value=""
                              class="form-control"
                              placeholder="Search…"
                              aria-label="Search in website"
                            />
                          </div>
                        </div>
                        <div class="card-body">
                          <div class="table-responsive">
                            <table
                              class="table card-table table-vcenter text-nowrap datatable align-middle"
                            >
                              <thead>
                                <tr>
                                  <th class="w-1">No.</th>
                                  <th>文档</th>
                                  <th>任务创建者</th>
                                  <!--                                  <th>发布</th>-->
                                  <th>任务说明</th>
                                  <th>任务状态</th>
                                  <th>任务创建时间</th>
                                  <!--                                  <th>任务类型</th>-->
                                  <th></th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr v-for="doc in documents" :key="doc.id">
                                  <td>
                                    <span class="text-secondary">{{ doc.id }}</span>
                                  </td>
                                  <td>
                                    <a :href="newWindow(doc)" target="_blank">{{ doc.name }}</a>
                                    <div class="text-secondary">
                                      {{ doc.snapshot.name }}
                                    </div>
                                  </td>
                                  <td>{{ doc.task.create_by }}</td>
                                  <!--                                  <td>{{ doc.snapshot.name}}</td>-->
                                  <td style="white-space: normal; max-width: 150px;">
                                    <a href="#">
                                      {{ doc.task.description }}

                                    </a>
                                    <div class="text-secondary">
                                      {{ doc.task.comment }}
                                    </div>
                                  </td>
                                  <td>
                                    {{ taskStatus(doc.task.status) }}
                                  </td>
                                  <td>{{ dateFormat(doc.modify_dt) }}</td>
                                  <!--                                  <td>{{doc.task.task_type}}</td>-->
                                  <td class="text-end">
                                    <div class="btn-list flex-nowrap">
                                      <a href="#" class="btn btn-success btn-sm" @click="doTask(doc.task)"> 做任务 </a>
                                      <a
                                        href="#"
                                        class="btn btn-sm"
                                        data-bs-toggle="modal"
                                        data-bs-target="#reAssigneeModal"
                                        @click="reAssignee(doc.assignee)"
                                      >
                                        转给
                                      </a>
                                      <a href="#"
                                         class="btn btn-danger btn-sm"
                                         data-bs-toggle="modal"
                                         data-bs-target="#rollBackModal"
                                         @click="rollBack(doc.task)"> 打回 </a>
                                    </div>
                                  </td>
                                </tr>
                              </tbody>
                            </table>
                          </div>
                        </div>
                        <div class="card-footer d-flex align-items-center">
                          <pagination
                            @go-page="goUserTask"
                            :per-count="perCount"
                            :total-page="totalPage"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!--  <div class="card">-->
  <!--    <div class="d-flex">-->
  <!--      <div class="ms-auto text-secondary">-->
  <!--        Search:-->
  <!--        <div class="ms-2 d-inline-block">-->
  <!--          <input type="text" class="form-control form-control-sm" aria-label="Search invoice" />-->
  <!--        </div>-->
  <!--      </div>-->
  <!--      <div class="card-actions">-->
  <!--        <a href="#" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#newDocument">-->
  <!--          &lt;!&ndash; Download SVG icon from http://tabler-icons.io/i/plus &ndash;&gt;-->
  <!--          <svg-->
  <!--            xmlns="http://www.w3.org/2000/svg"-->
  <!--            class="icon"-->
  <!--            width="24"-->
  <!--            height="24"-->
  <!--            viewBox="0 0 24 24"-->
  <!--            stroke-width="2"-->
  <!--            stroke="currentColor"-->
  <!--            fill="none"-->
  <!--            stroke-linecap="round"-->
  <!--            stroke-linejoin="round"-->
  <!--          >-->
  <!--            <path stroke="none" d="M0 0h24v24H0z" fill="none" />-->
  <!--            <path d="M12 5l0 14" />-->
  <!--            <path d="M5 12l14 0" />-->
  <!--          </svg>-->
  <!--          Add new-->
  <!--        </a>-->
  <!--      </div>-->
  <!--    </div>-->

  <!--  </div>-->
</template>

<style scoped></style>
