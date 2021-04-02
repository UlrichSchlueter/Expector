<template>
  <div id="app">
    <b-container class="bv-example-row" fluid>
      <router-view />
      <b-row>
        <b-col cols="4">
          <starter></starter>
          <timer></timer>
          <b-tabs content-class="mt-3">
            <runs :bus="bus" purpose="Init">tr</runs>
            <runs :bus="bus" purpose="Running">te</runs>
            <runs :bus="bus" purpose="Failed">tr</runs>
            <runs :bus="bus" purpose="Finished">ein</runs>
          </b-tabs>
        </b-col>
        <b-col cols="4">
          <b-row>
            <single-run :bus="bus" runid=""></single-run>
          </b-row>
        </b-col>
        <b-col cols="4"><sensors :bus="bus"></sensors></b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import Vue from 'vue';
import Starter from './components/Starter.vue';
import Sensors from './components/Sensors.vue';
import Runs from './components/Runs.vue';
import Timer from './components/Timer.vue';
import SingleRun from './components/SingleRun.vue';

export default {
  name: 'app',
  data() {
    return {
      // https://code.luasoftware.com/tutorials/vuejs/parent-call-child-component-method/
      item: {},
      bus: new Vue(),
    };
  },
  components: {
    Starter,
    Runs,
    Sensors,
    Timer,
    SingleRun,
  },
  methods: {
    testFunction() {
      setInterval(() => {
        // eslint-disable-next-line
        //console.error('App Triggered');
        this.bus.$emit('submit');
        // this.components.Metrics.triggerMe();
      }, 2000);
    },
  },
  mounted() {
    // eslint-disable-next-line
    console.error('App mounted');
    this.testFunction();
  },
};
</script>

<style>
#app {
  margin-top: 60px;
}
</style>
