<template>
  <div class="border">
    <div>
      <b-form-select v-model="selected" :options="options"></b-form-select>
      <div class="mt-3">
        Selected: <strong>{{ selected }}</strong>
      </div>
    </div>
    <b-button v-on:click="startTask">>Go</b-button>
    Status: {{ status }}
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selected: null,
      status: 'WAIT',
      options: [
        { value: null, text: '---select----' },
        { value: 'expectorfile.simple', text: 'Simple' },
        { value: 'expectorfile', text: 'Full' },
      ],
    };
  },
  methods: {
    startTask() {
      const path = `http://localhost:5000/startTask/${this.selected}`;
      this.status = 'Starting';
      axios
        .get(path)
        .then((res) => {
          this.status = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  mounted() {
    // eslint-disable-next-line
    console.error(this.message);
  },
};
</script>

<style lang="scss" scoped></style>
