<template>
    <b-modal v-model="showModal" @cancel="closeModal" ok-only @hidden="closeModal" size="xl">
        <table class="table table-striped table-bordered table-hover">
            <thead class="table-dark">
                <tr>
                    <th scope="col" class="text-center">Name</th>
                    <th scope="col" class="text-center">Created Date</th>
                    <th scope="col" class="text-center">Type</th>
                    <th scope="col" class="text-center">Status</th>
                    <th scope="col" class="text-center">Description</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(row, index) in list_layer" :key="index">
                    <td class="text-center align-middle fs-6">{{ row[1] }}</td>
                    <td class="text-center align-middle fs-6">{{ formatTimestamp(row[2]) }}</td>
                    <td class="text-center align-middle fs-6">
                        {{ typeLayer(row[5]) }}
                    </td>
                    <td class="text-center align-middle fs-6">
                        <select name="status" id="status" class="form-select" @change="updateStatus(row)" v-model="row[11]">
                            <option v-for="option in statusOption" :key="option" :value="option">
                                {{ option }}
                            </option>
                        </select>
                    </td>
                    <td class="text-center align-middle fs-6">{{ row[9] }}</td>
                </tr>
                <tr v-if="list_layer.length === 0">
                    <td colspan="5" class="text-center">No data available</td>
                </tr>
            </tbody>
        </table>
    </b-modal>
</template>

<script>
import LayerService from "../../services/layer.service";
import CommunityService from "../../services/community.service";
export default {
    props: {
        showDetailModal: Boolean,
        project_id: String,
    },

    data() {
        return {
            showModal: null,
            list_layer: [],
            statusOption: ['private', 'public']
        }
    },
    watch: {
        showDetailModal(newVal) {
            this.showModal = newVal; // Đồng bộ prop với v-model của modal
        },
    },
    methods: {
        async closeModal() {
            try {
                this.showModal = false;
                this.$emit('update:showModal', false);
            } catch (error) {
                console.error('Error in closeForm:', error);
            }
        },
        async initLayerTable(initLayerTable_response) {
            if (initLayerTable_response.status == '200') {
                const data = initLayerTable_response.data
                var user_layers = []
                data.layers.forEach(layer => {
                    if (layer[5] != 'L001') user_layers.push(layer)
                })
                this.list_layer = user_layers.sort((a, b) => b[10] - a[10]);
            }
        },
        formatTimestamp(timestamp) {
            if (!timestamp) return ''; // Xử lý trường hợp timestamp rỗng

            const date = new Date(timestamp); // Parse chuỗi timestamp thành đối tượng Date
            const day = String(date.getDate()).padStart(2, '0'); // Lấy ngày, thêm số 0 nếu cần
            const month = String(date.getMonth() + 1).padStart(2, '0'); // Lấy tháng (0-11, nên +1)
            const year = date.getFullYear(); // Lấy năm
            const hours = String(date.getHours()).padStart(2, '0'); // Lấy giờ
            const minutes = String(date.getMinutes()).padStart(2, '0'); // Lấy phút
            const seconds = String(date.getSeconds()).padStart(2, '0'); // Lấy giây

            // Định dạng: DD/MM/YYYY HH:mm:ss
            return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
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
        async updateStatus(row) {
            try {
                const response = await LayerService.update_status_layer(row)
                console.log(response)
                if (response.status === 200) {
                    console.log('✅ Cập nhật thành công:', response.data.message);
                } else {
                    console.warn('⚠️ Cập nhật thất bại:', response.data.message);
                }
            } catch (error) {
                console.error('❌ Lỗi khi gửi dữ liệu:', error);
            }
            if(row[11] == 'public'){
                try {
                    const response = await CommunityService.create_community(row)
                    console.log(response)
                    if (response.status === 200) {
                        console.log('✅ Cập nhật thành công:', response.data.message);
                    } else {
                        console.warn('⚠️ Cập nhật thất bại:', response.data.message);
                    }
                } catch (error) {
                    console.error('❌ Lỗi khi gửi dữ liệu:', error);
                }
            }
            else{
                try {
                    const response = await CommunityService.delete_community(row)
                    console.log(response)
                    if (response.status === 200) {
                        console.log('✅ Cập nhật thành công:', response.data.message);
                    } else {
                        console.warn('⚠️ Cập nhật thất bại:', response.data.message);
                    }
                } catch (error) {
                    console.error('❌ Lỗi khi gửi dữ liệu:', error);
                } 
            }
        }
    },
    async mounted() {
        const initLayer_response = await LayerService.get_all_layer(this.project_id)
        this.initLayerTable(initLayer_response)
    }

}

</script>