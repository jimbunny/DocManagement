import Keel from "./Keel";
import Heading from "./KeelHeading";
import Img from "./KeelImg";
import Text from "./KeelText";
export { Keel, Heading, Img, Text };
if (typeof window !== "undefined" && window.Vue) {
  window.Vue.component("zx-keel", Keel);
  window.Vue.component("zx-keel-heading", Heading);
  window.Vue.component("zx-keel-img", Img);
  window.Vue.component("zx-keel-text", Text);
}
