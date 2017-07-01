<template lang="html">
  <div class="row">
    <div class="sixteen wide column">
      <button class="ui labeled icon primary button" @click="scanSSD()">
        <i class="disk outline icon"></i>
        Scan SSD
      </button>
      <button class="ui labeled icon green button">
        <i class="upload icon"></i>
        Submit Bag
      </button>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    scanSSD () {
      this.$socket.emit('find_bags')
    }
  }
}
</script>

<style lang="css" scoped>
  div.row {
    text-align: center;
  }
</style>
