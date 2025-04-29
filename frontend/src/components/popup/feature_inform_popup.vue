<template>
    <div :id="popupId" class="ol-popup">
        <div class="popup-content">
            <h5>FEATURE INFORMATION</h5>
            <div>
                <div v-for="(item, index) in feature_array" :key="index">
                    <p v-for="(value, key) in item" :key="key">
                        <strong>{{ key }}:</strong> {{ value }}
                    </p>
                </div>
                <div v-if="user_feature_data.length > 0" v-for="(feature, index) in user_feature_data" :key="index">
                    <p v-if="editingIndex !== index">
                        <strong>{{ feature[5] }}:</strong> {{ feature[6] }}
                        <span class="badge bg-primary ms-2 me-2" @click="startEdit(index, feature)"><i
                                class="fa-solid fa-pen"></i></span>
                        <span class="badge bg-danger" @click="delete_inform(feature[0])"><i
                                class="fa-solid fa-trash"></i></span>
                    </p>
                    <div v-else class="row">
                        <div class="col-3" style="padding: 5px">
                            <input type="text" class="form-control" placeholder="Title" v-model="editForm.title" />
                        </div>
                        <div class="col-6" style="padding: 5px">
                            <input type="text" class="form-control" placeholder="Content" v-model="editForm.content" />
                        </div>
                        <div class="col-3 d-flex justify-content-center align-items-center" style="padding: 5px">
                            <span class="badge bg-success me-2 fs-6" @click="update_inform(feature[0])">
                                <i class="fa-solid fa-check"></i>
                            </span>
                            <span class="badge bg-danger fs-6" @click="cancelEdit">
                                <i class="fa-solid fa-times "></i>
                            </span>
                        </div>
                    </div>
                </div>
                <div id="more-feature-inform">
                    <div v-for="(item, index) in inputs" :key="index" class="container mt-4">
                        <div class="row">
                            <div class="col-3" style="padding: 5px">
                                <input type="text" class="form-control" placeholder="Title" v-model="item.title" />
                            </div>
                            <div class="col-7" style="padding: 5px">
                                <input type="text" class="form-control" placeholder="Content" v-model="item.content" />
                            </div>
                            <div class="col-2" style="padding: 5px">
                                <button class="btn btn-primary btn-sm" @click="add_inform(index)">
                                    <i class="fa-solid fa-floppy-disk"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="button-group">
            <button class="btn btn-success btn-sm" @click="handleAdd"><i class="fa-solid fa-plus"></i></button>
            <button class="btn btn-secondary btn-sm" @click="handleCancel"><i class="fa-solid fa-xmark"></i></button>
        </div>
    </div>
