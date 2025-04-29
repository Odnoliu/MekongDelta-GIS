<template>
    <div v-if="isVisible" class="loader-container">
      <div class="whirl"></div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        isVisible: true,
      };
    },
    mounted() {
      setTimeout(() => {
        this.isVisible = false;
      }, 3000); // 3 giây
    },
  };
  </script>
  
  <style>
  .loader-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(0, 0, 0, 0.3);
  }
  .whirl {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    border: 5px solid #3498db;
    border-top: 5px solid transparent;
    animation: whirl 1s infinite linear;
  }
  
  @keyframes whirl {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
  </style>
  