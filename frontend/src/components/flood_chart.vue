<template>
    <div class="chart-container">
      <div v-if="loading">Đang tải dữ liệu...</div>
      <div v-else-if="error">{{ error }}</div>
      <component v-else :is="chartComponent" :chart-data="chartData" :options="chartOptions" />
    </div>
  </template>
  
  <script>
  import { Bar, Line, Pie } from 'vue-chartjs';
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, LineElement, PointElement, CategoryScale, LinearScale, PieController, ArcElement } from 'chart.js';
  import Flood_And_TempService from '../services/flood_and_temp.service';
  import { ref, watch, onMounted } from 'vue';
  
  // Đăng ký các thành phần cần thiết của Chart.js
  ChartJS.register(Title, Tooltip, Legend, BarElement, LineElement, PointElement, CategoryScale, LinearScale, PieController, ArcElement);
  
  export default {
    name: 'FloodChart',
    components: {
      BarChart: Bar,
      LineChart: Line,
      PieChart: Pie,
    },
    props: {
      floodLV: {
        type: Number,
        required: true,
      },
      chartType: {
        type: String,
        default: 'bar',
        validator: value => ['bar', 'line', 'pie'].includes(value),
      },
    },
    setup(props) {
      const chartData = ref(null);
      const loading = ref(false);
      const error = ref(null);
  
      const fetchData = async () => {
        loading.value = true;
        error.value = null;
        try {
          const response = await Flood_And_TempService.get_flood_inform();
          console.log('FloodChart API Response:', response);
  
          if (!response || !response.data) {
            throw new Error('Không có dữ liệu từ API.');
          }
  
          const floodData = Array.isArray(response.data) ? response.data : response.data.floodata;
  
          if (!Array.isArray(floodData)) {
            throw new Error('Dữ liệu không hợp lệ.');
          }
  
          // Lọc dữ liệu dựa trên floodLV
          const filteredData = floodData.filter(item => item.Elve_mean <= props.floodLV);
  
          if (!filteredData || filteredData.length === 0) {
            throw new Error(`Không có vùng nào có mức ngập lụt <= ${props.floodLV}.`);
          }
  
          // Nhóm dữ liệu theo State và đếm số district
          const stateCounts = filteredData.reduce((acc, item) => {
            const state = item.State || 'Unknown';
            if (!acc[state]) {
              acc[state] = 0;
            }
            acc[state]++;
            return acc;
          }, {});
  
          const labels = Object.keys(stateCounts);
          const counts = Object.values(stateCounts);
  
          chartData.value = {
            labels: labels,
            datasets: [
              {
                label: 'Số district bị ngập',
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                data: counts,
              },
            ],
          };
        } catch (err) {
          error.value = err.message || 'Có lỗi xảy ra khi lấy dữ liệu.';
          chartData.value = {
            labels: [],
            datasets: [
              {
                label: 'Số district bị ngập',
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                data: [],
              },
            ],
          };
        } finally {
          loading.value = false;
        }
      };
  
      // Gọi API khi component được mount
      onMounted(() => {
        fetchData();
      });
  
      // Theo dõi sự thay đổi của floodLV và gọi lại API
      watch(() => props.floodLV, () => {
        fetchData();
      });
  
      const chartComponent = () => {
        return props.chartType === 'bar' ? 'BarChart' : props.chartType === 'line' ? 'LineChart' : 'PieChart';
      };
  
      const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: props.chartType === 'pie' ? {} : {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Số district',
            },
            ticks: {
              stepSize: 1,
            },
          },
          x: {
            title: {
              display: true,
              text: 'Thành phố (State)',
            },
          },
        },
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Thống kê số district bị ngập theo thành phố',
          },
        },
      };
  
      return {
        chartData,
        chartComponent,
        chartOptions,
        loading,
        error,
      };
    },
  };
  </script>
  
  <style scoped>
  .chart-container {
    position: relative;
    height: 400px;
    width: 100%;
  }
  </style>