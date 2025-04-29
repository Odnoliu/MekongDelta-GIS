<template>
    <b-modal v-model="showModal" title="Enter your new Layer's information" @ok="submitForm" @cancel="closeForm"
        @hidden="closeForm">
        <b-form>
            <b-form-group label="Layer's name:" label-for="name">
                <b-form-input id="name" v-model="formData.name" placeholder="Enter your Layer's name"></b-form-input>
            </b-form-group>
            <b-form-group label="Layer type">
                <!-- Tab buttons -->
                <div class="tab">
                    <button class="tablinks" :class="{ active: activeTab == 'Files' }" @click="openLayerInput('Files')">
                        Files
                    </button>
                    <button class="tablinks" :class="{ active: activeTab == 'WMS/WFS' }"
                        @click="openLayerInput('WMS/WFS')">
                        WMS/WFS
                    </button>
                    <button class="tablinks" :class="{ active: activeTab == 'Layers' }"
                        @click="openLayerInput('Layers')">
                        Layers
                    </button>
                </div>

                <!-- Tab content -->
                <div v-show="activeTab == 'Files'" id="Files" class="tabcontent">
                    <div id="file-content">
                        <label for="fileInput" class="form-label">Upload GeoJSON, KMZ, Shapefile, and Gpkg</label>
                        <input type="file" id="fileInput" accept=".json,.kmz,.zip,.kgpk" @change="onFileChange" />
                    </div>
                    <div id="file-color">
                        <label for="fillColor" class="form-label color-label">Fill color </label>
                        <input type="color" v-model="formData.fill_color" id="fillColor">
                        <label for="strokeColor" class="form-label color-label">Stroke color </label>
                        <input type="color" v-model="formData.stroke_color" id="strokeColor">

                    </div>
                    <div id="stroke-width">
                        <label for="strokeWidth">Stroke width:</label>
                        <input type="range" id="strokeWidth" v-model="formData.stroke_width" min="1" max="5">
                        <span>{{ formData.stroke_width }}</span>
                    </div>
                </div>

                <div v-show="activeTab == 'WMS/WFS'" id="WMS" class="tabcontent wms_div">
                    <label for="wms"> Enter your WMS link: </label>
                    <input v-model="formData.wms_url" id="wms" />
                </div>

                <div v-show="activeTab == 'Layers'" id="Layers" class="tabcontent">
                    <table class="table table-striped table-bordered table-hover">
                        <tbody>
                            <tr v-for="(row, index) in list_layer" :key="index">
                                <td class="text-center align-middle fs-6">{{ row[1] }}</td>
                                <td class="text-center align-middle fs-6">
                                    {{ typeLayer(row[5]) }}
                                </td>
                                <td class="text-center align-middle fs-6">
                                    <input type="checkbox" v-model="selectedLayers[index]">
                                </td>
                            </tr>
                            <tr v-if="list_layer.length == 0">
                                <td colspan="3" class="text-center">No data available</td>
                            </tr>
                        </tbody>
                        <tbody>
                            <tr v-for="(row, index) in community_layer" :key="index">
                                <td class="text-center align-middle fs-6">
                                    {{ row[2] }}
                                    <small class="text-secondary fst-italic">(Layer from community)</small>
                                </td>
                                <td class="text-center align-middle fs-6">
                                    {{ typeLayer(row[4]) }}
                                </td>
                                <td class="text-center align-middle fs-6">
                                    <input type="checkbox" v-model="selectedCommunityLayers[index]">
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <div id="color">
                        <label for="fillColor" class="form-label color-label">Fill color </label>
                        <input type="color" v-model="formData.fill_color" id="fillColor">
                        <label for="strokeColor" class="form-label color-label">Stroke color </label>
                        <input type="color" v-model="formData.stroke_color" id="strokeColor">

                    </div>
                </div>
            </b-form-group>
            <b-form-group label="Description:" label-for="description">
                <b-form-input id="description" v-model="formData.description"
                    placeholder="Enter your Layer's description"></b-form-input>
            </b-form-group>
            <b-form-group label="Priority" label-for="priority">
                <b-form-input id="priority" v-model="formData.priority" placeholder="Enter your Layer's priority"
                    type="number" max="100">
                </b-form-input>
            </b-form-group>
        </b-form>
    </b-modal>
