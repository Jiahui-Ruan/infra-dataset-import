<template lang="html">
  <div :style="styleObject" ref="tag"></div>
</template>

<script>
export default {
  data () {
    return {
      styleObject: {
        width: 80px,
        height: 20px,
        background-color: this.num
      }
    }
  }
  props: ['num'],
  watch: {
    num () {
      console.log(this.num)
      switch (this.num) {
        case -1:
          this.$refs.tag.style.backgroundColor = '#e6ffe6'
          break
        case 0:
          this.$refs.tag.style.backgroundColor = '#21ba45'
          break
        case 1:
          this.$refs.tag.style.backgroundColor = '#db2828'
          break
        case 2:
          this.$refs.tag.style.backgroundColor = '#fbbd08'
          break
        case 3:
          this.$refs.tag.style.backgroundColor = '#2185d0'
          break
      }
    }
  }
}
</script>

<style lang="css">
</style>
