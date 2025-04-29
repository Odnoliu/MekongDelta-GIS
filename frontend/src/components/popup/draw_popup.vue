<template>
  <div :id="popupId" class="ol-popup">
    <div class="popup-content">
      <h5>SELECT YOUR LAYER!</h5>
      <div>
        <select v-model="selectedLayer">
          <option v-for="(layer, index) in listLayer" :key="index" :value="layer[1]">
            {{ layer[1] }}
          </option>
        </select>
        <p v-if="selectedLayer">Selected layer: {{ selectedLayer }}</p>
      </div>
    </div>
    <div class="button-group">
      <button class="btn btn-primary btn-sm" @click="handleOk">OK</button>
      <button class="btn btn-secondary btn-sm" @click="handleCancel">Cancel</button>
    </div>
  </div>
</template>

<script>
import { toLonLat } from 'ol/proj';
import Overlay from 'ol/Overlay';
import LayerService from '../../services/layer.service';
export default {
  name: 'DrawingPopup',
  props: {
    map: {
      type: Object,
    },
    drawing: {
      type: Boolean,
    },
    coor: {
      type: Array,
    },
    project_id: {
      type: Number,
    }
  },
  data() {
    return {
      popupId: `drawing-popup-${Math.random().toString(36).substr(2, 9)}`,
      coordinates: '',
      overlay: null,
      isDrawing: false,
      startCoordinates: null, // Lưu tọa độ điểm đầu tiên
      listLayer: null,
      selectedLayer: null,
    };
  },
  watch: {
    drawing: {
      handler(newVal) {
        if (newVal) {
          this.isDrawing = newVal;
          this.initializePopup();
        } else {
          this.hidePopup();
        }
      },
      immediate: true,
    },
    coor: {
      handler(newCoords) {
        if (newCoords && this.isDrawing) {
          const lonLat = toLonLat(newCoords);
          this.coordinates = `[${lonLat[0].toFixed(4)}, ${lonLat[1].toFixed(4)}]`;
          this.overlay.setPosition(newCoords); // Hiển thị popup tại tọa độ click
          document.getElementById(this.popupId).style.display = 'block'
        }
      },
      immediate: true,
    },
  },
  methods: {
    async initializePopup() {
      if (!this.map) return;
      const get_layer_response = await LayerService.get_all_layer(this.project_id)
      if (get_layer_response.status == '200') {
        this.listLayer = get_layer_response.data.layers
        console.log(this.listLayer)
      }
      // Tạo overlay cho popup
      const popupElement = document.getElementById(this.popupId);
      this.overlay = new Overlay({
        element: popupElement,
        autoPan: true,
        autoPanAnimation: { duration: 250 },
      });
      this.map.addOverlay(this.overlay);
    },
    hidePopup() {
      if (this.overlay) {
        this.overlay.setPosition(undefined);
      }
      this.isDrawing = false;
      this.coordinates = '';
      this.startCoordinates = null;
    },
    handleOk() {
      this.isDrawing = false;
      const drawStatus = false;
      const layer = this.selectedLayer
      console.log("Layer được chọn:", layer)
      this.$emit('layer-selected', { layer, drawStatus });
      this.hidePopup();
    },
    handleCancel() {
      this.isDrawing = false;
      const drawStatus = false;
      this.$emit('layer-selected', { drawStatus });
      this.hidePopup();
    },
  },
  beforeUnmount() {
    if (this.overlay && this.map) {
      this.map.removeOverlay(this.overlay);
    }
  },

};
</script>

<style scoped>
.ol-popup {
  position: absolute;
  background-color: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  padding: 15px;
  border-radius: 10px;
  border: 1px solid #cccccc;
  bottom: 12px;
  left: -50px;
  min-width: 200px;
  display: none;
}

.button-group {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}

select {
  padding: 5px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

</style>