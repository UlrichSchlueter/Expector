<template>
  <div class="border">
    <b-button v-b-toggle.collapse-1>Show Steps</b-button>
    <b-card v-for="item in metrics" :key="item.name" :title="item.name">
      {{ runid }}
      <b-card-text>
        <b-badge v-if="item.finished" variant="success">Finished</b-badge>
        <b-badge v-else-if="item.stepsDone > 0" variant="warning"
          >Active</b-badge
        >
        <b-badge v-else variant="secondary">Pending</b-badge>
        <p v-if="item.finished == false">
          Waiting for {{ item.currentStep.sensorName }} to become
          {{ item.currentStep.expectedValue }}
        </p>
        <b-collapse id="collapse-1" class="mt-2">
          <b-card>
            <b-list-group v-for="step in item.steps" :key="step.counter">
              <b-list-group-item
                >{{ step.sensorName }} = &gt;{{ step.result }}&lt; ( expected:
                {{ step.expectedValue }} )</b-list-group-item
              >
            </b-list-group>
          </b-card>
        </b-collapse>
        <b-card>
          {{ item.whendone }}
        </b-card>
      </b-card-text>
    </b-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SingleRun',
  props: ['bus'],
  data() {
    return {
      runid: '',
      count: 0,
      test: 0,
      message: 'TT',
      metrics: null,
    };
  },
  methods: {
    runChanged(data) {
      console.info('SingleRun runChanged');
      this.runid = data;
      this.getMessage();
    },
    getMessage() {
      const path = `http://localhost:5000/getRunData/${this.runid}`;
      if (this.runid !== '') {
        axios
          .get(path)
          .then((res) => {
            // eslint-disable-next-line
            // console.error(res.data);
            this.metrics = res.data;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      }
    },
  },
  mounted() {
    console.error('SingleRun mounted');
    this.bus.$on('submit', this.getMessage);
    this.bus.$on('runChanged', this.runChanged);
  },
};
</script>

<style lang="scss" scoped></style>
