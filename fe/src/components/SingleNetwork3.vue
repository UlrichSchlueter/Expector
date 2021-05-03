<template>
  <v-container>
    <v-row>
      <v-col cols="4" class="d-flex justify-center align-center"> </v-col>
      <v-col id="my_dataviz" />
    </v-row>
  </v-container>
</template>

<script>
// cimport * as d3 from 'd3';
import * as d3plus from 'd3plus';
import axios from 'axios';

export default {
  name: 'SingleNetwork2',
  props: ['bus'],
  data() {
    return {
      runid: '',
      networkgraph: null,
    };
  },
  components: {},
  methods: {
    runChanged(data) {
      console.info('SingleRun runChanged');
      this.runid = data;
      this.loadGraph();
    },
    loadGraph() {
      const path = `http://localhost:5000/getGraph/${this.runid}`;
      const sss = this;
      if (this.runid !== '') {
        axios
          .get(path)
          .then((res) => {
            console.info('SingleRun loadGraph');
            // eslint-disable-next-line
            console.error(res.data);
            const x = sss.networkgraph;

            // x.nodes = res.data.nodes;
            // x.links = res.data.links;

            x.nodes(res.data.nodes)
              .links(res.data.links)
              .render();

            // eslint-disable-next-line no-underscore-dangle
            const nodeLookup = x._nodes.reduce((obj, d) => {
              // eslint-disable-next-line no-param-reassign
              obj[d.id] = d;
              return obj;
            });

            // eslint-disable-next-line no-underscore-dangle
            nodeLookup.forEach((d) => {
              // eslint-disable-next-line no-param-reassign
              // const shape = d.shape;

              console.error(d);
            });
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      }
    },
    createGraph() {
      const links = [
        { source: 'alpha', target: 'beta', weight: 10 },
        { source: 'alpha', target: 'gamma', weight: 10 },
        { source: 'epsilon', target: 'zeta', weight: 10 },
        { source: 'epsilon', target: 'theta', weight: 10 },
        { source: 'theta', target: 'alpha', weight: 10 },
      ];

      // d3.selectAll('#my_dataviz').remove();
      this.networkgraph = new d3plus.Sankey()
        .select('#my_dataviz')
        .links(links)
        .label((d) => d.id)
        .shapeConfig({
          Path: {
            label: false,
          },
          Rect: {
            label: true,
          },
        })
        .label((d) => d.id)
        .render();
    },
    getMessage() {
      // console.info('SingleNetwork2 getMessage');
      // this.loadGraph();
    },
  },
  mounted() {
    // set the dimensions and margins of the graph

    // append the svg object to the body of the page
    this.createGraph();
    this.bus.$on('submit', this.getMessage);
    this.bus.$on('runChanged', this.runChanged);
  },
};
</script>

<style lang="scss" scoped></style>
