<template lang="html">
  <div class="row">
    <div class="sixteen wide column">
      <table class="ui celled table">
        <thead>
          <tr>
            <th>Bag Name</th>
            <th>Import</th>
            <th>Compress Video</th>
            <th>Check</th>
            <th>Copy</th>
            <th>Submit</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(v, k) in progDict">
            <td style="width: 80px; white-space: nowrap;">{{ k }}</td>
            <template v-for="num in v">
              <td style="width:80px"><tag :num="num"></tag></td>
            </template>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  props: ['termDict', 'progDict'],
  sockets: {
    'cmd_output': function (obj) {
    }
  },
  components: {
    tag: require('./_tag')
  }
}
</script>

<style lang="css">
</style>