</template>

<script>
import CommunityService from '../../services/community.service';
import LayerService from '../../services/layer.service';
export default {
    props: {
        showCreateForm: Boolean,
        project_id: String,
    },
    data() {
        return {
            showModal: null,
            activeTab: 'Files',
            list_layer: [],
            community_layer: [],
            formData: {
                name: "",
                description: "",
                file: null,
                fill_color: "#006699",
                stroke_color: "#001100",
                stroke_width: 2,
                wms_url: "",
                priority: 1,
            },
            defaultData: {
                name: "",
                description: "",
                fill_color: "#006699",
                stroke_color: "#001100",
                stroke_width: 2,
                wms_url: "",
                priority: 1,
            },
            isFocused: false,
            selectedLayers: [],
            selectedCommunityLayers: [],
        };
    },
    watch: {
        showCreateForm(newVal) {
            this.showModal = newVal; // Đồng bộ prop với v-model của modal
        },
    },
    methods: {
        closeForm() {
            try {
                this.showModal = false;
                this.$emit('update:showCreateForm', false);
                this.formData = { ...this.defaultData };
            } catch (error) {
                console.error('Error in closeForm:', error);
            }
        },
        async submitForm() {
            const Data = new FormData();
            Data.append("name", this.formData.name)
            Data.append("description", this.formData.description)
            Data.append("project_id", this.project_id)
            Data.append("priority", this.formData.priority)
            if (this.activeTab == 'Files') {
                if (this.formData.file) {
                    Data.append('file', this.formData.file);
                    Data.append("fill_color", this.formData.fill_color)
                    Data.append("stroke_color", this.formData.stroke_color)
                    Data.append("stroke_width", this.formData.stroke_width)
                    const response = await LayerService.create_file_layer(Data)
                    console.log(response)
                    if (response.status == '200') {
                        alert(`Create your layer: ${this.formData.name} successfull!!!`)
                    }
                }
                else {
                    alert('Please enter your GIS file!')
                }
            } else if (this.activeTab == 'WMS/WFS') {
                if (this.formData.wms_url == "") {

                    alert('Please enter your WMS url!')
                }
                else {
                    const wms_url = this.formData.wms_url
                    if (!this.isValidWmsUrl(wms_url)) {
                        alert('Invalid WMS URL! Please enter a valid URL containing "wms".');
                        this.requiresAuth = false
                        return;
                    }
                    else {
                        const check_response = await this.checkWmsUrl(wms_url)
                        if (check_response) {
                            console.log(wms_url)
                            Data.append("wms_url", wms_url)
                            const wms_response = await LayerService.create_wms_layer(Data)
                            console.log(wms_response)
                            if (wms_response.status == '200') {
                                alert(`Create your layer: ${this.formData.name} successfull!!!`)
                            }
                        }
                    }
                }
            } else if(this.activeTab == 'Layers'){
                // Lọc các row[0] từ list_layer dựa trên selectedLayers
                const selectedListLayerIds = this.list_layer
                    .filter((row, index) => this.selectedLayers[index])
                    .map(row => ({
                        id: row[0],    // Lưu row[0]
                        type: row[5]   // Lưu row[5]
                    }));

                // Lọc các row[0] từ community_layer dựa trên selectedCommunityLayers
                const selectedCommunityLayerIds = this.community_layer
                    .filter((row, index) => this.selectedCommunityLayers[index])
                    .map(row => ({
                        id: row[0],    // Lưu row[0]
                        type: row[4]   // Lưu row[4] 
                    }));
                
                const allSelectedLayers = [...selectedListLayerIds, ...selectedCommunityLayerIds];
                Data.append("fill_color", this.formData.fill_color)
                Data.append("stroke_color", this.formData.stroke_color)
                Data.append("layers", JSON.stringify(allSelectedLayers))
                const response = await LayerService.create_layer_from_layer(Data)
                if(response.status == '200'){
                    console.log(response.data.new_layer_id)
                }
            }
            this.$emit("created")
            this.closeForm()

        },
        onFileChange(event) {
            const file = event.target.files[0];
            if (!file) return;

            // Kiểm tra định dạng file
            const validExtensions = ['.json', '.kmz', '.zip'];
            const fileExtension = file.name.slice(file.name.lastIndexOf('.')).toLowerCase();
            if (!validExtensions.includes(fileExtension)) {
                alert('Please upload a valid GeoJSON, KML, Geopackage or Shapefile.');
                return;
            }
            this.formData.file = file;
        },
        openLayerInput(tabName) {
            console.log(tabName)
            this.activeTab = tabName; // Cập nhật tab đang active
        },

        // Kiểm tra URL WMS hợp lệ (regex cơ bản)
        isValidWmsUrl(url) {
            const wmsRegex = /^https?:\/\/[^\s/$.?#].[^\s]*$/i;
            return wmsRegex.test(url) && url.toLowerCase().includes('wms');
        },

        // Kiểm tra WMS URL có yêu cầu xác thực không
        async checkWmsUrl(url) {
            const response = await LayerService.proxy_wms_capabilities(url);
            try {
                if (response.status === 401 || response.status === 403) {
                    alert('This WMS URL requires authentication. Please use a public WMS URL instead.');
                    return false
                } else if (response.status == 200) {
                    return true
                } else {
                    alert(`WMS returned an error: ${response.status}. Please check the URL.`);
                    return false
                }
            } catch (error) {
                alert('Error checking WMS URL: ' + error.message);
                return false
            }
        },
        typeLayer(type_id) {
            switch (type_id) {
                case 'L001':
                    return 'Default Layer'
                case 'L002':
                    return 'Layer created from file'
                case 'L003':
                    return 'Layer created from feature'
                case 'L004':
                    return 'Layer created from layer'
                case 'L005':
                    return 'Layer created from draw features'
                case 'L006':
                    return 'Layer created by wms url'
            }
        },
    },
    async mounted() {
        const layer_response = await LayerService.get_all_layer(this.project_id)
        console.log(layer_response)
        if (layer_response.status == '200') {
            layer_response.data.layers.forEach(element => {
                if((element[5] != 'L006') && (element[5] != 'L001')){
                    this.list_layer.push(element)
                }
            });
            console.log('List_layer: ', this.list_layer)
        }
        const community_response = await CommunityService.get_all_community()
        console.log(community_response)
        if (community_response.status == '200') {
            community_response.data.layers.forEach(element =>{
                if(element[5] != 'L006'){
                    this.community_layer.push(element)
                }
            }) 
        }
        const get_max_ZIndex_response = await LayerService.get_max_z_index(this.project_id)
        console.log("Max z_index: ",get_max_ZIndex_response)
        this.formData.priority = parseInt(get_max_ZIndex_response.data.z_index) +1
    }
};
</script>
<style>
/* Style the tab */
.tab {
    overflow: hidden;
    border: 1px solid #ccc;
    background-color: #f1f1f1;
}

/* Style the buttons inside the tab */
.tab button {
    background-color: inherit;
    float: left;
    border: none;
    outline: none;
    cursor: pointer;
    padding: 14px 16px;
    transition: 0.3s;
    font-size: 17px;
}

/* Change background color of buttons on hover */
.tab button:hover {
    background-color: #ddd;
}

/* Create an active/current tablink class */
.tab button.active {
    background-color: #ccc;
}

/* Style the tab content */
.tabcontent {
    padding: 6px 12px;
    border: 1px solid #ccc;
    border-top: none;
}

#file-content {
    margin-bottom: 15px;
}

#file-color, #color,
#stroke-width {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 15px;
}

#color{
    margin-top: 15px;
}
.wms_div {
    height: 60px;
}

#WMS>input {
    height: 30px;
    width: 250px;
    border: none;
    margin: 10px 0px 10px 10px;
}
</style>
