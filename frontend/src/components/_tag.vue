<template lang="html">
  <div :style="styleObject" ref="tag"></div>
</template>

<script>
export default {
  data () {
    return {
      styleObject: {
        width: '100px',
        height: '20px',
        backgroundColor: this.color
      }
    }
  },
  props: ['color'],
  watch: {
    color () {
      this.styleObject.backgroundColor = this.color
    }
  }
}
</script>

<style lang="css">
</style>
