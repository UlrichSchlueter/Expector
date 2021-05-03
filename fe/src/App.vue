<template>
  <div id="app">
    <b-container class="bv-example-row" fluid>
      <router-view />
      <b-row>
        <b-col cols="4">
          <b-card>
            <h2>Start Run</h2>
            <starter></starter>
          </b-card>
          <b-card>
            <h2>Runs By State</h2>
            <b-tabs content-class="mt-3">
              <runs :bus="bus" purpose="Init">tr</runs>
              <runs :bus="bus" purpose="Running">te</runs>
              <runs :bus="bus" purpose="Failed">tr</runs>
              <runs :bus="bus" purpose="Finished">ein</runs>
            </b-tabs>
          </b-card>
          <b-card>
            <sensors :bus="bus"></sensors>
          </b-card>
        </b-col>
        <b-col cols="8">
          <b-card>
            <single-network-2 :bus="bus">test</single-network-2>
          </b-card>

          <b-card>
            <single-run :bus="bus" runid=""></single-run>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import Vue from 'vue';
import Vuetify from 'vuetify';
import Starter from './components/Starter.vue';
import Sensors from './components/Sensors.vue';
import Runs from './components/Runs.vue';

import SingleRun from './components/SingleRun.vue';
// import SingleNetwork from './components/SingleNetwork.vue';
import SingleNetwork2 from './components/SingleNetwork2.vue';

Vue.use(Vuetify);

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
    SingleRun,
    SingleNetwork2,

    // SingleNetwork,
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
    // this.config = cytoconfig.cytoconfig;
  },
};
</script>

<style>
#app {
  margin-top: 60px;
}
</style>
