<template lang="html">
  <div class="row">
    <div class="sixteen wide column">
      <table class="ui celled table">
        <thead>
          <tr>
            <th>Bag Name</th>
            <th>Parameter</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(v, k) in paramDict">
            <td> {{ v }}</td>
            <td> {{ k }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  props: ['paramDict']
}
</script>

<style lang="css" scoped>
</style>
