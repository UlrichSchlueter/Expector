/* eslint-disable object-curly-newline */
<template>
  <Moveable
    class="moveable"
    v-bind="moveable"
    @drag="handleDrag"
    @resize="handleResize"
    @scale="handleScale"
    @rotate="handleRotate"
    @warp="handleWarp"
    @pinch="handlePinch"
  >
    <span>Vue Moveable</span>
  </Moveable>
</template>
<script>
import Moveable from 'vue-moveable';

export default {
  name: 'app',
  components: {
    Moveable,
  },
  data: () => ({
    moveable: {
      draggable: true,
      throttleDrag: 0,
      resizable: false,
      throttleResize: 1,
      keepRatio: false,
      scalable: true,
      throttleScale: 0,
      rotatable: true,
      throttleRotate: 0,
      pinchable: true, // ["draggable", "resizable", "scalable", "rotatable"]
      origin: false,
    },
  }),
  methods: {
    handleDrag({ target, transform }) {
      console.log('onDrag left, top', transform);
      // eslint-disable-next-line no-param-reassign
      target.style.transform = transform;
    },
    // eslint-disable-next-line object-curly-newline
    handleResize({ target, width, height, delta }) {
      console.log('onResize', width, height);
      // eslint-disable-next-line no-param-reassign, no-unused-expressions
      delta[0] && (target.style.width = `${width}px`);
      // eslint-disable-next-line no-param-reassign, no-unused-expressions
      delta[1] && (target.style.height = `${height}px`);
    },
    handleScale({ target, transform, scale }) {
      console.log('onScale scale', scale);
      // eslint-disable-next-line no-param-reassign, no-unused-expressions
      target.style.transform = transform;
    },
    handleRotate({ target, dist, transform }) {
      console.log('onRotate', dist);
      // eslint-disable-next-line no-param-reassign, no-unused-expressions
      target.style.transform = transform;
    },
    handleWarp({ target, transform }) {
      console.log('onWarp', transform);
      // eslint-disable-next-line no-param-reassign, no-unused-expressions
      target.style.transform = transform;
    },
    handlePinch({ target }) {
      console.log('onPinch', target);
    },
  },
};
</script>
