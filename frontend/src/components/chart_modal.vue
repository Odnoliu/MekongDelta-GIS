<b-modal v-model="showChartModal" id="chartModal" title="Thống kê số district bị ngập" size="lg"
                hide-footer>
                <template #modal-header>
                    <h5 class="modal-title">Thống kê số district bị ngập</h5>
                    <b-form-select v-model="selectedChartType" class="w-auto ms-auto">
                        <b-form-select-option value="bar">Biểu đồ cột</b-form-select-option>
                        <b-form-select-option value="line">Biểu đồ đường</b-form-select-option>
                        <b-form-select-option value="pie">Biểu đồ tròn</b-form-select-option>
                    </b-form-select>
                    <button type="button" class="btn-close" @click="showChartModal = false" aria-label="Close"></button>
                </template>
                <FloodChart :flood-l-v="currentFloodLV" :chart-type="selectedChartType" />
                <template #modal-footer>
                    <b-button variant="secondary" @click="showChartModal = false">Đóng</b-button>
                </template>
            </b-modal>