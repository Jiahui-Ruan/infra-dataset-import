<template lang="html">
  <div class="row">
    <div class="ui segment">
      <div class="ui vertical segment">
        <paginate
          name="bags"
          :list="bagList"
          :per="20"
          tag="div"
          class="ui celled list">
          <div v-for="bag in paginated('bags')" class="item">
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
</template>

<script>

export default {
  data () {
    return {
      bagList: [],
      paginate: ['bags']
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
    border: 0;
    border: none;
  }
  div.ui.vertical.segment {
    border: 0;
    border: none;
  }
  div.item {
    width: 800px;
    font-size: 25px;
  }
  ul.paginate-links.bags {
    list-style-type: none;
    padding: 0;
  }
  li.number {
    display: inline-block;
    margin: 0 10px;
    font-size: 25px;
  }
</style>
