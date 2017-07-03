<template lang="html">
  <div class="row">
    <div class="sixteen wide column">
      <h1 v-if="step === 1">Scan and Select Bag</h1>
      <h1 v-if="step === 2">Configure and Start</h1>
      <h1 v-if="step === 3">Import Status</h1>
    </div>
  </div>
</template>

<script>
export default {
  props: ['step']
}
</script>

<style lang="css" scoped>
  div.row {
    text-align: center;
  }
</style>
