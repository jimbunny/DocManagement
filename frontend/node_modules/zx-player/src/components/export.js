import Mp4 from "./Mp4";
import Hls from "./Hls";
import Flv from "./Flv";
import Custom from "./Custom";
export { Mp4, Hls, Flv, Custom };
if (typeof window !== "undefined" && window.Vue) {
  window.Vue.component("zx-player-mp4", Mp4);
  window.Vue.component("zx-player-hls", Hls);
  window.Vue.component("zx-player-flv", Flv);
  window.Vue.component("zx-player-custom", Custom);
}
