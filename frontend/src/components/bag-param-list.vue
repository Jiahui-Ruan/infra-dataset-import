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
            <td><div style="width: 80px;">{{ k }}</div></td>
            <td>
              <textarea rows="10" cols="120"
              @input="changeParam(k, $event)">{{ v }}</textarea>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
const $ = window.$

export default {
  props: ['paramDict'],
  methods: {
    changeParam (k, event) {
      this.paramDict[k] = $(event.target).val()
      this.$socket.emit('bag_param_change', this.paramDict)
    }
  }
}
</script>

<style lang="css" scoped>
  textarea {
    width: 1200px;
    height: 200px;
  }
</style>
