<template>
  <b-tab :title="purpose" :disabled="disabled">
    <div class="border">
      <b-list-group>
        <b-list-group-item
          v-for="item in metrics"
          :key="item.metrics"
          button
          v-on:click="triggerMe(item.name)"
        >
          {{ item.name }} {{ item.state }} {{ item.metrices }}
        </b-list-group-item>
      </b-list-group>
    </div>
  </b-tab>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Runs',
  props: ['bus', 'purpose'],
  data() {
    return {
      count: 0,
      test: 0,
      message: 'TT',
      metrics: null,
      disabled: false,
      selected: null,
    };
  },
  methods: {
    triggerMe(itemName) {
      // eslint-disable-next-line no-console
      console.error(`Hello from Runs ${itemName}`);
      this.bus.$emit('runChanged', itemName);
    },
    getMessage() {
      const path = `http://localhost:5000/getRuns/${this.purpose}`;
      axios
        .get(path)
        .then((res) => {
          // eslint-disable-next-line
          //Ccnsole.error(res);
          this.metrics = res.data;
          if (Object.entries(res.data).length > 0) {
            this.disabled = false;
          } else {
            this.disabled = true;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  mounted() {
    this.bus.$on('submit', this.getMessage);
  },
};
</script>

<style lang="scss" scoped></style>
