<template lang="html">
  <div class="row">
    <div class="sixteen wide column">
      <template v-if="step === 1">
        <button class="ui labeled icon primary button" @click="scanSSD()">
          <i class="disk outline icon"></i>
          Scan SSD
        </button>
        <button class="ui labeled icon green button" @click="submitBag()">
          <i class="upload icon"></i>
          Submit Bag
        </button>
      </template>
      <template v-if="step === 2">
        <button class="ui labeled icon red button" @click="prevPage()">
          <i class="left arrow icon"></i>
          Previous Page
        </button>
        <button class="ui labeled icon green button" @click="startImport()">
          <i class="play icon"></i>
          Start Import
        </button>
      </template>
      <template v-if="step === 3">
        <button class="ui labeled icon red button" @click="prevPage()">
          <i class="left arrow icon"></i>
          Previous Page
        </button>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  props: ['step'],
  methods: {
    scanSSD () {
      this.$socket.emit('find_bags')
    },
    submitBag () {
      this.$socket.emit('submit_bag')
      this.$socket.emit('next_page')
    },
    startImport () {
      this.$socket.emit('start_import')
      this.$socket.emit('next_page')
    },
    prevPage () {
      this.$socket.emit('prev_page')
    }
  }
}
</script>

<style lang="css" scoped>
  div.row {
    text-align: center;
  }
</style>
