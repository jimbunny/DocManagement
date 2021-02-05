<template>
  <div :class="className">
    <div v-for="n in lines" :key="n" :class="`${className}__line`" />
  </div>
</template>

<script>
export default {
  name: "keel-text",
  data() {
    return {
      className: "vue-keel-text",
    };
  },
  props: {
    lines: {
      type: Number,
      default: 4,
    },
  },
};
</script>
