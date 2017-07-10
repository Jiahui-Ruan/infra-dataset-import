<template lang="html">
  <div class="row">
    <div class="twelve wide column">
      <div class="ui vertical segment">
          <table class="ui celled table">
            <thead>
              <tr>
                <th style="width:100px">Bag Name</th>
                <template v-for="cmd in cmdList">
                  <th style="width:100px">{{ cmd }}</th>
                </template>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(v, k) in progDict">
                <td style="width: 100px; white-space: nowrap;">
                  <a class="ui label tag" @click="changeTerm(k)">{{ k }}</a>
                </td>
                <template v-for="color in v">
                  <td style="width:100px"><tag :color="color">{{ color }}</tag></td>
                </template>
              </tr>
            </tbody>
          </table>
        </div>
    </div>
    <div class="four wide column">
      <div class="ui vertical segment">
        <div class="terminal">
          terminal&#10;
          {{ termOutput }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      termOutput: 'You can choose a bag to see its output',
      selectBagName: ''
    }
  },
  props: ['termDict', 'progDict', 'cmdList'],
  components: {
    tag: require('./_tag')
  },
  methods: {
    changeTerm (bagName) {
      this.selectBagName = bagName
      this.termOutput = this.termDict[bagName].join('\r\n\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0')
    }
  },
  watch: {
    termDict: {
      handler: function (dict) {
        if (this.selectBagName) {
          this.termOutput = dict[this.selectBagName].join('\r\n\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0')
        }
      },
      deep: true
    }
  }
}
</script>

<style lang="css" scoped>
  div.terminal {
    margin-left: 100px;
    background-color: #000000;
    color: #02f71f;
    font-size: x-large;
    white-space: pre-wrap;
    width: 1000px;
    height: 620px;
    overflow: scroll;
  }
</style>
