<template>
  <HelloWorld />
</template>

<script>
import HelloWorld from './components/HelloWorld.vue';

export default {
  name: 'App',
  components: {
    HelloWorld,
  }
};
</script>

<style>
@font-face {
    font-family: 'Pretendard-Regular';
    src: url('https://fastly.jsdelivr.net/gh/Project-Noonnu/noonfonts_2107@1.1/Pretendard-Regular.woff') format('woff');
    font-weight: 400;
    font-style: normal;
}
@font-face {
    font-family: 'ClimateCrisisKR-1979';
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_2212@1.0/ClimateCrisisKR-1979.woff2') format('woff2');
    font-weight: 900;
    font-style: normal;
}
* {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}
body {
 -webkit-user-select: none;
 -moz-user-select: none;
 -ms-use-select: none;
  user-select: none;
  background:#fff;
  overflow-x:hidden;
}
#app {
  font-family: 'Pretendard-Regular', 'ClimateCrisisKR-1979';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
