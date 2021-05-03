<template>
  <v-container>
    <v-row>
      <v-col cols="4" class="d-flex justify-center align-center"> </v-col>
      <v-col id="my_dataviz" />
    </v-row>
  </v-container>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios';

export default {
  name: 'SingleNetwork23',
  props: ['bus'],
  data() {
    return {
      link: null,
      node: null,
      simulation: null,
      status: '',
    };
  },
  components: {},
  methods: {
    getMessage() {
      // console.info('SingleNetwork23 getMessage');
    },
    ticked() {
      this.link
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y);

      this.node.attr('cx', (d) => d.x + 6).attr('cy', (d) => d.y - 6);
    },
    createGraph() {
      const margin = {
        top: 10,
        right: 30,
        bottom: 30,
        left: 40,
      };
      const width = 400 - margin.left - margin.right;
      const height = 400 - margin.top - margin.bottom;

      // eslint-disable-next-line no-unused-vars
      const svg = d3
        .select('#my_dataviz')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

      // eslint-disable-next-line operator-linebreak
      const path =
        'https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/data_network.json';
      this.status = 'Starting';
      axios
        .get(path)
        .then((res) => {
          // eslint-disable-next-line
          console.error('Data loaded');

          this.link = svg
            .selectAll('line')
            .data(res.data.links)
            .enter()
            .append('line')
            .style('stroke', '#aaa');

          // Initialize the nodes
          this.node = svg
            .selectAll('circle')
            .data(res.data.nodes)
            .enter()
            .append('circle')
            .attr('r', 20)
            .style('fill', '#69b3a2');

          this.simulation = d3
            .forceSimulation(res.data.nodes) // Force algorithm is applied to data.nodes
            .force(
              'link',
              d3
                .forceLink() // This force provides links between nodes
                .id((d) => d.id) // This provide  the id of a node
                // eslint-disable-next-line comma-dangle
                .links(res.data.links) // and this the list of links
            )
            .force('charge', d3.forceManyBody().strength(-400)) // This adds repulsion between nodes. Play with the -400 for the repulsion strength
            .force('center', d3.forceCenter(width / 2, height / 2)) // This force attracts nodes to the center of the svg area
            .on('end', this.ticked);

          this.ticked();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  mounted() {
    // set the dimensions and margins of the graph

    // append the svg object to the body of the page
    this.createGraph();
    this.bus.$on('submit', this.getMessage);
  },
};
</script>

<style lang="scss" scoped></style>