</template>
<script>
import { toLonLat } from 'ol/proj';
import Overlay from 'ol/Overlay';
import LayerService from '../../services/layer.service';
import FeatureService from '../../services/feature.service';
import Inform_FeatureService from '../../services/inform_feature.service';
export default {
    name: 'DrawingPopup',
    props: {
        map: {
            type: Object,
        },
        Nonedrawing: {
            type: Boolean,
        },
        coor: {
            type: Array,
        },
        feature_data: {
            type: Object,
        },
    },
    data() {
        return {
            popupId: `feature-inform-popup-${Math.random().toString(36).substr(2, 9)}`,
            coordinates: '',
            overlay: null,
            NoneDrawing: false,
            startCoordinates: null, // Lưu tọa độ điểm đầu tiên
            feature_array: [],
            inputs: [],
            user_feature_data: [],
            editingIndex: null, // Chỉ số feature đang chỉnh sửa
            editForm: {
                title: '',
                content: ''
            } // Dữ liệu tạm thời cho chỉnh sửa
        };
    },
    watch: {
        Nonedrawing: {
            handler(newVal) {
                if (newVal) {
                    this.NoneDrawing = newVal;
                    this.initializePopup();
                } else {
                    this.hidePopup();
                }
            },
            immediate: true,
        },
        coor: {
            handler(newCoords) {
                if (newCoords && this.NoneDrawing) {
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
            console.log(this.feature_data)
            if (this.feature_data.layer_name == 'VN') {
                const get_default_feature_by_id_response = await FeatureService.get_default_feature_by_id(this.feature_data)
                this.feature_array = [get_default_feature_by_id_response.data.features.properties]
            }
            else if (this.feature_data.layer_name == 'MD_State' || this.feature_data.layer_name == 'MD_District') {
                const get_default_feature_by_id_response = await FeatureService.get_default_feature_by_id(this.feature_data)
                this.feature_array = [get_default_feature_by_id_response.data.features]
                console.log(this.feature_array)
            }
            else {
                const get_feature_by_id_response = await FeatureService.get_feature_by_id(this.feature_data)
                this.feature_array = get_feature_by_id_response.data.properties
                console.log(this.feature_array)
            }
            this.fetch_feature_inform()
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
            this.NoneDrawing = false;
            this.coordinates = '';
            this.startCoordinates = null;
        },
        startEdit(index, feature) {
            // Bắt đầu chỉnh sửa
            this.editingIndex = index;
            this.editForm = {
                title: feature[5],
                content: feature[6]
            };
        },
        cancelEdit() {
            // Hủy chỉnh sửa
            this.editingIndex = null;
            this.editForm = { title: '', content: '' };
        },
        handleAdd() {
            this.inputs.push({
                title: '',
                content: ''
            });
            document.getElementById('more-feature-inform').style.display = 'block';
            // const Feature_Inform_Status = false;
            // this.$emit('status', Feature_Inform_Status);
            // this.hidePopup();
        },
        handleCancel() {
            const Feature_Inform_Status = false;
            this.$emit('status', Feature_Inform_Status);
            this.hidePopup();
        },
        async fetch_feature_inform() {
            const Data = {
                "feature_id": this.feature_data.feature_id,
                "layer_name": this.feature_data.layer_name,
            }
            const fetch_feature_inform_response = await Inform_FeatureService.get_feature_inform_by_id(Data)
            console.log(fetch_feature_inform_response)
            if (fetch_feature_inform_response.status == '200') {
                if (fetch_feature_inform_response.data.feature_inform != null) {
                    this.user_feature_data = fetch_feature_inform_response.data.feature_inform
                    console.log(this.user_feature_data)
                }
            }
        },
        async add_inform(index) {
            const Data = {
                "feature_id": this.feature_data.feature_id,
                "layer_name": this.feature_data.layer_name,
                "title": this.inputs[index].title,
                "content": this.inputs[index].content
            }
            const add_feature_inform_response = await Inform_FeatureService.create_feature_inform(Data)
            console.log(add_feature_inform_response)
            this.fetch_feature_inform()
            this.inputs[index].title = ''
            this.inputs[index].content = ''
        },
        async update_inform(index) {
            if (!this.editForm.title || !this.editForm.content) {
                alert('Vui lòng nhập đầy đủ tiêu đề và nội dung!');
                return;
            }
            const Data = {
                "id": index,
                "title": this.editForm.title,
                "content": this.editForm.content
            }
            const update_feature_inform_repsonse = await Inform_FeatureService.update_feature_inform(Data)
            console.log(update_feature_inform_repsonse)
            this.editingIndex = null;
            this.fetch_feature_inform()
        },
        async delete_inform(id) {
            const Data = {
                "id": id,
            }
            const delete_feature_inform_response = await Inform_FeatureService.delete_feature_inform(Data)
            console.log(delete_feature_inform_response)
            this.fetch_feature_inform()
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
    width: 350px;
    display: none;
    font-size: 15px;
}

.button-group {
    margin-top: 10px;
    display: flex;
    justify-content: center;
    gap: 10px;
}

p {
    margin-bottom: 3px;
}

#more-feature-inform {
    display: none;
}
</style>