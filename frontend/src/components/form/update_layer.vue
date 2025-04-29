<template>
  <b-modal v-model="showModal" title="Update Layer's information" @ok="submitForm" @cancel="closeForm"
    @hidden="closeForm">
    <b-form>
      <b-form-group label="Layer's name:" label-for="name">
        <b-form-input id="name" v-model="formData.name"></b-form-input>
      </b-form-group>
      <div v-show="activeTab == 'Vector'" id="vector">
        <div id="update-color">
          <label for="fillColor" class="form-label color-label">Fill color:</label>
          <input type="color" v-model="formData.fill" id="fillColor">
          <label for="strokeColor" class="form-label color-label">Stroke color:</label>
          <input type="color" v-model="formData.stroke" id="strokeColor">
        </div>
        <div id="update-stroke-width">
          <label for="strokeWidth">Stroke width:</label>
          <input type="range" id="strokeWidth" v-model="formData.stroke_width" min="1" max="5">
          <span>{{ formData.stroke_width }}</span>
        </div>
      </div>
      <b-form-group label="Description:" label-for="description">
        <b-form-input id="description" v-model="formData.description"></b-form-input>
      </b-form-group>
    </b-form>
  </b-modal>
</template>

<script>
import LayerService from '../../services/layer.service';
export default {
  props: ({
    layer: {
      type: Number, // Định nghĩa kiểu dữ liệu là Number
      required: true, // Bắt buộc phải truyền giá trị
    },
  }),
  data() {
    return {
      showModal: null,
      activeTab: 'Vector',
      formData: {
        name: "",
        description: "",
        fill: "#006699",
        stroke: "#001100",
        stroke_width: 2,
        layer_id: 0,
      },
      defaultData: {
        name: "",
        description: "",
        fill: "#006699",
        stroke: "#001100",
        stroke_width: 2,
        layer_id: 0,
      },
      type: "",
    };
  },
  watch: {
    layer: {
      immediate: true,
      handler(newId) {
        if (newId) {
          this.formData.layer_id = newId
          this.fetchLayerData(newId)
        }
      },
    },
  },
  methods: {
    closeForm() {
      this.showModal = false;
      this.$emit("update:showUpdate", false);
    },
    async fetchLayerData(id) {
      const response = await LayerService.get_layer_by_id(id)
      const layer = response.data.layer
      this.formData.name = layer[1]
      this.type = layer[5]
      if (layer[5] != 'L006') {
        this.formData.fill = layer[3]
        this.formData.stroke = layer[4]
        this.formData.stroke_width = layer[7]
      }
      this.formData.description = layer[9]
    },
    async submitForm() {
      const Data = new FormData();
      Data.append("name", this.formData.name)
      Data.append("layer_id", this.formData.layer_id)
      Data.append("des", this.formData.description)
      if (this.type != 'L006') {
        Data.append("fill", this.formData.fill)
        Data.append("stroke", this.formData.stroke)
        Data.append("stroke_width", this.formData.stroke_width)
        const response = await LayerService.update_vector_layer(Data)
      }
      else {
        const response = await LayerService.update_tile_layer(Data)
      }
      this.$emit("updated")
      this.closeForm()
      alert('Update your layer successfully :)')
    },
  },
};
</script>
<style>
#vector {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
#update-color{
  width: 100%;
  display: flex;
  justify-content:center;
  gap: 20px;
  margin-top: 10px;
  margin-bottom: 10px;
}
#update-stroke-width{
  display: flex;
  justify-content: center;
  gap: 10px;
}
</style>