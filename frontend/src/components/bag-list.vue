<template lang="html">
  <div class="row">
    <div class="twelve wide column baglist">
      <div class="ui segment">
        <div class="ui vertical segment">
          <paginate
            name="bags"
            :list="bagList"
            :per="20"
            tag="div"
            class="ui celled list">
            <div v-for="bag in paginated('bags')" class="item" @click="addBag">
              <i class="tasks icon"></i>
              {{ bag }}
            </div>
          </paginate>
        </div>
        <div class="ui vertical segment">
          <paginate-links for="bags"></paginate-links>
        </div>
      </div>
    </div>
    <!-- <div class="four wide column">
      <textarea rows="48" cols="80" id="showBagArea"></textarea>
    </div> -->
    <div class="four wide column selectbag">
      <div class="ui segment">
        <div class="ui middle aligned divided list">
          <div class="item" v-for="bag in selectBagObj['selectBag']">
            {{ bag }}
            <i class="remove icon" @click="removeBag(bag)"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const $ = window.$

export default {
  data () {
    return {
      bagList: [],
      paginate: ['bags'],
      selectBagObj: {
        'selectBag': []
      }
    }
  },
  sockets: {
    'init_state': function (stateDict) {
      this.bagList = stateDict['allBag'] || []
      this.selectBagObj['selectBag'] = stateDict['selectBag'] || []
    },
    'all_bag_found': function (list) {
      this.bagList = list
    }
  },
  watch: {
    'selectBagObj': {
      handler: function (obj) {
        var textedJSON = JSON.stringify(obj, null, 4)
        console.log(textedJSON)
        $('#showBagArea').val(textedJSON)
        this.$socket.emit('select_bag_change', this.selectBagObj['selectBag'])
      },
      deep: true
    }
  },
  methods: {
    addBag (event) {
      let target = event.target
      let bag = $(target).text().trim()
      let array = this.selectBagObj['selectBag']
      let idx = array.indexOf(bag)
      if (idx > -1) {
        return
      }
      array.push(bag)
    },
    removeBag (bag) {
      let array = this.selectBagObj['selectBag']
      let idx = array.indexOf(bag)
      if (idx > -1) {
        array.splice(idx, 1)
      }
    }
  }
}
</script>

<style lang="css">
  .twelve.wide.column.baglist {
    left: -20%;
  }
  .four.wide.column.selectbag {
    left: -20%;
  }
  div.ui.segment {
    width: 800px;
  }
  div.ui.vertical.segment {
    border: 0;
  }
  div.item {
    width: 750px;
    font-size: 25px;
  }
  ul.paginate-links.bags {
    text-align: center;
    list-style-type: none;
    padding: 0;
  }
  li.number{
    display: inline-block;
    margin: 0 10px;
    font-size: 25px;
  }
  li.number.active > a {
    font-weight: bold;
  }
  li.number > a {
    color: #42b983;
  }
</style>
