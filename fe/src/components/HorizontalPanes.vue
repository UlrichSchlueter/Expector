<template>
  <multipane class="horizontal-panes" layout="horizontal">
    <single-network-2 :bus="bus">test</single-network-2>

    <multipane-resizer></multipane-resizer>

    <single-run :bus="bus" runid=""></single-run>
    <multipane-resizer></multipane-resizer>
    <div>test</div>
  </multipane>
</template>

<script>
import { Multipane, MultipaneResizer } from 'vue-multipane';
import SingleRun from './SingleRun.vue';
// import SingleNetwork from './components/SingleNetwork.vue';
import SingleNetwork2 from './SingleNetwork2.vue';

export default {
  props: ['bus'],
  components: {
    Multipane,
    MultipaneResizer,
    SingleRun,
    SingleNetwork2,
  },
};
</script>

<style>
.horizontal-panes {
  width: 100%;
  height: 600px;
  border: 1px solid #ccc;
}

.horizontal-panes > .pane {
  text-align: left;
  padding: 15px;
  overflow: hidden;
  background: #eee;
}

.horizontal-panes > .pane ~ .pane {
  border-top: 1px solid #ccc;
}
</style>
