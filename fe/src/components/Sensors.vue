<template>
  <div class="border">
    <ul id="example-1">
      <li v-for="item in sensors" :key="item.sensors">
        {{ item }}
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
