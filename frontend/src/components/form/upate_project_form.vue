<template>
  <b-modal v-model="showModal" title="Update Project's information" @ok="submitForm" @cancel="closeForm"
    @hidden="closeForm">
    <b-form>
      <b-form-group label="Project's name:" label-for="name">
        <b-form-input id="name" v-model="formData.name"></b-form-input>
      </b-form-group>
      <b-form-group label="Project's image:" label-for="image">
        <input type="file" id="image" accept="image/*" @change="onFileChange" require></input>
      </b-form-group>
      <b-form-group label="Description:" label-for="description">
        <b-form-input id="description" v-model="formData.description"></b-form-input>
      </b-form-group>
    </b-form>
  </b-modal>
</template>

<script>
import ProjectService from '../../services/project.service'
export default {
  props: ({
    project: {
    type: Number, // Định nghĩa kiểu dữ liệu là Number
    required: true, // Bắt buộc phải truyền giá trị
  },
  }),
  data() {
    return {
      showModal: null,
      formData: {
        name: "",
        description: "",
        image: "",
      },
      defaultData: {
        name: "",
        description: "",
        image: "",
      }
    };
  },
  watch: {
    project: {
      immediate: true,
      handler(newId) {
        if (newId) {
          this.fetchProjectData(newId);
        }
      },
    },
  },
  methods: {
    closeForm() {
      this.showModal = false;
      this.$emit("update:showUpdate", false);
    },
    async fetchProjectData(id) {
      const response = await ProjectService.get_project_by_id(id)
      this.formData.name = response.data.data[0].project_name
      this.formData.description = response.data.data[0].project_description
    },
    async submitForm() {
      const Data = new FormData();
      Data.append("name", this.formData.name)
      Data.append("image", this.formData.image)
      Data.append("description", this.formData.description)
      Data.append("id",this.project)
      const response = await ProjectService.update_project(Data)
      this.$emit("updated")
      this.closeForm()
      alert('Update your project successfully :)')
    },
    onFileChange(event) {
      this.formData.image = event.target.files[0];
    },
  },
};
</script>