<template>
  <v-container fluid>
    <h2>Run Name: {{ runid }}</h2>
    <v-row id="my_dataviz" fluid> </v-row>
  </v-container>
</template>

<script>
import Plotly from 'plotly.js-dist';
import axios from 'axios';

export default {
  name: 'SingleNetwork2',
  props: ['bus'],
  data() {
    return {
      runid: '',
      networkgraph: null,
      lastChange: 0,
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
            const resLabels = [];
            const resColors = [];
            const linkSource = [];
            const linkTarget = [];
            const linkValue = [];
            const x = res.data.nodes;
            x.forEach((n) => {
              let label = n.id;
              if (n.isFinished === true) {
                resColors.push('green');
              } else if (n.stepsDone > 0) {
                resColors.push('orange');
              } else {
                resColors.push('yellow');
              }
              label = `${label}(${n.stepsDone}/${n.stepsDone + n.stepsLeft})`;
              resLabels.push(label);
            });
            const y = res.data.links;
            y.forEach((l) => {
              linkSource.push(l.source);
              linkTarget.push(l.target);
              linkValue.push(1);
            });

            const transition = {
              duration: 0,
              easing: 'cubic-in-out',
            };

            const data2 = {
              type: 'sankey',
              orientation: 'h',
              arrangement: 'fixed',
              node: {
                pad: 15,
                thickness: 30,
                line: {
                  color: 'black',
                  width: 0.5,
                },
                label: resLabels,
                color: resColors,
              },

              link: {
                source: linkSource,
                target: linkTarget,
                value: linkValue,
              },
            };

            const data3 = [data2];

            const layout = {
              title: '',
              // eslint-disable-next-line object-shorthand
              transition: transition,
              font: {
                size: 10,
              },
            };
            if (sss.lastChange !== res.data.lastChange) {
              Plotly.react('my_dataviz', data3, layout);
              sss.lastChange = res.data.lastChange;
            }
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      }
    },
    createGraph() {
      const data = {
        type: 'sankey',
        orientation: 'h',
        arrangement: 'perpendicular',
        node: {
          pad: 15,
          thickness: 30,
          line: {
            color: 'black',
            width: 0.5,
          },
          label: ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'],
          color: ['blue', 'blue', 'blue', 'blue', 'blue', 'blue'],
        },

        link: {
          source: [0, 1, 0, 2, 3, 3],
          target: [2, 3, 3, 4, 4, 5],
          value: [8, 4, 2, 8, 4, 2],
        },
      };

      const data2 = [data];

      const layout = {
        title: '',
        transition: 0,
        font: {
          size: 10,
        },
      };

      Plotly.react('my_dataviz', data2, layout);
    },
    getMessage() {
      // console.info('SingleNetwork2 getMessage');
      this.loadGraph();
    },
  },
  mounted() {
    // set the dimensions and margins of the graph

    // append the svg object to the body of the page
    // this.createGraph();
    this.bus.$on('submit', this.getMessage);
    this.bus.$on('runChanged', this.runChanged);
  },
};
</script>

<style lang="scss" scoped></style>
