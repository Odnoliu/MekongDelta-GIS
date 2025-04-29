<template>
  <div id="app">
    <!-- Khu vực hiển thị giao diện của router -->
    <router-view />
  </div>
</template>
<script>
export default {
  name: 'App',
};
</script>
<style>
/* Thêm các style chung của ứng dụng nếu cần */
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background-color: #f8f9fa;
}

</style>