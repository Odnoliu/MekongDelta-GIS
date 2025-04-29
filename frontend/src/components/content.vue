<template>
  <div>
    <b-button variant="info" data-bs-toggle="tooltip" title="Create new layer" class="create-layer-button" @click="showCreateForm = true; showUpdateForm = false;">
      <i class="fa-solid fa-plus"></i>
    </b-button>
    <Create_Form v-model="showCreateForm" @update:showCreateForm="updateShowCreate" @created="fetchAllProject"></Create_Form>
    <Update_Form v-model="showUpdateForm" :project="Number(updateProjectID)" @close="updateProjectID = null" @update:showUpdate="updateShowUpdate" @updated="fetchAllProject"></Update_Form>
    <div class="container mt-4">
    <div class="row">
      <div v-for="project in project_list" :key="project.project_id" class="col-md-3 mb-4x" style="height: 400px;">
        <div class="card shadow-sm">
          <img :src="project.project_image" class="card-img-top" alt="Project Image">
          <div class="card-body">
            <p class="card-title" style="margin: 0; color: brown; font-weight: bold;">{{ project.project_name }}</p>
            <p class="card-text">{{ project.project_description }}</p>
            <div class="d-flex justify-content-end gap-2 route-btn">
              <BButton variant="success" @click="fetchProject(project.project_id)"><i class="fa-solid fa-map"></i></BButton>
              <BButton variant="primary" @click="updateProject(project.project_id)"><i class="fa-solid fa-pen"></i></BButton>
              <BButton variant="danger" @click="deleteProject(project.project_id)"><i class="fa-solid fa-trash"></i></BButton>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
  
</template>
<script>
import { useRouter } from "vue-router"

import Create_Form from '../components/form/create_project_form.vue'
import Update_Form from '../components/form/upate_project_form.vue'
import ProjectService from '../services/project.service'
export default {
  setup(){
    const router = useRouter()
    const fetchProject = (project_id) => {
      router.push(`/map/${project_id}`)
    };

    return{
      fetchProject
    };
  },
  name: 'Content',
  components: {
    Create_Form,
    Update_Form,
  },
  data() {
    return {
      showTooltip: false,
      showCreateForm: false,
      showUpdateForm: false,
      updateProjectID: null,
      fetchProjectID: null,
      project_list: [],
    }
  },
  watch: {
    show(val) {
      this.showCreateForm = val; // Cập nhật showModal khi show thay đổ
    },
  },
  methods: {
    async fetchAllProject() {
      const response = await ProjectService.get_all_project();
      if (response.status == 200) {
        this.project_list = response.data.data
      }
    },
    updateShowCreate(value) {
      this.showCreateForm = value;
    },
    updateShowUpdate(value) {
      this.showUpdateForm = value;
    },
    async updateProject(project_id){
      this.showCreateForm = false;
      this.showUpdateForm = true;
      this.updateProjectID = project_id
    },
    async deleteProject(project_id){
      const id = Number(project_id)
      const response = await ProjectService.delete_project(id)
      this.fetchAllProject()
    }
  },
  mounted() {
    this.fetchAllProject();
  }
}
</script>

<style scoped>
.card {
  margin-bottom: 20px;
  height: 95%;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card img{
  height: 60%;
}
.card-body{
  height: 35%;
}
.create-layer-button{
  position: fixed;
  bottom: 20px;
  right: -80px;
  width: 100px;
  height: 50px;
  transition: transform 0.5s ease-in-out, background-color 1s ease;
  background-color: rgb(14, 194, 194);
}

.create-layer-button:hover{
  transform: translateX(-70px);
}
.create-layer-button i{
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
}
.create-layer-button:hover i{
  opacity: 1;
}
.container{
  padding: 12px 12px 12px 12px;
}
.card:hover{
  transform: translateY(-6px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}
.card-title, .card-text{
  height: 30%;
}

.route-btn{
  height: 35%;
}
</style>