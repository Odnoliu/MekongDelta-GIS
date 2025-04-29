<template>
    <div v-if="!isLoading" class="container-web">
        <div class="map">
            <!-- Header chứa nút Quay lại -->
            <div class="header">
                <button class="btn btn-primary" @click="backHome">Back</button>
            </div>

            <!-- Vùng hiển thị bản đồ -->
            <div ref="mapContainer" class="map-container"></div>

            <!-- Nút chọn mức độ dâng của mực nước biển -->
            <div class="custom-select-wrapper">
                <div class="custom-select form-control" @click="toggleDropdown">
                    <span class="selected-option">{{ selectedStyleText }}</span>
                    <span class="arrow no-before"><i class="fa-solid fa-caret-up"></i></span>
                </div>
                <ul v-if="isDropdownOpen" class="options-list dropdown-menu show">
                    <li v-for="style in styles" :key="style.value"
                        @click="selectStyle(style.value, style.text, style.level)" class="dropdown-item"
                        :class="{ active: style.value == selectedStyle }">
                        {{ style.text }}
                    </li>
                </ul>
            </div>
            <!-- Nút chọn layer Viet Nam -->
            <div class="vn_baselayer-buttons btn-group">
                <button v-for="(layer, key) in Object.values(vnbaseLayers)" :key="key"
                    @click="changeVN_BaseLayer(layer.name)" class="btn"
                    :class="{ 'btn-dark': activeVNLayer == layer.name, 'btn-outline-dark': activeVNLayer !== layer.name }">
                    {{ layer.label }}
                </button>
            </div>

            <!-- Nút chọn layer MD -->
            <div class="vectorlayer-buttons btn-group">
                <button v-for="(layer, key) in Object.values(vectorLayers)" :key="key"
                    @click="changeVectorLayer(layer.name)" class="btn"
                    :class="{ 'btn-dark': activevectorLayer == layer.name, 'btn-outline-dark': activevectorLayer !== layer.name }">
                    {{ layer.label }}
                </button>
            </div>

            <!-- Nút chọn layer nền -->
            <div class="baselayer-buttons btn-group">
                <button v-for="(layer, key) in baseLayers" :key="key" @click="changeBaseLayer(key)" class="btn"
                    :class="{ 'btn-dark': selectedLayer == key, 'btn-outline-dark': selectedLayer !== key }">
                    {{ layer.label }}
                </button>
            </div>

            <!-- Thẻ chứa 3 button chồng lên nhau, nằm góc trên bên phải -->
            <div class="position-absolute d-flex flex-column" style="top: 50px; right: 520px;">
                <button class="btn btn-secondary mb-1 draw-tool" :class="{ 'btn-primary': drawType === 'Point' }"
                    data-bs-toggle="tooltip" title="Point" @click="setDrawType('Point')">
                    <i class="fa-solid fa-map-pin"></i>
                </button>
                <button class="btn btn-secondary mb-1 draw-tool" :class="{ 'btn-primary': drawType === 'LineString' }"
                    data-bs-toggle="tooltip" title="Line" @click="setDrawType('LineString')">
                    <i class="fa-solid fa-grip-lines"></i>
                </button>
                <button class="btn btn-secondary mb-1 draw-tool" :class="{ 'btn-primary': drawType === 'Polygon' }"
                    data-bs-toggle="tooltip" title="Polygon" @click="setDrawType('Polygon')">
                    <i class="fa-solid fa-draw-polygon"></i>
                </button>
                <button class="btn btn-secondary mb-1 draw-tool" :class="{ 'btn-primary': drawType === 'None' }"
                    data-bs-toggle="tooltip" title="Off" @click="setDrawType('None')">
                    <i class="fa-solid fa-ban"></i>
                </button>
            </div>
            <Draw_Popup v-if="mapInstance" :map="mapInstance" :project_id="Number(project_id)" :drawing="isDrawing"
                :coor="drawclickCoordinates" @layer-selected="handleSelectedLayer"></Draw_Popup>
            <Feature_Inform_Popup v-if="mapInstance" :map="mapInstance" :Nonedrawing="noneDrawing"
                :coor="clickCoordinates" :feature_data="Feature_Data" @status="updateStatusFeatureInformPopup">
            </Feature_Inform_Popup>
        </div>
        <div class="menu">
            <div class="menu-header">
                <h5 class="mb-0">Control</h5>
            </div>
            <div class="menu-content">
                <div v-show="activeMenu == 'FloodAndTemp'" id="FloodAndTemp" class="menucontent">
                    <div class="floodcontent">
                        <div v-if="noDataMessage" class="floodcontent">
                            <h5>{{ noDataMessage }}</h5>
                        </div>

                        <!-- Bảng hiển thị dữ liệu ngập lụt -->
                        <div v-else class="table-container">
                            <table class="table table-striped table-bordered table-sm">
                                <thead>
                                    <tr>
                                        <th scope="col">City</th>
                                        <th scope="col">District / Town</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(item, index) in uniqueRows" :key="index">
                                        <td>{{ item.State }}</td>
                                        <td>{{ item.Type }} {{ item.Name }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <div v-show="activeMenu == 'Layers'" id="Layers" class="menucontent">
                    <table class="table table-striped table-bordered table-hover layer-table">
                        <thead class="table-dark">
                            <tr>
                                <th scope="col" class="text-center">Name</th>
                                <th scope="col" class="text-center">Type</th>
                                <th scope="col" class="text-center">Priority</th>
                                <th scope="col" class="text-center">Control</th>
                            </tr>
                        </thead>
                        <draggable v-model="list_layer" tag="tbody" item-key="id" @end="updatePriorities">
                            <template #item="{ element: row, index }">
                                <tr :key="row[0]">
                                    <td class="text-center align-middle fs-6">{{ row[1] }}</td>
                                    <td class="text-center align-middle fs-6">{{ typeLayer(row[5]) }}</td>
                                    <td class="text-center align-middle fs-6">{{ row[10] }}</td>
                                    <td>
                                        <label class="switch">
                                            <input type="checkbox" class="checkbox"
                                                @click="controlLayer(row[0], $event)" />
                                            <span></span>
                                        </label>
                                        <div class="d-flex justify-content-center gap-2">
                                            <button class="btn btn-primary" id="update-layer"
                                                @click="updateLayer(row[0])">
                                                <i class="fa-solid fa-pen"></i>
                                            </button>
                                            <button class="btn btn-danger" id="delete-layer"
                                                @click="deleteLayer(row[0])">
                                                <i class="fa-solid fa-trash"></i>
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            </template>
                            <template #footer>
                                <tr v-if="list_layer.length == 0">
                                    <td colspan="4" class="text-center">No data available</td>
                                </tr>
                            </template>
                        </draggable>
                    </table>
                    <a href="#" style="font-style: italic; font-size: 20px;" @click="showDetailModal = true">Details</a>
                    <b-button class="create_layer_btn" data-bs-toggle="tooltip" title="Create new Layer"
                        @click="showCreateForm = true">
                        <i class="fa-solid fa-plus"></i>
                    </b-button>
                </div>
                <div v-show="activeMenu == 'Features'" id="Features" class="menucontent">
                    <div class="mb-3">
                        <label for="layerFilter" class="form-label">Filter by Layer's name:</label>
                        <select id="layerFilter" v-model="selectedLayerName" class="form-select"
                            @change="filterFeatures">
                            <option value="All">All</option>
                            <option v-for="(layer, index) in listLayer" :key="index" :value="layer[1]">
                                {{ layer[1] }}
                            </option>
                        </select>
                    </div>
                    <table class="table table-striped table-bordered table-hover layer-table">
                        <thead class="table-dark">
                            <tr>
                                <th scope="col" class="text-center">Name</th>
                                <th scope="col" class="text-center">Type</th>
                                <th scope="col" class="text-center">Belongs to Layer</th>
                                <th scope="col" class="text-center">Control</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(pair, index) in filteredFeatureLayerPairs" :key="index">
                                <td class="text-center align-middle fs-6">{{ pair[0].properties.name }}</td>
                                <td class="text-center align-middle fs-6">{{ pair[0].geometry.type }}</td>
                                <td class="text-center align-middle fs-6">{{ pair[1] }}</td>
                                <td class="text-center align-middle fs-6">
                                    <button class="btn btn-danger" id="delete-feature"
                                        @click="deleteFeature(pair[0].properties.id, index)">
                                        <i class="fa-solid fa-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="menu-footer">
                <button class="btn btn-primary" :class="{ active: activeMenu == 'FloodAndTemp' }"
                    @click="openMenu('FloodAndTemp')">Flood Area</button>
                <button class="btn btn-primary" :class="{ active: activeMenu == 'Layers' }"
                    @click="openMenu('Layers')">Layers</button>
                <button class="btn btn-primary" :class="{ active: activeMenu == 'Features' }"
                    @click="openMenu('Features')">Features</button>
            </div>
        </div>
        <Create_Layer v-model="showCreateForm" :project_id="project_id" @update:showCreateForm="updateShowCreate">
        </Create_Layer>
        <Update_Layer v-model="showUpdateForm" :layer="Number(updateLayerID)" @close="updateLayerID = null"
            @update:showUpdate="updateShowUpdate" @updated="fetchAllLayer">
        </Update_Layer>
        <Layer_Detail_Modal v-model="showDetailModal" :project_id="project_id" @update:showModal="updateShowModal">
        </Layer_Detail_Modal>
    </div>
    <div v-else>Loading...</div>
</template>

<script>
import { ref, onMounted, computed, watch } from "vue";
import Draggable from "vuedraggable";
import Map from "ol/Map";
import View from "ol/View";
import { fromLonLat } from "ol/proj";
import TileLayer from "ol/layer/Tile";
import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";
import OSM from "ol/source/OSM";
import XYZ from "ol/source/XYZ";
import GeoJSON from "ol/format/GeoJSON";
import { Stroke, Style, Fill } from "ol/style";
import { useRoute, useRouter } from "vue-router";
import FeatureService from "../../services/feature.service";
import LayerService from "../../services/layer.service";
import { TileWMS } from 'ol/source';
import Flood_And_TempService from "../../services/flood_and_temp.service";
import LayerTypeService from "../../services/layer_type.service";
import FloodChart from "../../components/flood_chart.vue";
import Create_Layer from "../../components/form/create_layer.vue";
import Layer_Detail_Modal from "../../components/modal/layer_detail_modal.vue";
import Draw from 'ol/interaction/Draw';
import Update_Layer from "../../components/form/update_layer.vue";
import Draw_Popup from "../../components/popup/draw_popup.vue";
import Circle from 'ol/style/Circle';
import Feature_Inform_Popup from "../../components/popup/feature_inform_popup.vue";
import Inform_Feature_Service from "../../services/inform_feature.service";

export default {
    props: {
        show: Boolean, // Giả định prop show từ watch
    },
    name: 'MapComponent',
    components: {
        Create_Layer,
        Update_Layer,
        FloodChart,
        Layer_Detail_Modal,
        Draggable,
        Draw_Popup,
        Feature_Inform_Popup,
    },

    setup(props) {
        const route = useRoute()
        const project_id = ref(route.params.id)
        const maxPriority = ref(1);
        const mapContainer = ref(null);
        let mapInstance = ref(null);
        let selectedLayer = ref("osm");
        let Default_vectorLayers = ref([]);
        let vectorLayers = ref({});
        let activevectorLayer = ref("md_state");
        let activeVNLayer = ref("vn");
        let vnbaseLayers = ref({});
        let updateLayerID = ref(0);
        const selectedStyle = ref(''); // Mặc định là "None"
        const isDropdownOpen = ref(false);
        const menuContent = ref(null);
        const selectedChartType = ref('bar');
        const showChartModal = ref(true);
        const currentFloodLV = ref(0);
        const showCreateForm = ref(false);
        const showUpdateForm = ref(false);
        const showDetailModal = ref(false);
        const activeMenu = ref('FloodAndTemp');
        const list_layer = ref([]);
        const featureLayerPairs = ref([]);
        const isLoaded = ref(false);
        const isLoading = ref(false);
        let saveFeature = ref(false);
        const drawType = ref('None');
        const listLayer = ref([]);
        const listFeature = ref(null);
        const floodData = ref([]);
        const noDataMessage = ref('');
        let drawInteraction = null;
        let clickCoordinates = ref(null);
        let drawclickCoordinates = ref(null);
        let filteredFeatureLayerPairs = ref([]);
        let selectedLayerName = ref('All');
        const DrawvectorSource = new VectorSource();
        const DrawvectorLayer = new VectorLayer({
            source: DrawvectorSource,
        });
        const isDrawing = ref(false);
        const noneDrawing = ref(false);
        const Feature_Data = ref(null);
        const drawStatus = ref(false);
        watch(
            () => props.show,
            async (val) => {
                showCreateForm.value = val; // Gán giá trị mới cho showCreateForm
                if (val) {
                    try {
                        // 1. Gọi API get_all_layer
                        const initLayer_response = await LayerService.get_all_layer(project_id.value);

                        // 2. Đợi initLayer và initLayerTable hoàn thành
                        await Promise.all([
                            initLayer(initLayer_response),
                            initLayerTable(initLayer_response),
                        ]);

                        // 3. Cập nhật isLoaded sau khi tất cả hoàn thành
                        isLoaded.value = true;
                        console.log('All initialization completed, isLoaded:', isLoaded.value);
                    } catch (error) {
                        console.error('Lỗi trong quá trình khởi tạo:', error);
                        isLoaded.value = false; // Đặt lại isLoaded nếu có lỗi
                    }
                }
            }
        );
        watch(featureLayerPairs, () => {
            filterFeatures();
        }, { deep: true });

        const router = useRouter();
        // Chuyển các hàm từ methods sang setup()
        const updateShowCreate = async (value) => {
            showCreateForm.value = value;
            try {
                // 1. Gọi API get_all_layer
                const initLayer_response = await LayerService.get_all_layer(project_id.value);

                // 2. Đợi initLayer và initLayerTable hoàn thành
                await Promise.all([
                    initLayer(initLayer_response),
                    initLayerTable(initLayer_response),
                ]);

                // 3. Cập nhật isLoaded sau khi tất cả hoàn thành
                isLoaded.value = true;
                console.log('All initialization completed, isLoaded:', isLoaded.value);
            } catch (error) {
                console.error('Lỗi trong quá trình khởi tạo:', error);
                isLoaded.value = false; // Đặt lại isLoaded nếu có lỗi
            }
            const get_max_ZIndex_response = await LayerService.get_max_z_index(project_id.value)
            maxPriority.value = parseInt(get_max_ZIndex_response.data.z_index)
        };
        const updateShowUpdate = async (value) => {
            showUpdateForm.value = value;
        }
        const fetchAllLayer = async () => {
            try {
                // 1. Gọi API get_all_layer
                const initLayer_response = await LayerService.get_all_layer(project_id.value);

                // 2. Đợi initLayer và initLayerTable hoàn thành
                await Promise.all([
                    initLayer(initLayer_response),
                    initLayerTable(initLayer_response),
                ]);

                // 3. Cập nhật isLoaded sau khi tất cả hoàn thành
                isLoaded.value = true;
                console.log('All initialization completed, isLoaded:', isLoaded.value);
            } catch (error) {
                console.error('Lỗi trong quá trình khởi tạo:', error);
                isLoaded.value = false; // Đặt lại isLoaded nếu có lỗi
            }
            const get_max_ZIndex_response = await LayerService.get_max_z_index(project_id.value)
            maxPriority.value = parseInt(get_max_ZIndex_response.data.z_index)
        }
        const updateLayer = (layer_id) => {
            showCreateForm.value = false;
            showUpdateForm.value = true;
            updateLayerID.value = layer_id;
        }
        const updatePriorities = async () => {
            const updatePromises = list_layer.value.map(async (row, index) => {
                const newPriority = maxPriority.value - index;

                // Cập nhật Priority trên giao diện
                row[10] = newPriority;
                // Gọi API để cập nhật Priority trên server
                await update_priority_layer(row);
            });

            // Chờ tất cả các API call hoàn tất
            await Promise.all(updatePromises);
            const layers = mapInstance.value.getLayers().getArray();
            const layersToRemove = layers.filter((layer) => {
                const zIndex = layer.getZIndex() || 0; // Mặc định zIndex là 0 nếu không có
                return zIndex > 3;
            });

            layersToRemove.forEach((layer) => {
                mapInstance.value.removeLayer(layer);
                console.log(`Removed layer with zIndex: ${layer.getZIndex()}`);
            });
            try {
                // 1. Gọi API get_all_layer
                const initLayer_response = await LayerService.get_all_layer(project_id.value);

                // 2. Đợi initLayer và initLayerTable hoàn thành
                await Promise.all([
                    initLayer(initLayer_response),
                ]);

                // 3. Cập nhật isLoaded sau khi tất cả hoàn thành
                isLoaded.value = true;
                console.log('All initialization completed, isLoaded:', isLoaded.value);
            } catch (error) {
                console.error('Lỗi trong quá trình khởi tạo:', error);
                isLoaded.value = false; // Đặt lại isLoaded nếu có lỗi
            }

        };
        const updateShowModal = (value) => {
            showDetailModal.value = value;
        };
        const backHome = () => {
            router.push('/home');
        };
        // Hàm mở/đóng dropdown
        const toggleDropdown = () => {
            isDropdownOpen.value = !isDropdownOpen.value;
        };

        // Hàm thay đổi lớp nền
        const changeBaseLayer = (layerName) => {
            selectedLayer.value = layerName;
            console.log(baseLayers);
            Object.keys(baseLayers).forEach((key) => {
                console.log(key);
                if (key === 'none') return; // Thay return bằng continue
                baseLayers[key].layer.setVisible(key == layerName);
            });
        };

        const changeVN_BaseLayer = (layerName) => {
            activeVNLayer.value = layerName;
            Object.keys(vnbaseLayers.value).forEach((key) => {
                if (key == 'none') return;
                vnbaseLayers.value[key].layer.setVisible(key == layerName);
            });
        };
        // Hàm thay đổi lớp VectorLayer
        const changeVectorLayer = (layerName) => {
            console.log(layerName)
            activevectorLayer.value = layerName;
            Object.keys(vectorLayers.value).forEach((key) => {
                if (key == 'none') return;
                console.log(vectorLayers.value[key])
                vectorLayers.value[key].layer.setVisible(key == layerName);
            });
        };
        // Hàm chọn style
        const selectStyle = (value, text, level) => {
            selectedStyle.value = value;
            isDropdownOpen.value = false;
            // Cập nhật style cho Tile Layer
            const tileLayers = mapInstance.value.getLayers().getArray().filter((layer) => layer instanceof TileLayer);
            tileLayers.forEach((layer) => {
                if (layer.get("label") == "GeoTIFF") {
                    if (value == '') {
                        layer.setVisible(false);
                    } else {
                        layer.setVisible(true);
                        layer.setZIndex(4);
                        const source = layer.getSource();
                        source.updateParams({ 'STYLES': value });
                        source.refresh(); // Làm mới layer để áp dụng style mới
                    }
                }
            });
            showFloodInform(level);
        };
        const uniqueRows = computed(() => {
            const seen = new Set();
            return floodData.value.filter(item => {
                const rowKey = `${item.State}|${item.Type}|${item.Name}`;
                if (!seen.has(rowKey)) {
                    seen.add(rowKey);
                    return true;
                }
                return false;
            });
        });
        const showFloodInform = async (FloodLV) => {
            if (FloodLV === '0') {
                noDataMessage.value = 'No data about flood area in Mekong Delta';
                floodData.value = [];
                return;
            }

            try {
                const response = await Flood_And_TempService.get_flood_inform();
                const floodDataRaw = response.data.floodata;
                const filteredData = floodDataRaw.filter(item => item.Elve_mean <= Number(FloodLV));

                if (filteredData.length === 0) {
                    noDataMessage.value = 'Không có vùng nào có mức ngập lụt.';
                    floodData.value = [];
                    return;
                }

                // Cập nhật dữ liệu
                noDataMessage.value = '';
                floodData.value = filteredData;
                currentFloodLV.value = Number(FloodLV);
            } catch (error) {
                console.error('Error fetching flood data:', error);
                noDataMessage.value = 'Lỗi khi lấy dữ liệu ngập lụt.';
                floodData.value = [];
            }
        };

        // Hàm thiết lập loại hình vẽ
        const setDrawType = async (type) => {
            drawStatus.value = true
            drawType.value = type;
            noneDrawing.value = false
            if (type != 'None') {
                if (!saveFeature.value) {
                    noneDrawing.value = false
                    isDrawing.value = true
                    saveFeature.value = true
                }
                updateDrawInteraction();
            }
            else {
                drawStatus.value = false;
                saveFeature.value = false;
                updateDrawInteraction();
                const drawFeatures = DrawvectorSource.getFeatures()
                const geojsonFormat = new GeoJSON();
                const featuresGeoJSON = drawFeatures.map((feature, index) => {
                    const geojson = geojsonFormat.writeFeatureObject(feature, {
                        featureProjection: 'EPSG:3857', // Hệ tọa độ của bản đồ
                        dataProjection: 'EPSG:4326', // Hệ tọa độ mong muốn (WGS84)
                    });

                    return {
                        name: `Draw-Feature ${index + 1}`, // Tên feature (có thể tùy chỉnh)
                        geom: geojson.geometry, // Dữ liệu hình học dạng GeoJSON
                        properties: JSON.stringify(feature.getProperties()), // Thuộc tính (nếu có)
                    };
                });
                const payload = {
                    features: featuresGeoJSON,
                    layer_name: selectedLayer.value,
                };
                console.log(payload)
                const create_draw_feature_response = await FeatureService.create_draw_feature(payload)
                console.log(create_draw_feature_response)
                if (create_draw_feature_response.status == '200') {
                    try {
                        // 1. Gọi API get_all_layer
                        const initLayer_response = await LayerService.get_all_layer(project_id.value);

                        // 2. Đợi initLayer và initLayerTable hoàn thành
                        await Promise.all([
                            initLayer(initLayer_response),
                        ]);

                        // 3. Cập nhật isLoaded sau khi tất cả hoàn thành
                        isLoaded.value = true;
                        console.log('All initialization completed, isLoaded:', isLoaded.value);
                    } catch (error) {
                        console.error('Lỗi trong quá trình khởi tạo:', error);
                        isLoaded.value = false; // Đặt lại isLoaded nếu có lỗi
                    }
                    DrawvectorSource.clear()
                }
            }
        };
        const handleSelectedLayer = (data) => {
            console.log('Received from DrawingPopup:', data.layer);
            if (data.layer) {
                selectedLayer.value = data.layer
            }
            isDrawing.value = data.drawStatus
        };
        // Hàm cập nhật công cụ vẽ
        const updateDrawInteraction = () => {
            // Xóa công cụ vẽ hiện tại (nếu có)
            if (drawInteraction) {
                console.log(drawInteraction)
                console.log(drawType.value)
                const interactions = mapInstance.value.getInteractions().getArray()
                for (let i = interactions.length - 1; i >= 0; i--) {
                    if (interactions[i] instanceof Draw) {
                        mapInstance.value.removeInteraction(interactions[i]);
                    }
                }
                drawInteraction = null;
            }
            // Thêm công cụ vẽ mới nếu không phải "None"
            if (drawType.value != 'None') {
                console.log("dang ve")
                drawInteraction = new Draw({
                    source: DrawvectorSource,
                    type: drawType.value,
                });
                // Xử lý sự kiện drawend
                drawInteraction.on('drawend', async (event) => {
                    const feature = event.feature;
                    const geojsonFormat = new GeoJSON();
                    const geojson = geojsonFormat.writeFeature(feature, {
                        featureProjection: 'EPSG:3857',
                        dataProjection: 'EPSG:4326', // Chuyển sang WGS84
                    });
                });
                mapInstance.value.addInteraction(drawInteraction);
            }
        }
        const openChartModal = () => {
            if (currentFloodLV.value !== null) {
                showChartModal.value = true;
            } else {
                alert('Vui lòng tải dữ liệu trước khi xem biểu đồ.');
            }
        };
        const updateStatusFeatureInformPopup = () => {
            noneDrawing.value = false;
        }
        const openMenu = async (type) => {
            activeMenu.value = type;
            if (type == 'FloodAndTemp') {
                return;
            } else if (type == 'Layers') {
                // 3. Kiểm tra project_id
                if (!project_id.value) {
                    throw new Error('project_id is not defined');
                }

                console.log(list_layer.value)
                // 4. Gọi API và đợi dữ liệu
                const initLayer_response = await LayerService.get_all_layer(project_id.value);

                // 5. Đợi initLayer và initLayerTable hoàn thành
                await Promise.all([
                    initLayer(initLayer_response),
                    initLayerTable(initLayer_response),
                ]);

                // 6. Cập nhật isLoaded sau khi tất cả hoàn thành
                isLoaded.value = true;
                console.log('All initialization completed, isLoaded:', isLoaded.value);
            } else {
                const get_all_layer_response = await LayerService.get_all_layer(project_id.value)
                if (get_all_layer_response.status == '200') {
                    const data = get_all_layer_response.data.layers
                    data.forEach(item => {
                        if (item[5] != 'L001' && item[5] != 'L006') {
                            listLayer.value.push(item)
                        }
                    })
                    const listIDlayer = []
                    listLayer.value.forEach(layer => {
                        if (layer[5] != 'L001' && layer[5] != 'L006') {
                            listIDlayer.push({ id: layer[0], name: layer[1] });
                        }
                    })
                    for (const { id, name } of listIDlayer) {
                        try {
                            const get_feature_by_id_layer_response = await FeatureService.get_feature_by_layer_id(id);
                            const features = get_feature_by_id_layer_response.data.features || []; // Đảm bảo features tồn tại
                            // Thêm từng feature cùng với tên layer vào mảng kết quả
                            features.features.forEach(feature => {
                                featureLayerPairs.value.push([feature, name]);
                            });
                        } catch (error) {
                            console.error(`Error fetching features for layer ID ${id}:`, error);
                        }
                    }
                }
                filterFeatures()
            }
        };
        const update_priority_layer = async (credential) => {
            console.log(credential)
            try {
                const update_priority_response = await LayerService.update_priority_layer(credential)
                console.log(update_priority_response)
            } catch (error) {
                console.error(`Error updating priority for layer ${credential[0]}:`, error);
                throw error;
            }
        };
        // Hàm initLayerTable
        const initLayerTable = async (initLayerTable_response) => {
            try {
                console.log(initLayerTable_response)
                if (initLayerTable_response?.status == '200' && initLayerTable_response.data?.layers) {
                    const data = initLayerTable_response.data;
                    const user_layers = [];
                    data.layers.forEach(layer => {
                        if (layer[5] !== 'L001') {
                            user_layers.push(layer);
                        }
                    });
                    list_layer.value = user_layers.sort((a, b) => b[10] - a[10]);
                    console.log('List-layer: ', list_layer.value)
                    console.log('initLayerTable completed:', user_layers);
                } else {
                    console.warn('initLayerTable: Invalid response or status not 200', initLayerTable_response);
                    list_layer.value = []; // Đặt giá trị mặc định nếu không có dữ liệu
                }
            } catch (error) {
                console.error('Error in initLayerTable:', error);
                list_layer.value = []; // Đặt giá trị mặc định nếu có lỗi
            }
        };

        // Hàm initLayer
        const initLayer = async (initLayer_response) => {
            try {
                if (initLayer_response?.status == '200' && initLayer_response.data?.layers) {
                    const data = initLayer_response.data;
                    const user_layers = [];

                    for (const layer of data.layers) {
                        if (layer[5] !== 'L001') {
                            user_layers.push(layer);
                            switch (layer[5]) {
                                case 'L002':
                                    try {
                                        const features = await initListFeature(layer[0]);
                                        console.log('Features for layer', layer[0], ':', features);
                                        // Chuyển đổi GeoJSON thành Feature OpenLayers
                                        const geojsonFormat = new GeoJSON();
                                        const olFeatures = features
                                            ? geojsonFormat.readFeatures(features, {
                                                dataProjection: 'EPSG:4326',
                                                featureProjection: 'EPSG:3857',
                                            })
                                            : [];
                                        const vectorLayer = new VectorLayer({
                                            source: new VectorSource({
                                                features: olFeatures,
                                            }),
                                            id: layer[0],
                                            name: layer[1],
                                            description: layer[9],
                                        });
                                        vectorLayer.setStyle(
                                            new Style({
                                                stroke: new Stroke({
                                                    color: layer[4],
                                                    width: layer[7],
                                                }),
                                                fill: new Fill({
                                                    color: layer[3], // Sửa lỗi: layer[3] thay vì [3]
                                                }),
                                            })
                                        );
                                        olFeatures.forEach(feat => {
                                            if (feat.getGeometry().getType() == 'Point') {
                                                feat.setStyle(
                                                    new Style({
                                                        image: new Circle({
                                                            radius: 6,
                                                            fill: new Fill({
                                                                color: layer[3],
                                                            }),
                                                            stroke: new Stroke({
                                                                color: layer[4],
                                                                width: layer[7],
                                                            }),
                                                        }),
                                                    })
                                                )
                                            }
                                        })
                                        // Đặt các thuộc tính khác cho layer
                                        vectorLayer.setVisible(false);
                                        vectorLayer.setZIndex(layer[10]); // Mặc định Z-index là 0 nếu layer[10] không hợp lệ
                                        const formatFeature = vectorLayer.getSource().getFeatures()
                                        formatFeature.forEach(feat => {
                                            feat.set('layer_name', layer[1])
                                        })
                                        // Thêm layer vào bản đồ
                                        mapInstance.value?.addLayer(vectorLayer);
                                    } catch (error) {
                                        console.error(`Error loading features for layer ${layer[0]}:`, error);
                                    }
                                    break;

                                case 'L006':
                                    const tileLayer = new TileLayer({
                                        source: new TileWMS({
                                            url: layer[8],
                                        }),
                                        id: layer[0],
                                        name: layer[1],
                                        description: layer[9],
                                    });
                                    tileLayer.setVisible(false);
                                    tileLayer.setZIndex(layer[10])
                                    mapInstance.value?.addLayer(tileLayer);
                                    break;
                                case 'L004':
                                    try {
                                        const features = await initListFeature(layer[0]);
                                        console.log('Features for layer', layer[0], ':', features);
                                        const vectorLayer = new VectorLayer({
                                            source: new VectorSource({
                                                features: features
                                                    ? new GeoJSON().readFeatures(features, {
                                                        dataProjection: "EPSG:4326",
                                                        featureProjection: "EPSG:3857",
                                                    })
                                                    : [],
                                            }),
                                            id: layer[0],
                                            name: layer[1],
                                            description: layer[9],
                                        });
                                        vectorLayer.setStyle(
                                            new Style({
                                                stroke: new Stroke({
                                                    color: layer[4],
                                                    width: layer[7],
                                                }),
                                                fill: new Fill({
                                                    color: layer[3], // Sửa lỗi: layer[3] thay vì [3]
                                                }),
                                            })
                                        );
                                        vectorLayer.setVisible(false);
                                        vectorLayer.setZIndex(layer[10])
                                        const formatFeature = vectorLayer.getSource().getFeatures()
                                        formatFeature.forEach(feat => {
                                            feat.set('layer_name', layer[1])
                                        })
                                        mapInstance.value?.addLayer(vectorLayer);
                                    } catch (error) {
                                        console.error(`Error loading features for layer ${layer[0]}:`, error);
                                    }
                                    break;
                            }
                        }
                    }
                    console.log('initLayer completed:', user_layers);
                } else {
                    console.warn('initLayer: Invalid response or status not 200', initLayer_response);
                }
            } catch (error) {
                console.error('Error in initLayer:', error);
            }
        };

        const initListFeature = async (layer_id) => {
            const initListFeature_response = await FeatureService.get_feature_by_layer_id(layer_id);
            if (initListFeature_response.status == '200') {
                const data = initListFeature_response.data;
                console.log('Data: ', data);
                console.log('Features: ', data.features);
                return data.features;
            } else {
                return null;
            }
        };
        // Tạo styleFunction để tùy chỉnh style cho từng loại hình học
        const controlLayer = (id, event) => {
            const isChecked = event.target.checked;
            console.log(isChecked)
            const layer_in_map = mapInstance.value.getLayers().getArray();

            console.log(id)
            layer_in_map.forEach(layer => {
                console.log(layer.get('id'));
                if (layer.get('id') == id) {
                    layer.setVisible(isChecked);
                }
            });
            console.log(mapInstance.value.getLayers().getArray())
        };

        const typeLayer = (type_id) => {
            switch (type_id) {
                case 'L001':
                    return 'Default Layer';
                case 'L002':
                    return 'Layer created from file';
                case 'L003':
                    return 'Layer created from feature';
                case 'L004':
                    return 'Layer created from layer';
                case 'L005':
                    return 'Layer created from draw features';
                case 'L006':
                    return 'Layer created by wms url';
            }
        };

        const deleteLayer = async (layer_id) => {
            const delete_layer_response = await LayerService.delete_layer(layer_id);
            console.log(delete_layer_response);
            if (delete_layer_response.data.status == '200') {
                const initLayer_response = await LayerService.get_all_layer(project_id.value);
                await initLayerTable(initLayer_response);
                const layer_in_map = mapInstance.value.getLayers().getArray();
                layer_in_map.forEach(layer => {
                    console.log(layer.get('id'));
                    if (layer.get('id') == layer_id) {
                        mapInstance.value.removeLayer(layer);
                    }
                });
            }
        };
        const deleteFeature = async (feature_id, index) => {
            const delete_feature_response = await FeatureService.delete_feature(feature_id)
            if (delete_feature_response.status == '200') {
                try {
                    // 1. Gọi API get_all_layer
                    const initLayer_response = await LayerService.get_all_layer(project_id.value);

                    // 2. Đợi initLayer và initLayerTable hoàn thành
                    await Promise.all([
                        initLayer(initLayer_response),
                    ]);

                    // 3. Cập nhật isLoaded sau khi tất cả hoàn thành
                    isLoaded.value = true;
                    console.log('All initialization completed, isLoaded:', isLoaded.value);
                } catch (error) {
                    console.error('Lỗi trong quá trình khởi tạo:', error);
                    isLoaded.value = false; // Đặt lại isLoaded nếu có lỗi
                }
                featureLayerPairs.value.splice(index, 1);
                alert("Delete feature successful!!")
            }
        }
        const filterFeatures = () => {
            // Lọc featureLayerPairs dựa trên selectedLayer
            if (selectedLayerName.value == 'All') {
                filteredFeatureLayerPairs.value = [...featureLayerPairs.value];
            } else {
                console.log(selectedLayerName.value)
                filteredFeatureLayerPairs.value = featureLayerPairs.value.filter(
                    pair => pair[1] == selectedLayerName.value
                );
            }
        }
        // Danh sách các style từ GeoServer
        const styles = [
            { text: 'None', value: '', level: '0' },
            { text: 'Current Sea Level', value: 'Lv0', level: '3.5' },
            { text: 'Sea Level Rise 1m', value: 'Lv1', level: '4.5' },
            { text: 'Sea Level Rise 2m', value: 'Lv2', level: '5.5' },
            { text: 'Sea Level Rise 3m', value: 'Lv3', level: '6.5' },
            { text: 'Sea Level Rise 4m', value: 'Lv4', level: '7.5' },
            { text: 'Sea Level Rise 5m', value: 'Lv5', level: '8.5' }
        ];
        // Tính toán text của style được chọn
        const selectedStyleText = computed(() => {
            const selected = styles.find((style) => style.value == selectedStyle.value);
            return selected ? selected.text : 'None';
        });
        const baseLayers = {
            osm: {
                layer: new TileLayer({ source: new OSM(), visible: true, "label": "OSM" }),
                label: "OSM",
            },
            google: {
                layer: new TileLayer({
                    source: new XYZ({ url: "https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}&key=AIzaSyAA8Nlt2SS2UwcEa4IAGYWlujC4C34mMf0" }),
                    visible: false,
                    "label": "Google Map"
                }),
                label: "Google Map",
            },
            satellite: {
                layer: new TileLayer({
                    source: new XYZ({ url: "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}&key=AIzaSyAA8Nlt2SS2UwcEa4IAGYWlujC4C34mMf0" }),
                    visible: false,
                    "label": "Google Satellite"
                }),
                label: "Google Satellite",
            },
            none: {
                layer: new TileLayer({
                    visible: false,
                    "label": "None",
                }),
                label: "None",
            }
        };
        const tiffLayer = {
            tiff8: {
                layer: new TileLayer({
                    source: new TileWMS({
                        url: 'http://localhost:7777/geoserver/wms',
                        params: {
                            'LAYERS': '	CT439:dbscl_dsm_final_nodata_cog',
                            'TILED': true,
                            'STYLE': 'Lv0',
                        },
                        serverType: 'geoserver',
                    }),
                    'label': 'GeoTIFF',
                    visible: false,
                }),
            },
        };
        const initMap = async () => {
            const Data = {
                "project_id": project_id.value,
                "layer_type": 'L001'
            }

            const layers_response = await LayerService.get_all_layer_by_type(Data)
            const layers_list = layers_response.data.layers

            const response = await FeatureService.get_default_feature()
            const layersData = response.data.features
            Default_vectorLayers.value = layersData.map((layerData) => {
                return new VectorLayer({
                    source: new VectorSource({
                        features: new GeoJSON().readFeatures(layerData, {
                            dataProjection: "EPSG:4326",
                            featureProjection: "EPSG:3857",
                        }),
                    }),
                });
            });
            console.log(Default_vectorLayers.value)

            Default_vectorLayers.value[0].set("label", "VietNam");
            Default_vectorLayers.value[0].setStyle(
                new Style({
                    stroke: new Stroke({
                        color: layers_list[2][4],
                        width: layers_list[2][7],
                    }),
                    fill: new Fill({
                        color: layers_list[2][3],
                    }),
                })
            );
            Default_vectorLayers.value[0].setZIndex(1)
            const firstLayer = Default_vectorLayers.value[0];
            let source = firstLayer.getSource()
            let DefaultFeatures = source.getFeatures()
            DefaultFeatures.forEach(feat => {
                feat.set('layer_name', 'VN')
            })

            Default_vectorLayers.value[1].set("label", "MD_District")
            Default_vectorLayers.value[1].setStyle(
                new Style({
                    stroke: new Stroke({
                        color: layers_list[1][4],
                        width: layers_list[1][7],
                    }),
                    fill: new Fill({
                        color: layers_list[1][3],
                    }),
                })
            );

            Default_vectorLayers.value[1].setZIndex(2)
            const secondLayer = Default_vectorLayers.value[1];
            source = secondLayer.getSource()
            DefaultFeatures = source.getFeatures()
            DefaultFeatures.forEach(feat => {
                feat.set('layer_name', 'MD_District')
            })
            Default_vectorLayers.value[2].set("label", "MD_State")
            Default_vectorLayers.value[2].setStyle(
                new Style({
                    stroke: new Stroke({
                        color: layers_list[0][4],
                        width: layers_list[0][7],
                    }),
                    fill: new Fill({
                        color: layers_list[0][3],
                    }),
                })
            );
            Default_vectorLayers.value[2].setZIndex(3)
            const thirdLayer = Default_vectorLayers.value[2];
            source = thirdLayer.getSource()
            DefaultFeatures = source.getFeatures()
            DefaultFeatures.forEach(feat => {
                feat.set('layer_name', 'MD_State')
            })

            // Khởi tạo bản đồ
            mapInstance.value = new Map({
                target: mapContainer.value,
                layers: [...Object.values(baseLayers).map((l) => l.layer), ...Object.values(tiffLayer).map((l) => l.layer), ...Default_vectorLayers.value, DrawvectorLayer],
                view: new View({
                    center: fromLonLat([106.5, 15.55]),
                    zoom: 6,
                    projection: 'EPSG:3857',
                }),
                controls: [],
            });
            mapInstance.value.on('click', async (event) => {
                if (!drawStatus.value) {
                    const featuresList = []
                    mapInstance.value.forEachFeatureAtPixel(event.pixel, (feature) => {
                        featuresList.push(feature);
                    });
                    if (featuresList.length > 0) {
                        console.log('Features at click:', featuresList);
                        console.log(featuresList[0])
                        const featureID = featuresList[0].getProperties().id;
                        console.log("ID: ", featureID)
                        const layer_name = featuresList[0].get('layer_name')
                        const FeatureData = {
                            "feature_id": featureID,
                            "layer_name": layer_name
                        }
                        Feature_Data.value = FeatureData;
                        clickCoordinates.value = event.coordinate;
                        noneDrawing.value = true;
                    }
                }
                else {
                    drawclickCoordinates.value = event.coordinate;
                }

            })

        };
        // Đóng dropdown khi click bên ngoài
        document.addEventListener('click', (event) => {
            const dropdown = document.querySelector('.custom-select-wrapper');
            if (!dropdown.contains(event.target)) {
                isDropdownOpen.value = false;
            }
        });

        // Hàm onMounted
        onMounted(async () => {
            try {
                // 1. Đợi initMap hoàn thành
                await initMap();
                // 2. Gán dữ liệu tĩnh cho vectorLayers và vnbaseLayers
                vectorLayers.value = {
                    md_state: {
                        layer: Default_vectorLayers.value[2],
                        label: Default_vectorLayers.value[2]?.get("label") || 'md_state', // Kiểm tra an toàn
                        name: 'md_state',
                    },
                    md_district: {
                        layer: Default_vectorLayers.value[1],
                        label: Default_vectorLayers.value[1]?.get("label") || 'md_district', // Kiểm tra an toàn
                        name: 'md_district',
                    },
                    none: {
                        layer: null,
                        label: 'None',
                        name: 'none',
                    },
                };
                console.log(vectorLayers.value)
                vnbaseLayers.value = {
                    vn: {
                        layer: Default_vectorLayers.value[0],
                        label: Default_vectorLayers.value[0]?.get("label") || 'vn', // Kiểm tra an toàn
                        name: 'vn',
                    },
                    none: {
                        layer: null,
                        label: 'None',
                        name: 'none',
                    },
                };
                console.log(vnbaseLayers.value)

            } catch (error) {
                console.error('Error in onMounted:', error);
                isLoaded.value = false;
            }
            const get_max_ZIndex_response = await LayerService.get_max_z_index(project_id.value)
            maxPriority.value = parseInt(get_max_ZIndex_response.data.z_index)
        });

        return {
            project_id,
            mapContainer,
            mapInstance,
            baseLayers,
            tiffLayer,
            selectedLayer,
            vectorLayers,
            activevectorLayer,
            isLoaded,
            isLoading,
            listLayer,
            listFeature,
            vnbaseLayers,
            activeVNLayer,
            selectedStyle,
            selectedStyleText,
            selectedLayerName,
            styles,
            isDropdownOpen,
            menuContent,
            selectedChartType,
            showChartModal,
            currentFloodLV,
            showCreateForm,
            showDetailModal,
            activeMenu,
            list_layer,
            featureLayerPairs,
            updateShowCreate,
            updateShowModal,
            backHome,
            toggleDropdown,
            changeBaseLayer,
            changeVN_BaseLayer,
            changeVectorLayer,
            selectStyle,
            showFloodInform,
            openChartModal,
            openMenu,
            updateLayer,
            initLayerTable,
            initLayer,
            initListFeature,
            controlLayer,
            typeLayer,
            deleteLayer,
            drawInteraction,
            drawType,
            setDrawType,
            updatePriorities,
            updateShowUpdate,
            fetchAllLayer,
            showUpdateForm,
            updateLayerID,
            isDrawing,
            handleSelectedLayer,
            clickCoordinates,
            saveFeature,
            deleteFeature,
            filteredFeatureLayerPairs,
            filterFeatures,
            floodData,
            noDataMessage,
            uniqueRows,
            noneDrawing,
            Feature_Data,
            drawclickCoordinates,
            updateStatusFeatureInformPopup,
        };
    },
};
</script>

<style>
@import '../../assets/css/container.css';
@import '../../assets/css/map.css';
@import '../../assets/css/menu.css';
</style>
<style scoped>
@import '../../assets/css/btn-toggle.css';

.create_layer_btn {
    width: 100%;
    margin-top: 10px;
    margin-bottom: 5px;
    font-size: 20px;
    border-radius: 8px;
    background-color: rgb(96, 221, 180);
    color: white;
    border: none;
}

#delete-layer,
#delete-feature,
#update-layer {
    padding: 4px 8px 4px 8px;
}

.draw-tool {
    width: 40px;
    height: 40px;
}

.no-before::before,
.selected-option::before {
    width: 0px;
}

.floodcontent {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    color: red;
}
</style>