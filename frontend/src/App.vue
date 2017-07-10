<template>
  <div id="app">
    <div class="ui equal width grid container">
      <stat-header :step="step"></stat-header>
      <bag-list v-if="step === 1"></bag-list>
      <bag-param-list v-if="step === 2" :paramDict="paramDict"></bag-param-list>
      <bag-prog-list v-if="step === 3"
       :termDict="termDict" :progDict="progDict" :cmdList="cmdList">
      </bag-prog-list>
      <ctrl-bar :step="step"></ctrl-bar>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      step: 1,
      paramDict: [],
      termDict: [],
      statDict: []
    }
  },
  sockets: {
    connect: function () {
      console.log('socket connected')
      this.$socket.emit('call_init')
    },
    'init_state': function (stateDict) {
      this.paramDict = stateDict['bagParamDict']
      this.termDict = stateDict['bagTermOutputDict']
      this.progDict = stateDict['bagProgDict']
      this.cmdList = stateDict['cmdList']
    },
    'change_step': function (step) {
      this.step = step
    },
    'bag_param_change': function (dict) {
      this.paramDict = dict
    }
  }
}
</script>

<style>
#app {
  height: 100%
}
</style>
