<template lang="html">
  <div class="row">
    <div class="twelve wide column">
      <div class="ui segment">
        <div class="ui vertical segment">
          <paginate
            name="bags"
            :list="bagList"
            :per="20"
            tag="div"
            class="ui celled list">
            <div v-for="bag in paginated('bags')" class="item" @click="toggleItem">
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
    <div class="four wide column">
      <textarea rows="48" cols="80" id="showBagArea"></textarea>
    </div>
  </div>
</template>

<script>
const $ = window.$

function replacer (key, value) {
  // Filtering out properties
  if (typeof value === 'string') {
    return value.trim()
  }
  return value
}

export default {
  data () {
    return {
      bagList: [],
      paginate: ['bags'],
      selectBag: {
        'select': []
      }
    }
  },
  watch: {
    'selectBag': {
      handler: function (obj) {
        var textedJSON = JSON.stringify(obj, replacer, 4)
        console.log(textedJSON)
        $('#showBagArea').val(textedJSON)
      },
      deep: true
    }
  },
  methods: {
    toggleItem (event) {
      let target = event.target
      if ($(target).hasClass('active')) {
        $(target).removeClass('active')
        // TODO: remember to delete the bag
      } else {
        $(target).addClass('active')
        // cmdObj['param'] = event.data.param
        this.selectBag['select'].push($(target).text())
      }
    }
  },
  sockets: {
    allBagFound: function (list) {
      this.bagList = list
    }
  }
}
</script>

<style lang="css">
  div.ui.segment {
    width: 800px;
    border: 0;
    border: none;
  }
  div.ui.vertical.segment {
    border: 0;
  }
  div.item {
    width: 750px;
    font-size: 25px;
  }
  div.item.active {
    background-color: #1E90FF;
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
