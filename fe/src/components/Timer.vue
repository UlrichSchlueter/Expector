<template>
  <div class="border">Timer {{ message }}</div>
</template>

<script>
import $bus from '../event';

export default {
  name: 'Timer',
  data() {
    return {
      count: 0,
      test: 0,
      message: 'TT',
    };
  },
  methods: {
    testFunction() {
      const v = this;
      setInterval(() => {
        v.test += 1;
        v.message = `Hi Vue!${v.test}`;
        v.$emit('testEvent');
        $bus.trigger('testEvent2', 'data');
      }, 3000);
    },
  },
  mounted() {
    // eslint-disable-next-line
    console.error(this.message);
    this.testFunction();
  },
};
</script>

<style lang="scss" scoped></style>
