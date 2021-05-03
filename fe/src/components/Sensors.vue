<template>
  <div class="border">
    <h2>Active Sensors</h2>
    <ul id="sensors">
      <li v-for="(evalue, ekey) in sensors" :key="ekey">
        {{ ekey }}:
        <p v-for="(value, key) in evalue" :key="key">
          {{ key }} : Last result={{ value }}
        </p>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Sensors',
  props: ['bus'],
  data() {
    return {
      count: 0,
      test: 0,
      message: 'TT',
      sensors: null,
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/getSensors';
      axios
        .get(path)
        .then((res) => {
          // eslint-disable-next-line
          //console.error(res);
          this.sensors = res.data;
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
