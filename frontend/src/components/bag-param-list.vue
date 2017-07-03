<template lang="html">

</template>

<script>
export default {
  sockets: {
    'terminal_rst': function(obj) {
      console.log(obj)
    }
  }
}
</script>

<style lang="css">
</style>
