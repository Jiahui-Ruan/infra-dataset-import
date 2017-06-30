<template>
  <div id="app">
    <div class="ui equal width grid container">
      <stat-header></stat-header>
      <bag-list></bag-list>
      <ctrl-bar></ctrl-bar>
    </div>
  </div>
</template>

<script>
export default {
  sockets: {
    connect: function () {
      console.log('socket connected')
    }
  }
}
</script>

<style>
#app {
  height: 100%
}
</style>
