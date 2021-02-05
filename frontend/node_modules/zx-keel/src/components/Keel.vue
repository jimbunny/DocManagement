<template>
  <div :class="classObject">
    <slot />
  </div>
</template>

<script>
export default {
  props: {
    rounded: {
      type: Boolean,
      default: false,
    },
    centered: {
      type: Boolean,
      default: false,
    },
    animated: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    classObject() {
      return {
        "vue-keel": true,
        "vue-keel-is-rounded": this.rounded,
        "vue-keel-is-centered": this.centered,
        "vue-keel-is-animated": this.animated,
      };
    },
  },
};
</script>

<style lang="scss">
@import "../styles/keel.scss";
</style>
