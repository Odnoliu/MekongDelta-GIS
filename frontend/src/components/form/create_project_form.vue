<template>
  <b-modal v-model="showModal" title="Enter your new Project's information" @ok="submitForm" @cancel="closeForm"
    @hidden="closeForm">
    <b-form>
      <b-form-group label="Project's name:" label-for="name">
        <b-form-input id="name" v-model="formData.name" placeholder="Enter your Project's name"></b-form-input>
      </b-form-group>
      <b-form-group label="Project's image:" label-for="image">
        <input type="file" id="image"  accept="image/*" @change="onFileChange" require></input>
      </b-form-group>
      <b-form-group label="Description:" label-for="description">
        <b-form-input id="description" v-model="formData.description" placeholder="Enter your Project's description"></b-form-input>
      </b-form-group>
    </b-form>
  </b-modal>
</template>

<script>
import ProjectService from '../../services/project.service'
import LayerService from '../../services/layer.service';
export default {
  props: {
    showCreateForm: Boolean // Nhận giá trị từ Home.vue
  },
  data() {
    return {
      showModal: null,
      formData: {
        name: "",
        description: "",
        image: null,
      },
      defaultData: {
        name: "",
        description: "",
      }
    };
  },
  methods: {
    closeForm() {
      this.showModal = false;
      this.$emit("update:showCreateForm", false);
      this.formData = {...this.defaultData}
    },
    async submitForm() {
      const Data = new FormData();
      Data.append("name",this.formData.name)
      Data.append("image",this.formData.image)
      Data.append("description",this.formData.description)
      const response = await ProjectService.create_project(Data)
      this.$emit("created")
      const layer_response = await LayerService.create_default_layer(response.data.project_id)
      this.closeForm()
      alert('Create your new project successfully :)')
    },
    onFileChange(event) {
      this.formData.image = event.target.files[0];
    },
  },
};
</script>