<template>
  <v-container>
    <v-row>
      <v-col cols="4" class="d-flex justify-center align-center">
        <div>
          <h2>Zoomable Force Directed Graph</h2>
          <svg
            id="svg"
            width="1000"
            height="700"
            class="container-border"
          ></svg>
        </div>
      </v-col>
      <v-col id="arc" />
    </v-row>
  </v-container>
</template>

<script>
import * as d3 from 'd3';

export default {
  name: 'SingleNetwork23',
  props: ['bus'],
  components: {},
  methods: {
    getMessage() {
      console.info('SingleNetwork23 getMessage');
    },
  },
  mounted() {
    // create somewhere to put the force directed graph
    const svg = d3.select('svg');
    const width = +svg.attr('width');
    const height = +svg.attr('height');
    const radius = 15;
    const nodesData = [
      { name: 'Lillian', sex: 'F' },
      { name: 'Gordon', sex: 'M' },
      { name: 'Sylvester', sex: 'M' },
      { name: 'Mary', sex: 'F' },
      { name: 'Helen', sex: 'F' },
      { name: 'Jamie', sex: 'M' },
      { name: 'Jessie', sex: 'F' },
      { name: 'Ashton', sex: 'M' },
      { name: 'Duncan', sex: 'M' },
      { name: 'Evette', sex: 'F' },
      { name: 'Mauer', sex: 'M' },
      { name: 'Fray', sex: 'F' },
      { name: 'Duke', sex: 'M' },
      { name: 'Baron', sex: 'M' },
      { name: 'Infante', sex: 'M' },
      { name: 'Percy', sex: 'M' },
      { name: 'Cynthia', sex: 'F' },
      { name: 'Feyton', sex: 'M' },
      { name: 'Lesley', sex: 'F' },
      { name: 'Yvette', sex: 'F' },
      { name: 'Maria', sex: 'F' },
      { name: 'Lexy', sex: 'F' },
      { name: 'Peter', sex: 'M' },
      { name: 'Ashley', sex: 'F' },
      { name: 'Finkler', sex: 'M' },
      { name: 'Damo', sex: 'M' },
      { name: 'Imogen', sex: 'F' },
    ];
    // Sample links data
    // type: A for Ally, E for Enemy
    const linksData = [
      { source: 'Sylvester', target: 'Gordon', type: 'A' },
      { source: 'Sylvester', target: 'Lillian', type: 'A' },
      { source: 'Sylvester', target: 'Mary', type: 'A' },
      { source: 'Sylvester', target: 'Jamie', type: 'A' },
      { source: 'Sylvester', target: 'Jessie', type: 'A' },
      { source: 'Sylvester', target: 'Helen', type: 'A' },
      { source: 'Helen', target: 'Gordon', type: 'A' },
      { source: 'Mary', target: 'Lillian', type: 'A' },
      { source: 'Ashton', target: 'Mary', type: 'A' },
      { source: 'Duncan', target: 'Jamie', type: 'A' },
      { source: 'Gordon', target: 'Jessie', type: 'A' },
      { source: 'Sylvester', target: 'Fray', type: 'E' },
      { source: 'Fray', target: 'Mauer', type: 'A' },
      { source: 'Fray', target: 'Cynthia', type: 'A' },
      { source: 'Fray', target: 'Percy', type: 'A' },
      { source: 'Percy', target: 'Cynthia', type: 'A' },
      { source: 'Infante', target: 'Duke', type: 'A' },
      { source: 'Duke', target: 'Gordon', type: 'A' },
      { source: 'Duke', target: 'Sylvester', type: 'A' },
      { source: 'Baron', target: 'Duke', type: 'A' },
      { source: 'Baron', target: 'Sylvester', type: 'E' },
      { source: 'Evette', target: 'Sylvester', type: 'E' },
      { source: 'Cynthia', target: 'Sylvester', type: 'E' },
      { source: 'Cynthia', target: 'Jamie', type: 'E' },
      { source: 'Mauer', target: 'Jessie', type: 'E' },
      { source: 'Duke', target: 'Lexy', type: 'A' },
      { source: 'Feyton', target: 'Lexy', type: 'A' },
      { source: 'Maria', target: 'Feyton', type: 'A' },
      { source: 'Baron', target: 'Yvette', type: 'E' },
      { source: 'Evette', target: 'Maria', type: 'E' },
      { source: 'Cynthia', target: 'Yvette', type: 'E' },
      { source: 'Maria', target: 'Jamie', type: 'E' },
      { source: 'Maria', target: 'Lesley', type: 'E' },
      { source: 'Ashley', target: 'Damo', type: 'A' },
      { source: 'Damo', target: 'Lexy', type: 'A' },
      { source: 'Maria', target: 'Feyton', type: 'A' },
      { source: 'Finkler', target: 'Ashley', type: 'E' },
      { source: 'Sylvester', target: 'Maria', type: 'E' },
      { source: 'Peter', target: 'Finkler', type: 'E' },
      { source: 'Ashley', target: 'Gordon', type: 'E' },
      { source: 'Maria', target: 'Imogen', type: 'E' },
    ];
    // set up the simulation and add forces
    const simulation = d3.forceSimulation().nodes(nodesData);
    const linkForce = d3.forceLink(linksData).id((d) => d.name);
    const chargeForce = d3.forceManyBody().strength(-100);
    const centerForce = d3.forceCenter(width / 2, height / 2);
    simulation
      .force('chargeForce', chargeForce)
      .force('centerForce', centerForce)
      .force('links', linkForce);
    // add tick instructions:

    // add encompassing group for the zoom
    const g = svg.append('g').attr('class', 'everything');
    // draw lines for the links
    // eslint-disable-next-line no-unused-vars
    const link = g
      .append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(linksData)
      .enter()
      .append('line')
      .attr('stroke-width', 2)
      .style('stroke', 'green');
    // draw circles for the nodes
    // eslint-disable-next-line no-unused-vars
    const node = g
      .append('g')
      .attr('class', 'nodes')
      .selectAll('circle')
      .data(nodesData)
      .enter()
      .append('circle')
      .attr('r', radius)
      .attr('fill', 'green');
    // // add text
    // g.append('text')
    //   .attr('clip-path', function (d) {
    //     console.log('d: ', d.name)
    //     return 'url(#clip-' + d.name + ')'
    //   })
    //   .selectAll('tspan')
    //   .data(function (d) { return d.data.id.split('.').pop().split(/(?=[A-Z][^A-Z])/g) })
    //   .enter().append('tspan')
    //   .attr('x', 0)
    //   .attr('y', function (d, i, nodes) { return 13 + (i - nodes.length / 2 - 0.5) * 10 })
    //   .text(function (d) { return d })
    // let format = d3.format(',d')
    // // add title
    // node.append('title')
    //   .text(function (d) { return d.data.id + '\n' + format(d.value) })
    // add drag capabilities

    /** Functions * */
    // Function to choose what color circle we have
    // Let's return blue for males and red for females

    this.bus.$on('submit', this.getMessage);
  },
};
</script>
<style></style>
