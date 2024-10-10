var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });
var __commonJS = (cb, mod) => function __require() {
  return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));

// node_modules/.pnpm/@monet-color+quantize@0.0.1-alpha.1/node_modules/@monet-color/quantize/utils/math.js
var require_math = __commonJS({
  "node_modules/.pnpm/@monet-color+quantize@0.0.1-alpha.1/node_modules/@monet-color/quantize/utils/math.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.toRadians = exports.toDegrees = exports.sanitizeDegrees = exports.differenceDegrees = exports.lerp = exports.clamp = exports.signum = void 0;
    function signum(input) {
      if (input < 0) {
        return -1;
      } else if (input === 0) {
        return 0;
      } else {
        return 1;
      }
    }
    __name(signum, "signum");
    exports.signum = signum;
    function clamp(min, max, input) {
      return Math.min(Math.max(input, min), max);
    }
    __name(clamp, "clamp");
    exports.clamp = clamp;
    function lerp(start, stop, amount) {
      return (1 - amount) * start + amount * stop;
    }
    __name(lerp, "lerp");
    exports.lerp = lerp;
    function differenceDegrees(a, b) {
      return 180 - Math.abs(Math.abs(a - b) - 180);
    }
    __name(differenceDegrees, "differenceDegrees");
    exports.differenceDegrees = differenceDegrees;
    function sanitizeDegrees(degrees) {
      if (degrees < 0) {
        return degrees % 360 + 360;
      } else if (degrees >= 360) {
        return degrees % 360;
      } else {
        return degrees;
      }
    }
    __name(sanitizeDegrees, "sanitizeDegrees");
    exports.sanitizeDegrees = sanitizeDegrees;
    function toDegrees(radians) {
      return radians * 180 / Math.PI;
    }
    __name(toDegrees, "toDegrees");
    exports.toDegrees = toDegrees;
    function toRadians(degrees) {
      return degrees / 180 * Math.PI;
    }
    __name(toRadians, "toRadians");
    exports.toRadians = toRadians;
  }
});

// node_modules/.pnpm/@monet-color+quantize@0.0.1-alpha.1/node_modules/@monet-color/quantize/utils/color.js
var require_color = __commonJS({
  "node_modules/.pnpm/@monet-color+quantize@0.0.1-alpha.1/node_modules/@monet-color/quantize/utils/color.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.delinearized = exports.linearized = exports.yFromLstar = exports.intFromLstar = exports.intFromHex = exports.intFromXyz = exports.intFromXyzComponents = exports.intFromLab = exports.labFromInt = exports.intFromRgb = exports.xyzFromInt = exports.hexFromInt = exports.lstarFromInt = exports.blueFromInt = exports.greenFromInt = exports.redFromInt = exports.alphaFromInt = exports.WHITE_POINT_D65 = void 0;
    var math = require_math();
    exports.WHITE_POINT_D65 = [95.047, 100, 108.883];
    var alphaFromInt = /* @__PURE__ */ __name((argb) => {
      return (argb & 4278190080) >> 24 >>> 0;
    }, "alphaFromInt");
    exports.alphaFromInt = alphaFromInt;
    var redFromInt = /* @__PURE__ */ __name((argb) => {
      return (argb & 16711680) >> 16;
    }, "redFromInt");
    exports.redFromInt = redFromInt;
    var greenFromInt = /* @__PURE__ */ __name((argb) => {
      return (argb & 65280) >> 8;
    }, "greenFromInt");
    exports.greenFromInt = greenFromInt;
    var blueFromInt = /* @__PURE__ */ __name((argb) => {
      return argb & 255;
    }, "blueFromInt");
    exports.blueFromInt = blueFromInt;
    var lstarFromInt = /* @__PURE__ */ __name((argb) => {
      const red = (argb & 16711680) >> 16;
      const green = (argb & 65280) >> 8;
      const blue = argb & 255;
      const redL = (0, exports.linearized)(red / 255) * 100;
      const greenL = (0, exports.linearized)(green / 255) * 100;
      const blueL = (0, exports.linearized)(blue / 255) * 100;
      let y = 0.2126 * redL + 0.7152 * greenL + 0.0722 * blueL;
      y = y / 100;
      const e = 216 / 24389;
      let yIntermediate;
      if (y <= e) {
        yIntermediate = 24389 / 27 * y;
        return yIntermediate;
      } else {
        yIntermediate = Math.pow(y, 1 / 3);
      }
      return 116 * yIntermediate - 16;
    }, "lstarFromInt");
    exports.lstarFromInt = lstarFromInt;
    var hexFromInt = /* @__PURE__ */ __name((argb) => {
      const r = (0, exports.redFromInt)(argb);
      const g = (0, exports.greenFromInt)(argb);
      const b = (0, exports.blueFromInt)(argb);
      const outParts = [r.toString(16), g.toString(16), b.toString(16)];
      for (const [i, part] of outParts.entries()) {
        if (part.length === 1) {
          outParts[i] = "0" + part;
        }
      }
      return "#" + outParts.join("");
    }, "hexFromInt");
    exports.hexFromInt = hexFromInt;
    var xyzFromInt = /* @__PURE__ */ __name((argb) => {
      const red = (argb & 16711680) >> 16;
      const green = (argb & 65280) >> 8;
      const blue = argb & 255;
      const redL = (0, exports.linearized)(red / 255) * 100;
      const greenL = (0, exports.linearized)(green / 255) * 100;
      const blueL = (0, exports.linearized)(blue / 255) * 100;
      const x = 0.41233895 * redL + 0.35762064 * greenL + 0.18051042 * blueL;
      const y = 0.2126 * redL + 0.7152 * greenL + 0.0722 * blueL;
      const z = 0.01932141 * redL + 0.11916382 * greenL + 0.95034478 * blueL;
      return [x, y, z];
    }, "xyzFromInt");
    exports.xyzFromInt = xyzFromInt;
    var intFromRgb = /* @__PURE__ */ __name((rgb) => {
      return (255 << 24 | (rgb[0] & 255) << 16 | (rgb[1] & 255) << 8 | rgb[2] & 255) >>> 0;
    }, "intFromRgb");
    exports.intFromRgb = intFromRgb;
    var labFromInt = /* @__PURE__ */ __name((argb) => {
      const e = 216 / 24389;
      const kappa = 24389 / 27;
      const red = (argb & 16711680) >> 16;
      const green = (argb & 65280) >> 8;
      const blue = argb & 255;
      const redL = (0, exports.linearized)(red / 255) * 100;
      const greenL = (0, exports.linearized)(green / 255) * 100;
      const blueL = (0, exports.linearized)(blue / 255) * 100;
      const x = 0.41233895 * redL + 0.35762064 * greenL + 0.18051042 * blueL;
      const y = 0.2126 * redL + 0.7152 * greenL + 0.0722 * blueL;
      const z = 0.01932141 * redL + 0.11916382 * greenL + 0.95034478 * blueL;
      const yNormalized = y / exports.WHITE_POINT_D65[1];
      let fy;
      if (yNormalized > e) {
        fy = Math.pow(yNormalized, 1 / 3);
      } else {
        fy = (kappa * yNormalized + 16) / 116;
      }
      const xNormalized = x / exports.WHITE_POINT_D65[0];
      let fx;
      if (xNormalized > e) {
        fx = Math.pow(xNormalized, 1 / 3);
      } else {
        fx = (kappa * xNormalized + 16) / 116;
      }
      const zNormalized = z / exports.WHITE_POINT_D65[2];
      let fz;
      if (zNormalized > e) {
        fz = Math.pow(zNormalized, 1 / 3);
      } else {
        fz = (kappa * zNormalized + 16) / 116;
      }
      const l = 116 * fy - 16;
      const a = 500 * (fx - fy);
      const b = 200 * (fy - fz);
      return [l, a, b];
    }, "labFromInt");
    exports.labFromInt = labFromInt;
    var intFromLab = /* @__PURE__ */ __name((l, a, b) => {
      const e = 216 / 24389;
      const kappa = 24389 / 27;
      const ke = 8;
      const fy = (l + 16) / 116;
      const fx = a / 500 + fy;
      const fz = fy - b / 200;
      const fx3 = fx * fx * fx;
      const xNormalized = fx3 > e ? fx3 : (116 * fx - 16) / kappa;
      const yNormalized = l > ke ? fy * fy * fy : l / kappa;
      const fz3 = fz * fz * fz;
      const zNormalized = fz3 > e ? fz3 : (116 * fz - 16) / kappa;
      const x = xNormalized * exports.WHITE_POINT_D65[0];
      const y = yNormalized * exports.WHITE_POINT_D65[1];
      const z = zNormalized * exports.WHITE_POINT_D65[2];
      return (0, exports.intFromXyz)([x, y, z]);
    }, "intFromLab");
    exports.intFromLab = intFromLab;
    var intFromXyzComponents = /* @__PURE__ */ __name((x, y, z) => {
      x = x / 100;
      y = y / 100;
      z = z / 100;
      const rL = x * 3.2406 + y * -1.5372 + z * -0.4986;
      const gL = x * -0.9689 + y * 1.8758 + z * 0.0415;
      const bL = x * 0.0557 + y * -0.204 + z * 1.057;
      const r = (0, exports.delinearized)(rL);
      const g = (0, exports.delinearized)(gL);
      const b = (0, exports.delinearized)(bL);
      const rInt = Math.round(math.clamp(0, 255, r * 255));
      const gInt = Math.round(math.clamp(0, 255, g * 255));
      const bInt = Math.round(math.clamp(0, 255, b * 255));
      return (0, exports.intFromRgb)([rInt, gInt, bInt]);
    }, "intFromXyzComponents");
    exports.intFromXyzComponents = intFromXyzComponents;
    var intFromXyz = /* @__PURE__ */ __name((xyz) => {
      return (0, exports.intFromXyzComponents)(xyz[0], xyz[1], xyz[2]);
    }, "intFromXyz");
    exports.intFromXyz = intFromXyz;
    var intFromHex = /* @__PURE__ */ __name((hex) => {
      hex = hex.replace("#", "");
      const isThree = hex.length === 3;
      const isSix = hex.length === 6;
      const isEight = hex.length === 8;
      if (!isThree && !isSix && !isEight) {
        throw new Error("unexpected hex " + hex);
      }
      let r = 0;
      let g = 0;
      let b = 0;
      if (isThree) {
        r = parseIntHex(hex.slice(0, 1).repeat(2));
        g = parseIntHex(hex.slice(1, 2).repeat(2));
        b = parseIntHex(hex.slice(2, 3).repeat(2));
      } else if (isSix) {
        r = parseIntHex(hex.slice(0, 2));
        g = parseIntHex(hex.slice(2, 4));
        b = parseIntHex(hex.slice(4, 6));
      } else if (isEight) {
        r = parseIntHex(hex.slice(2, 4));
        g = parseIntHex(hex.slice(4, 6));
        b = parseIntHex(hex.slice(6, 8));
      }
      return (255 << 24 | (r & 255) << 16 | (g & 255) << 8 | b & 255) >>> 0;
    }, "intFromHex");
    exports.intFromHex = intFromHex;
    function parseIntHex(value) {
      return parseInt(value, 16);
    }
    __name(parseIntHex, "parseIntHex");
    var intFromLstar = /* @__PURE__ */ __name((lstar) => {
      const fy = (lstar + 16) / 116;
      const fz = fy;
      const fx = fy;
      const kappa = 24389 / 27;
      const epsilon = 216 / 24389;
      const cubeExceedEpsilon = fy * fy * fy > epsilon;
      const lExceedsEpsilonKappa = lstar > 8;
      const y = lExceedsEpsilonKappa ? fy * fy * fy : lstar / kappa;
      const x = cubeExceedEpsilon ? fx * fx * fx : (116 * fx - 16) / kappa;
      const z = cubeExceedEpsilon ? fz * fz * fz : (116 * fx - 16) / kappa;
      const xyz = [
        x * exports.WHITE_POINT_D65[0],
        y * exports.WHITE_POINT_D65[1],
        z * exports.WHITE_POINT_D65[2]
      ];
      return (0, exports.intFromXyz)(xyz);
    }, "intFromLstar");
    exports.intFromLstar = intFromLstar;
    var yFromLstar = /* @__PURE__ */ __name((lstar) => {
      const ke = 8;
      if (lstar > ke) {
        return Math.pow((lstar + 16) / 116, 3) * 100;
      } else {
        return lstar / (24389 / 27) * 100;
      }
    }, "yFromLstar");
    exports.yFromLstar = yFromLstar;
    var linearized = /* @__PURE__ */ __name((rgb) => {
      if (rgb <= 0.04045) {
        return rgb / 12.92;
      } else {
        return Math.pow((rgb + 0.055) / 1.055, 2.4);
      }
    }, "linearized");
    exports.linearized = linearized;
    var delinearized = /* @__PURE__ */ __name((rgb) => {
      if (rgb <= 31308e-7) {
        return rgb * 12.92;
      } else {
        return 1.055 * Math.pow(rgb, 1 / 2.4) - 0.055;
      }
    }, "delinearized");
    exports.delinearized = delinearized;
  }
});

// node_modules/.pnpm/@monet-color+quantize@0.0.1-alpha.1/node_modules/@monet-color/quantize/lab_point_provider.js
var require_lab_point_provider = __commonJS({
  "node_modules/.pnpm/@monet-color+quantize@0.0.1-alpha.1/node_modules/@monet-color/quantize/lab_point_provider.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.LabPointProvider = void 0;
    var utils = require_color();
    var LabPointProvider = class {
      static {
        __name(this, "LabPointProvider");
      }
      /**
       * Convert a color represented in ARGB to a 3-element array of L*a*b*
       * coordinates of the color.
       */
      fromInt(argb) {
        return utils.labFromInt(argb);
      }
      /**
       * Convert a 3-element array to a color represented in ARGB.
       */
      toInt(point) {
        return utils.intFromLab(point[0], point[1], point[2]);
      }
      /**
       * Standard CIE 1976 delta E formula also takes the square root, unneeded
       * here. This method is used by quantization algorithms to compare distance,
       * and the relative ordering is the same, with or without a square root.
       *
       * This relatively minor optimization is helpful because this method is
       * called at least once for each pixel in an image.
       */
      distance(from, to) {
        const dL = from[0] - to[0];
        const dA = from[1] - to[1];
        const dB = from[2] - to[2];
        return dL * dL + dA * dA + dB * dB;
      }
    };
    exports.LabPointProvider = LabPointProvider;
  }
});

// node_modules/.pnpm/@monet-color+quantize@0.0.1-alpha.1/node_modules/@monet-color/quantize/quantizer_wsmeans.js
var require_quantizer_wsmeans = __commonJS({
  "node_modules/.pnpm/@monet-color+quantize@0.0.1-alpha.1/node_modules/@monet-color/quantize/quantizer_wsmeans.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.QuantizerWsmeans = void 0;
    var lab_point_provider_1 = require_lab_point_provider();
    var MAX_ITERATIONS = 10;
    var MIN_MOVEMENT_DISTANCE = 3;
    var QuantizerWsmeans = class {
      static {
        __name(this, "QuantizerWsmeans");
      }
      /**
       * @param inputPixels Colors in ARGB format.
       * @param startingClusters Defines the initial state of the quantizer. Passing
       *     an empty array is fine, the implementation will create its own initial
       *     state that leads to reproducible results for the same inputs.
       *     Passing an array that is the result of Wu quantization leads to higher
       *     quality results.
       * @param maxColors The number of colors to divide the image into. A lower
       *     number of colors may be returned.
       * @return Colors in ARGB format.
       */
      static quantize(inputPixels, startingClusters, maxColors) {
        const pixelToCount = /* @__PURE__ */ new Map();
        const points = new Array();
        const pixels = new Array();
        const pointProvider = new lab_point_provider_1.LabPointProvider();
        let pointCount = 0;
        for (let i = 0; i < inputPixels.length; i++) {
          const inputPixel = inputPixels[i];
          const pixelCount = pixelToCount.get(inputPixel);
          if (pixelCount === void 0) {
            pointCount++;
            points.push(pointProvider.fromInt(inputPixel));
            pixels.push(inputPixel);
            pixelToCount.set(inputPixel, 1);
          } else {
            pixelToCount.set(inputPixel, pixelCount + 1);
          }
        }
        const counts = new Array();
        for (let i = 0; i < pointCount; i++) {
          const pixel = pixels[i];
          const count = pixelToCount.get(pixel);
          if (count !== void 0) {
            counts[i] = count;
          }
        }
        let clusterCount = Math.min(maxColors, pointCount);
        if (startingClusters.length > 0) {
          clusterCount = Math.min(clusterCount, startingClusters.length);
        }
        const clusters = new Array();
        for (let i = 0; i < startingClusters.length; i++) {
          clusters.push(pointProvider.fromInt(startingClusters[i]));
        }
        const additionalClustersNeeded = clusterCount - clusters.length;
        if (startingClusters.length === 0 && additionalClustersNeeded > 0) {
          for (let i = 0; i < additionalClustersNeeded; i++) {
            const l = Math.random() * 100;
            const a = Math.random() * (100 - -100 + 1) + -100;
            const b = Math.random() * (100 - -100 + 1) + -100;
            clusters.push([l, a, b]);
          }
        }
        const clusterIndices = new Array();
        for (let i = 0; i < pointCount; i++) {
          clusterIndices.push(Math.floor(Math.random() * clusterCount));
        }
        const indexMatrix = new Array();
        for (let i = 0; i < clusterCount; i++) {
          indexMatrix.push(new Array());
          for (let j = 0; j < clusterCount; j++) {
            indexMatrix[i].push(0);
          }
        }
        const distanceToIndexMatrix = new Array();
        for (let i = 0; i < clusterCount; i++) {
          distanceToIndexMatrix.push(new Array());
          for (let j = 0; j < clusterCount; j++) {
            distanceToIndexMatrix[i].push(new DistanceAndIndex());
          }
        }
        const pixelCountSums = new Array();
        for (let i = 0; i < clusterCount; i++) {
          pixelCountSums.push(0);
        }
        for (let iteration = 0; iteration < MAX_ITERATIONS; iteration++) {
          for (let i = 0; i < clusterCount; i++) {
            for (let j = i + 1; j < clusterCount; j++) {
              const distance = pointProvider.distance(clusters[i], clusters[j]);
              distanceToIndexMatrix[j][i].distance = distance;
              distanceToIndexMatrix[j][i].index = i;
              distanceToIndexMatrix[i][j].distance = distance;
              distanceToIndexMatrix[i][j].index = j;
            }
            distanceToIndexMatrix[i].sort();
            for (let j = 0; j < clusterCount; j++) {
              indexMatrix[i][j] = distanceToIndexMatrix[i][j].index;
            }
          }
          let pointsMoved = 0;
          for (let i = 0; i < pointCount; i++) {
            const point = points[i];
            const previousClusterIndex = clusterIndices[i];
            const previousCluster = clusters[previousClusterIndex];
            const previousDistance = pointProvider.distance(point, previousCluster);
            let minimumDistance = previousDistance;
            let newClusterIndex = -1;
            for (let j = 0; j < clusterCount; j++) {
              if (distanceToIndexMatrix[previousClusterIndex][j].distance >= 4 * previousDistance) {
                continue;
              }
              const distance = pointProvider.distance(point, clusters[j]);
              if (distance < minimumDistance) {
                minimumDistance = distance;
                newClusterIndex = j;
              }
            }
            if (newClusterIndex !== -1) {
              const distanceChange = Math.abs(Math.sqrt(minimumDistance) - Math.sqrt(previousDistance));
              if (distanceChange > MIN_MOVEMENT_DISTANCE) {
                pointsMoved++;
                clusterIndices[i] = newClusterIndex;
              }
            }
          }
          if (pointsMoved === 0 && iteration !== 0) {
            break;
          }
          const componentASums = new Array(clusterCount).fill(0);
          const componentBSums = new Array(clusterCount).fill(0);
          const componentCSums = new Array(clusterCount).fill(0);
          for (let i = 0; i < clusterCount; i++) {
            pixelCountSums[i] = 0;
          }
          for (let i = 0; i < pointCount; i++) {
            const clusterIndex = clusterIndices[i];
            const point = points[i];
            const count = counts[i];
            pixelCountSums[clusterIndex] += count;
            componentASums[clusterIndex] += point[0] * count;
            componentBSums[clusterIndex] += point[1] * count;
            componentCSums[clusterIndex] += point[2] * count;
          }
          for (let i = 0; i < clusterCount; i++) {
            const count = pixelCountSums[i];
            if (count === 0) {
              clusters[i] = [0, 0, 0];
              continue;
            }
            const a = componentASums[i] / count;
            const b = componentBSums[i] / count;
            const c = componentCSums[i] / count;
            clusters[i] = [a, b, c];
          }
        }
        const argbToPopulation = /* @__PURE__ */ new Map();
        for (let i = 0; i < clusterCount; i++) {
          const count = pixelCountSums[i];
          if (count === 0) {
            continue;
          }
          const possibleNewCluster = pointProvider.toInt(clusters[i]);
          if (argbToPopulation.has(possibleNewCluster)) {
            continue;
          }
          argbToPopulation.set(possibleNewCluster, count);
        }
        return argbToPopulation;
      }
    };
    exports.QuantizerWsmeans = QuantizerWsmeans;
    var DistanceAndIndex = class {
      static {
        __name(this, "DistanceAndIndex");
      }
      constructor() {
        this.distance = -1;
        this.index = -1;
      }
    };
  }
});

// node_modules/.pnpm/@monet-color+quantize@0.0.1-alpha.1/node_modules/@monet-color/quantize/quantizer_map.js
var require_quantizer_map = __commonJS({
  "node_modules/.pnpm/@monet-color+quantize@0.0.1-alpha.1/node_modules/@monet-color/quantize/quantizer_map.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.QuantizerMap = void 0;
    var utils = require_color();
    var QuantizerMap = class {
      static {
        __name(this, "QuantizerMap");
      }
      /**
       * @param pixels Colors in ARGB format.
       * @return A Map with keys of ARGB colors, and values of the number of times
       *     the color appears in the image.
       */
      static quantize(pixels) {
        var _a;
        const countByColor = /* @__PURE__ */ new Map();
        for (let i = 0; i < pixels.length; i++) {
          const pixel = pixels[i];
          const alpha = utils.alphaFromInt(pixel);
          if (alpha < 255) {
            continue;
          }
          countByColor.set(pixel, ((_a = countByColor.get(pixel)) !== null && _a !== void 0 ? _a : 0) + 1);
        }
        return countByColor;
      }
    };
    exports.QuantizerMap = QuantizerMap;
  }
});

// node_modules/.pnpm/@monet-color+quantize@0.0.1-alpha.1/node_modules/@monet-color/quantize/quantizer_wu.js
var require_quantizer_wu = __commonJS({
  "node_modules/.pnpm/@monet-color+quantize@0.0.1-alpha.1/node_modules/@monet-color/quantize/quantizer_wu.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.QuantizerWu = void 0;
    var utils = require_color();
    var quantizer_map_1 = require_quantizer_map();
    var INDEX_BITS = 5;
    var SIDE_LENGTH = 33;
    var TOTAL_SIZE = 35937;
    var directions = {
      RED: "red",
      GREEN: "green",
      BLUE: "blue"
    };
    var QuantizerWu = class {
      static {
        __name(this, "QuantizerWu");
      }
      constructor(weights = [], momentsR = [], momentsG = [], momentsB = [], moments = [], cubes = []) {
        this.weights = weights;
        this.momentsR = momentsR;
        this.momentsG = momentsG;
        this.momentsB = momentsB;
        this.moments = moments;
        this.cubes = cubes;
      }
      /**
       * @param pixels Colors in ARGB format.
       * @param maxColors The number of colors to divide the image into. A lower
       *     number of colors may be returned.
       * @return Colors in ARGB format.
       */
      quantize(pixels, maxColors) {
        this.constructHistogram(pixels);
        this.computeMoments();
        const createBoxesResult = this.createBoxes(maxColors);
        const results = this.createResult(createBoxesResult.resultCount);
        return results;
      }
      constructHistogram(pixels) {
        var _a;
        this.weights = Array.from({ length: TOTAL_SIZE }).fill(0);
        this.momentsR = Array.from({ length: TOTAL_SIZE }).fill(0);
        this.momentsG = Array.from({ length: TOTAL_SIZE }).fill(0);
        this.momentsB = Array.from({ length: TOTAL_SIZE }).fill(0);
        this.moments = Array.from({ length: TOTAL_SIZE }).fill(0);
        const countByColor = quantizer_map_1.QuantizerMap.quantize(pixels);
        for (const [pixel, count] of countByColor.entries()) {
          const red = utils.redFromInt(pixel);
          const green = utils.greenFromInt(pixel);
          const blue = utils.blueFromInt(pixel);
          const bitsToRemove = 8 - INDEX_BITS;
          const iR = (red >> bitsToRemove) + 1;
          const iG = (green >> bitsToRemove) + 1;
          const iB = (blue >> bitsToRemove) + 1;
          const index = this.getIndex(iR, iG, iB);
          this.weights[index] = ((_a = this.weights[index]) !== null && _a !== void 0 ? _a : 0) + count;
          this.momentsR[index] += count * red;
          this.momentsG[index] += count * green;
          this.momentsB[index] += count * blue;
          this.moments[index] += count * (red * red + green * green + blue * blue);
        }
      }
      computeMoments() {
        for (let r = 1; r < SIDE_LENGTH; r++) {
          const area = Array.from({ length: SIDE_LENGTH }).fill(0);
          const areaR = Array.from({ length: SIDE_LENGTH }).fill(0);
          const areaG = Array.from({ length: SIDE_LENGTH }).fill(0);
          const areaB = Array.from({ length: SIDE_LENGTH }).fill(0);
          const area2 = Array.from({ length: SIDE_LENGTH }).fill(0);
          for (let g = 1; g < SIDE_LENGTH; g++) {
            let line = 0;
            let lineR = 0;
            let lineG = 0;
            let lineB = 0;
            let line2 = 0;
            for (let b = 1; b < SIDE_LENGTH; b++) {
              const index = this.getIndex(r, g, b);
              line += this.weights[index];
              lineR += this.momentsR[index];
              lineG += this.momentsG[index];
              lineB += this.momentsB[index];
              line2 += this.moments[index];
              area[b] += line;
              areaR[b] += lineR;
              areaG[b] += lineG;
              areaB[b] += lineB;
              area2[b] += line2;
              const previousIndex = this.getIndex(r - 1, g, b);
              this.weights[index] = this.weights[previousIndex] + area[b];
              this.momentsR[index] = this.momentsR[previousIndex] + areaR[b];
              this.momentsG[index] = this.momentsG[previousIndex] + areaG[b];
              this.momentsB[index] = this.momentsB[previousIndex] + areaB[b];
              this.moments[index] = this.moments[previousIndex] + area2[b];
            }
          }
        }
      }
      createBoxes(maxColors) {
        this.cubes = Array.from({ length: maxColors }).fill(0).map(() => new Box());
        const volumeVariance = Array.from({ length: maxColors }).fill(0);
        this.cubes[0].r0 = 0;
        this.cubes[0].g0 = 0;
        this.cubes[0].b0 = 0;
        this.cubes[0].r1 = SIDE_LENGTH - 1;
        this.cubes[0].g1 = SIDE_LENGTH - 1;
        this.cubes[0].b1 = SIDE_LENGTH - 1;
        let generatedColorCount = maxColors;
        let next = 0;
        for (let i = 1; i < maxColors; i++) {
          if (this.cut(this.cubes[next], this.cubes[i])) {
            volumeVariance[next] = this.cubes[next].vol > 1 ? this.variance(this.cubes[next]) : 0;
            volumeVariance[i] = this.cubes[i].vol > 1 ? this.variance(this.cubes[i]) : 0;
          } else {
            volumeVariance[next] = 0;
            i--;
          }
          next = 0;
          let temp = volumeVariance[0];
          for (let j = 1; j <= i; j++) {
            if (volumeVariance[j] > temp) {
              temp = volumeVariance[j];
              next = j;
            }
          }
          if (temp <= 0) {
            generatedColorCount = i + 1;
            break;
          }
        }
        return new CreateBoxesResult(maxColors, generatedColorCount);
      }
      createResult(colorCount) {
        const colors = [];
        for (let i = 0; i < colorCount; ++i) {
          const cube = this.cubes[i];
          const weight = this.volume(cube, this.weights);
          if (weight > 0) {
            const r = Math.round(this.volume(cube, this.momentsR) / weight);
            const g = Math.round(this.volume(cube, this.momentsG) / weight);
            const b = Math.round(this.volume(cube, this.momentsB) / weight);
            const color = 255 << 24 | (r & 255) << 16 | (g & 255) << 8 | b & 255;
            colors.push(color);
          }
        }
        return colors;
      }
      variance(cube) {
        const dr = this.volume(cube, this.momentsR);
        const dg = this.volume(cube, this.momentsG);
        const db = this.volume(cube, this.momentsB);
        const xx = this.moments[this.getIndex(cube.r1, cube.g1, cube.b1)] - this.moments[this.getIndex(cube.r1, cube.g1, cube.b0)] - this.moments[this.getIndex(cube.r1, cube.g0, cube.b1)] + this.moments[this.getIndex(cube.r1, cube.g0, cube.b0)] - this.moments[this.getIndex(cube.r0, cube.g1, cube.b1)] + this.moments[this.getIndex(cube.r0, cube.g1, cube.b0)] + this.moments[this.getIndex(cube.r0, cube.g0, cube.b1)] - this.moments[this.getIndex(cube.r0, cube.g0, cube.b0)];
        const hypotenuse = dr * dr + dg * dg + db * db;
        const volume = this.volume(cube, this.weights);
        return xx - hypotenuse / volume;
      }
      cut(one, two) {
        const wholeR = this.volume(one, this.momentsR);
        const wholeG = this.volume(one, this.momentsG);
        const wholeB = this.volume(one, this.momentsB);
        const wholeW = this.volume(one, this.weights);
        const maxRResult = this.maximize(one, directions.RED, one.r0 + 1, one.r1, wholeR, wholeG, wholeB, wholeW);
        const maxGResult = this.maximize(one, directions.GREEN, one.g0 + 1, one.g1, wholeR, wholeG, wholeB, wholeW);
        const maxBResult = this.maximize(one, directions.BLUE, one.b0 + 1, one.b1, wholeR, wholeG, wholeB, wholeW);
        let direction;
        const maxR = maxRResult.maximum;
        const maxG = maxGResult.maximum;
        const maxB = maxBResult.maximum;
        if (maxR >= maxG && maxR >= maxB) {
          if (maxRResult.cutLocation < 0) {
            return false;
          }
          direction = directions.RED;
        } else if (maxG >= maxR && maxG >= maxB) {
          direction = directions.GREEN;
        } else {
          direction = directions.BLUE;
        }
        two.r1 = one.r1;
        two.g1 = one.g1;
        two.b1 = one.b1;
        switch (direction) {
          case directions.RED:
            one.r1 = maxRResult.cutLocation;
            two.r0 = one.r1;
            two.g0 = one.g0;
            two.b0 = one.b0;
            break;
          case directions.GREEN:
            one.g1 = maxGResult.cutLocation;
            two.r0 = one.r0;
            two.g0 = one.g1;
            two.b0 = one.b0;
            break;
          case directions.BLUE:
            one.b1 = maxBResult.cutLocation;
            two.r0 = one.r0;
            two.g0 = one.g0;
            two.b0 = one.b1;
            break;
          default:
            throw new Error("unexpected direction " + direction);
        }
        one.vol = (one.r1 - one.r0) * (one.g1 - one.g0) * (one.b1 - one.b0);
        two.vol = (two.r1 - two.r0) * (two.g1 - two.g0) * (two.b1 - two.b0);
        return true;
      }
      maximize(cube, direction, first, last, wholeR, wholeG, wholeB, wholeW) {
        const bottomR = this.bottom(cube, direction, this.momentsR);
        const bottomG = this.bottom(cube, direction, this.momentsG);
        const bottomB = this.bottom(cube, direction, this.momentsB);
        const bottomW = this.bottom(cube, direction, this.weights);
        let max = 0;
        let cut = -1;
        let halfR = 0;
        let halfG = 0;
        let halfB = 0;
        let halfW = 0;
        for (let i = first; i < last; i++) {
          halfR = bottomR + this.top(cube, direction, i, this.momentsR);
          halfG = bottomG + this.top(cube, direction, i, this.momentsG);
          halfB = bottomB + this.top(cube, direction, i, this.momentsB);
          halfW = bottomW + this.top(cube, direction, i, this.weights);
          if (halfW === 0) {
            continue;
          }
          let tempNumerator = (halfR * halfR + halfG * halfG + halfB * halfB) * 1;
          let tempDenominator = halfW * 1;
          let temp = tempNumerator / tempDenominator;
          halfR = wholeR - halfR;
          halfG = wholeG - halfG;
          halfB = wholeB - halfB;
          halfW = wholeW - halfW;
          if (halfW === 0) {
            continue;
          }
          tempNumerator = (halfR * halfR + halfG * halfG + halfB * halfB) * 1;
          tempDenominator = halfW * 1;
          temp += tempNumerator / tempDenominator;
          if (temp > max) {
            max = temp;
            cut = i;
          }
        }
        return new MaximizeResult(cut, max);
      }
      volume(cube, moment) {
        return moment[this.getIndex(cube.r1, cube.g1, cube.b1)] - moment[this.getIndex(cube.r1, cube.g1, cube.b0)] - moment[this.getIndex(cube.r1, cube.g0, cube.b1)] + moment[this.getIndex(cube.r1, cube.g0, cube.b0)] - moment[this.getIndex(cube.r0, cube.g1, cube.b1)] + moment[this.getIndex(cube.r0, cube.g1, cube.b0)] + moment[this.getIndex(cube.r0, cube.g0, cube.b1)] - moment[this.getIndex(cube.r0, cube.g0, cube.b0)];
      }
      bottom(cube, direction, moment) {
        switch (direction) {
          case directions.RED:
            return -moment[this.getIndex(cube.r0, cube.g1, cube.b1)] + moment[this.getIndex(cube.r0, cube.g1, cube.b0)] + moment[this.getIndex(cube.r0, cube.g0, cube.b1)] - moment[this.getIndex(cube.r0, cube.g0, cube.b0)];
          case directions.GREEN:
            return -moment[this.getIndex(cube.r1, cube.g0, cube.b1)] + moment[this.getIndex(cube.r1, cube.g0, cube.b0)] + moment[this.getIndex(cube.r0, cube.g0, cube.b1)] - moment[this.getIndex(cube.r0, cube.g0, cube.b0)];
          case directions.BLUE:
            return -moment[this.getIndex(cube.r1, cube.g1, cube.b0)] + moment[this.getIndex(cube.r1, cube.g0, cube.b0)] + moment[this.getIndex(cube.r0, cube.g1, cube.b0)] - moment[this.getIndex(cube.r0, cube.g0, cube.b0)];
          default:
            throw new Error("unexpected direction $direction");
        }
      }
      top(cube, direction, position, moment) {
        switch (direction) {
          case directions.RED:
            return moment[this.getIndex(position, cube.g1, cube.b1)] - moment[this.getIndex(position, cube.g1, cube.b0)] - moment[this.getIndex(position, cube.g0, cube.b1)] + moment[this.getIndex(position, cube.g0, cube.b0)];
          case directions.GREEN:
            return moment[this.getIndex(cube.r1, position, cube.b1)] - moment[this.getIndex(cube.r1, position, cube.b0)] - moment[this.getIndex(cube.r0, position, cube.b1)] + moment[this.getIndex(cube.r0, position, cube.b0)];
          case directions.BLUE:
            return moment[this.getIndex(cube.r1, cube.g1, position)] - moment[this.getIndex(cube.r1, cube.g0, position)] - moment[this.getIndex(cube.r0, cube.g1, position)] + moment[this.getIndex(cube.r0, cube.g0, position)];
          default:
            throw new Error("unexpected direction $direction");
        }
      }
      getIndex(r, g, b) {
        return (r << INDEX_BITS * 2) + (r << INDEX_BITS + 1) + r + (g << INDEX_BITS) + g + b;
      }
    };
    exports.QuantizerWu = QuantizerWu;
    var Box = class {
      static {
        __name(this, "Box");
      }
      constructor(r0 = 0, r1 = 0, g0 = 0, g1 = 0, b0 = 0, b1 = 0, vol = 0) {
        this.r0 = r0;
        this.r1 = r1;
        this.g0 = g0;
        this.g1 = g1;
        this.b0 = b0;
        this.b1 = b1;
        this.vol = vol;
      }
    };
    var CreateBoxesResult = class {
      static {
        __name(this, "CreateBoxesResult");
      }
      /**
       * @param requestedCount how many colors the caller asked to be returned from
       *     quantization.
       * @param resultCount the actual number of colors achieved from quantization.
       *     May be lower than the requested count.
       */
      constructor(requestedCount, resultCount) {
        this.requestedCount = requestedCount;
        this.resultCount = resultCount;
      }
    };
    var MaximizeResult = class {
      static {
        __name(this, "MaximizeResult");
      }
      constructor(cutLocation, maximum) {
        this.cutLocation = cutLocation;
        this.maximum = maximum;
      }
    };
  }
});

// node_modules/.pnpm/@monet-color+quantize@0.0.1-alpha.1/node_modules/@monet-color/quantize/quantizer_celebi.js
var require_quantizer_celebi = __commonJS({
  "node_modules/.pnpm/@monet-color+quantize@0.0.1-alpha.1/node_modules/@monet-color/quantize/quantizer_celebi.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.QuantizerCelebi = void 0;
    var quantizer_wsmeans_1 = require_quantizer_wsmeans();
    var quantizer_wu_1 = require_quantizer_wu();
    var QuantizerCelebi = class {
      static {
        __name(this, "QuantizerCelebi");
      }
      /**
       * @param pixels - Colors in ARGB format.
       * @param maxColors - The number of colors to divide the image into. A lower
       *     number of colors may be returned.
       * @return Map with keys of colors in ARGB format, and values of number of
       *     pixels in the original image that correspond to the color in the
       *     quantized image.
       */
      static quantize(pixels, maxColors) {
        const wu = new quantizer_wu_1.QuantizerWu();
        const wuResult = wu.quantize(pixels, maxColors);
        return quantizer_wsmeans_1.QuantizerWsmeans.quantize(pixels, wuResult, maxColors);
      }
    };
    exports.QuantizerCelebi = QuantizerCelebi;
  }
});

// node_modules/.pnpm/@monet-color+quantize@0.0.1-alpha.1/node_modules/@monet-color/quantize/index.js
var require_quantize = __commonJS({
  "node_modules/.pnpm/@monet-color+quantize@0.0.1-alpha.1/node_modules/@monet-color/quantize/index.js"(exports) {
    "use strict";
    var __createBinding = exports && exports.__createBinding || (Object.create ? function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      Object.defineProperty(o, k2, { enumerable: true, get: /* @__PURE__ */ __name(function() {
        return m[k];
      }, "get") });
    } : function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      o[k2] = m[k];
    });
    var __exportStar = exports && exports.__exportStar || function(m, exports2) {
      for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports2, p)) __createBinding(exports2, m, p);
    };
    Object.defineProperty(exports, "__esModule", { value: true });
    __exportStar(require_quantizer_celebi(), exports);
  }
});

// node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/gamut/LchGamut.js
var require_LchGamut = __commonJS({
  "node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/gamut/LchGamut.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.LchGamut = exports.ClipMethod = void 0;
    var LinearRgb_1 = require_LinearRgb();
    var ClipMethod;
    (function(ClipMethod2) {
      ClipMethod2[ClipMethod2["PRESERVE_LIGHTNESS"] = 0] = "PRESERVE_LIGHTNESS";
      ClipMethod2[ClipMethod2["PROJECT_TO_MID"] = 1] = "PROJECT_TO_MID";
      ClipMethod2[ClipMethod2["ADAPTIVE_TOWARDS_MID"] = 2] = "ADAPTIVE_TOWARDS_MID";
    })(ClipMethod = exports.ClipMethod || (exports.ClipMethod = {}));
    exports.LchGamut = {
      /** Epsilon for color spaces where lightness ranges from 0 to 100 */
      EPSILON_100: 1e-3,
      evalLine(slope, intercept, x) {
        return slope * x + intercept;
      },
      clip(l1, c1, hue, l0, epsilon, maxLightness, factory) {
        let result = factory.getColor(l1, c1, hue);
        if (result.isInGamut()) {
          return result;
        } else if (l1 <= epsilon) {
          return new LinearRgb_1.LinearSrgb(0, 0, 0);
        } else if (l1 >= maxLightness - epsilon) {
          return new LinearRgb_1.LinearSrgb(1, 1, 1);
        } else {
          const c0 = 0;
          const slope = (l1 - l0) / (c1 - c0);
          const intercept = l0 - slope * c0;
          let lo = 0;
          let hi = c1;
          while (Math.abs(hi - lo) > epsilon) {
            const midC = (lo + hi) / 2;
            const midL = exports.LchGamut.evalLine(slope, intercept, midC);
            result = factory.getColor(midL, midC, hue);
            if (!result.isInGamut()) {
              hi = midC;
            } else {
              const midC2 = midC + epsilon;
              const midL2 = exports.LchGamut.evalLine(slope, intercept, midC2);
              const ptOutside = factory.getColor(midL2, midC2, hue);
              if (ptOutside.isInGamut()) {
                lo = midC;
              } else {
                break;
              }
            }
          }
          return result;
        }
      }
    };
  }
});

// node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/math/index.js
var require_math2 = __commonJS({
  "node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/math/index.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.differenceDegrees = exports.sanitizeDegrees = exports.toDegrees = exports.toRadians = exports.clamp = exports.square = exports.cube = void 0;
    var cube = /* @__PURE__ */ __name((x) => x * x * x, "cube");
    exports.cube = cube;
    var square = /* @__PURE__ */ __name((x) => x * x, "square");
    exports.square = square;
    function clamp(min, input, max) {
      return Math.min(Math.max(min, input), max);
    }
    __name(clamp, "clamp");
    exports.clamp = clamp;
    var toRadians = /* @__PURE__ */ __name((degrees) => degrees * Math.PI / 180, "toRadians");
    exports.toRadians = toRadians;
    var toDegrees = /* @__PURE__ */ __name((radians) => radians * 180 / Math.PI, "toDegrees");
    exports.toDegrees = toDegrees;
    function sanitizeDegrees(degrees) {
      if (degrees < 0) {
        return degrees % 360 + 360;
      } else if (degrees >= 360) {
        return degrees % 360;
      } else {
        return degrees;
      }
    }
    __name(sanitizeDegrees, "sanitizeDegrees");
    exports.sanitizeDegrees = sanitizeDegrees;
    function differenceDegrees(a, b) {
      return 180 - Math.abs(Math.abs(a - b) - 180);
    }
    __name(differenceDegrees, "differenceDegrees");
    exports.differenceDegrees = differenceDegrees;
  }
});

// node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/cam/Zcam.js
var require_Zcam = __commonJS({
  "node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/cam/Zcam.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.Zcam = exports.ChromaSource = exports.LuminanceSource = exports.ViewingConditions = exports.izToQz = exports.hpToEz = exports.xyzToIzazbz = void 0;
    var LchGamut_1 = require_LchGamut();
    var math_1 = require_math2();
    var CieXyzAbs_1 = require_CieXyzAbs();
    var B = 1.15;
    var G = 0.66;
    var C1 = 3424 / 4096;
    var C2 = 2413 / 128;
    var C3 = 2392 / 128;
    var ETA = 2610 / 16384;
    var RHO = 1.7 * 2523 / 32;
    var EPSILON = 37035226210190005e-27;
    function pq(x) {
      const num = C1 - Math.pow(x, 1 / RHO);
      const denom = C3 * Math.pow(x, 1 / RHO) - C2;
      return 1e4 * Math.pow(num / denom, 1 / ETA);
    }
    __name(pq, "pq");
    function pqInv(x) {
      const num = C1 + C2 * Math.pow(x / 1e4, ETA);
      const denom = 1 + C3 * Math.pow(x / 1e4, ETA);
      return Math.pow(num / denom, RHO);
    }
    __name(pqInv, "pqInv");
    function xyzToIzazbz(xyz) {
      const xp = B * xyz.x - (B - 1) * xyz.z;
      const yp = G * xyz.y - (G - 1) * xyz.x;
      const rp = pqInv(0.41478972 * xp + 0.579999 * yp + 0.014648 * xyz.z);
      const gp = pqInv(-0.20151 * xp + 1.120649 * yp + 0.0531008 * xyz.z);
      const bp = pqInv(-0.0166008 * xp + 0.2648 * yp + 0.6684799 * xyz.z);
      const az = 3.524 * rp + -4.066708 * gp + 0.542708 * bp;
      const bz = 0.199076 * rp + 1.096799 * gp + -1.295875 * bp;
      const Iz = gp - EPSILON;
      return [Iz, az, bz];
    }
    __name(xyzToIzazbz, "xyzToIzazbz");
    exports.xyzToIzazbz = xyzToIzazbz;
    var hpToEz = /* @__PURE__ */ __name((hp) => 1.015 + Math.cos((0, math_1.toRadians)(89.038 + hp)), "hpToEz");
    exports.hpToEz = hpToEz;
    var izToQz = /* @__PURE__ */ __name((Iz, cond) => cond.Iz_coeff * Math.pow(Iz, 1.6 * cond.surroundFactor / cond.Qz_denom), "izToQz");
    exports.izToQz = izToQz;
    var ViewingConditions = class {
      static {
        __name(this, "ViewingConditions");
      }
      constructor(surroundFactor, adaptingLuminance, backgroundLuminance, referenceWhite) {
        this.surroundFactor = surroundFactor;
        this.adaptingLuminance = adaptingLuminance;
        this.backgroundLuminance = backgroundLuminance;
        this.referenceWhite = referenceWhite;
        const F_b = Math.sqrt(backgroundLuminance / referenceWhite.y);
        const F_l = 0.171 * Math.cbrt(adaptingLuminance) * (1 - Math.exp(-48 / 9 * adaptingLuminance));
        this.Iz_coeff = 2700 * Math.pow(surroundFactor, 2.2) * Math.sqrt(F_b) * Math.pow(F_l, 0.2);
        this.ez_coeff = Math.pow(F_l, 0.2);
        this.Qz_denom = Math.pow(F_b, 0.12);
        this.Sz_coeff = Math.pow(F_l, 0.6);
        this.Sz_denom = Math.pow(F_l, 1.2);
        const Iz_w = xyzToIzazbz(referenceWhite)[0];
        this.Mz_denom = Math.pow(Iz_w, 0.78) * Math.pow(F_b, 0.1);
        this.Qz_w = (0, exports.izToQz)(Iz_w, this);
      }
    };
    exports.ViewingConditions = ViewingConditions;
    ViewingConditions.SURROUND_DARK = 0.525;
    ViewingConditions.SURROUND_DIM = 0.59;
    ViewingConditions.SURROUND_AVERAGE = 0.69;
    var LuminanceSource;
    (function(LuminanceSource2) {
      LuminanceSource2[LuminanceSource2["BRIGHTNESS"] = 0] = "BRIGHTNESS";
      LuminanceSource2[LuminanceSource2["LIGHTNESS"] = 1] = "LIGHTNESS";
    })(LuminanceSource = exports.LuminanceSource || (exports.LuminanceSource = {}));
    var ChromaSource;
    (function(ChromaSource2) {
      ChromaSource2[ChromaSource2["CHROMA"] = 0] = "CHROMA";
      ChromaSource2[ChromaSource2["COLORFULNESS"] = 1] = "COLORFULNESS";
      ChromaSource2[ChromaSource2["SATURATION"] = 2] = "SATURATION";
      ChromaSource2[ChromaSource2["VIVIDNESS"] = 3] = "VIVIDNESS";
      ChromaSource2[ChromaSource2["BLACKNESS"] = 4] = "BLACKNESS";
      ChromaSource2[ChromaSource2["WHITENESS"] = 5] = "WHITENESS";
    })(ChromaSource = exports.ChromaSource || (exports.ChromaSource = {}));
    var Zcam = class _Zcam {
      static {
        __name(this, "Zcam");
      }
      constructor({ brightness = NaN, lightness = NaN, colorfulness = NaN, chroma = NaN, hue, saturation = NaN, vividness = NaN, blackness = NaN, whiteness = NaN, viewingConditions }) {
        this.brightness = brightness;
        this.lightness = lightness;
        this.colorfulness = colorfulness;
        this.chroma = chroma;
        this.hue = hue;
        this.saturation = saturation;
        this.vividness = vividness;
        this.blackness = blackness;
        this.whiteness = whiteness;
        this.viewingConditions = viewingConditions;
      }
      // Aliases to match the paper
      /** Alias for [brightness]. **/
      get Qz() {
        return this.brightness;
      }
      /** Alias for [lightness]. **/
      get Jz() {
        return this.lightness;
      }
      /** Alias for [colorfulness]. **/
      get Mz() {
        return this.colorfulness;
      }
      /** Alias for [chroma]. **/
      get Cz() {
        return this.chroma;
      }
      /** Alias for [hue]. **/
      get hz() {
        return this.hue;
      }
      /** Alias for [saturation]. **/
      get Sz() {
        return this.saturation;
      }
      /** Alias for [vividness]. **/
      get Vz() {
        return this.vividness;
      }
      /** Alias for [blackness]. **/
      get Kz() {
        return this.blackness;
      }
      /** Alias for [whiteness]. **/
      get Wz() {
        return this.whiteness;
      }
      /**
       * Convert this color to the CIE XYZ color space, with absolute luminance.
       *
       * @see CieXyzAbs
       * @return Color in absolute XYZ
       */
      toXyzAbs(luminanceSource, chromaSource) {
        const cond = this.viewingConditions;
        const Qz_w = cond.Qz_w;
        const Iz = Math.pow(luminanceSource == LuminanceSource.BRIGHTNESS ? this.Qz / cond.Iz_coeff : this.Jz * Qz_w / (cond.Iz_coeff * 100), cond.Qz_denom / (1.6 * cond.surroundFactor));
        let Cz;
        switch (chromaSource) {
          case ChromaSource.CHROMA:
            Cz = this.Cz;
            break;
          case ChromaSource.COLORFULNESS:
            Cz = NaN;
            break;
          case ChromaSource.SATURATION:
            Cz = this.Qz * (0, math_1.square)(this.Sz) / (100 * Qz_w * cond.Sz_denom);
            break;
          case ChromaSource.VIVIDNESS:
            Cz = Math.sqrt(((0, math_1.square)(this.Vz) - (0, math_1.square)(this.Jz - 58)) / 3.4);
            break;
          case ChromaSource.BLACKNESS:
            Cz = Math.sqrt(((0, math_1.square)((100 - this.Kz) / 0.8) - (0, math_1.square)(this.Jz)) / 8);
            break;
          case ChromaSource.WHITENESS:
            Cz = Math.sqrt((0, math_1.square)(100 - this.Wz) - (0, math_1.square)(100 - this.Jz));
            break;
        }
        const Mz = chromaSource == ChromaSource.COLORFULNESS ? this.Mz : Cz * Qz_w / 100;
        const ez = (0, exports.hpToEz)(this.hz);
        const Cz_p = Math.pow(Mz * cond.Mz_denom / // Paper specifies pow(1.3514) but this extra precision is necessary for accurate inversion
        (100 * Math.pow(ez, 0.068) * cond.ez_coeff), 1 / 0.37 / 2);
        const hzRad = (0, math_1.toRadians)(this.hz);
        const az = Cz_p * Math.cos(hzRad);
        const bz = Cz_p * Math.sin(hzRad);
        const I = Iz + EPSILON;
        const r = pq(I + 0.2772100865 * az + 0.1160946323 * bz);
        const g = pq(I);
        const b = pq(I + 0.0425858012 * az + -0.7538445799 * bz);
        const xp = 1.9242264358 * r + -1.0047923126 * g + 0.037651404 * b;
        const yp = 0.3503167621 * r + 0.7264811939 * g + -0.0653844229 * b;
        const z = -0.090982811 * r + -0.3127282905 * g + 1.5227665613 * b;
        const x = (xp + (B - 1) * z) / B;
        const y = (yp + (G - 1) * x) / G;
        return new CieXyzAbs_1.CieXyzAbs(x, y, z);
      }
      /**
       * Convert this ZCAM color to linear sRGB, and clip it to sRGB gamut boundaries if it's not already within gamut.
       *
       * Out-of-gamut colors are mapped using gamut intersection in a 2D plane, and hue is always preserved. Lightness and
       * chroma are changed depending on the clip method; see [ClipMethod] for details.
       *
       * @return clipped color in linear sRGB
       */
      clipToLinearSrgb(method = LchGamut_1.ClipMethod.PRESERVE_LIGHTNESS, alpha = 0.05) {
        let l0;
        switch (method) {
          case LchGamut_1.ClipMethod.PRESERVE_LIGHTNESS:
            l0 = this.lightness;
            break;
          case LchGamut_1.ClipMethod.PROJECT_TO_MID:
            l0 = 50;
            break;
          case LchGamut_1.ClipMethod.ADAPTIVE_TOWARDS_MID:
            l0 = NaN;
            break;
        }
        return LchGamut_1.LchGamut.clip(this.lightness, this.chroma, this.hue, l0, LchGamut_1.LchGamut.EPSILON_100, 100, {
          getColor: /* @__PURE__ */ __name((l, c, h) => {
            const { viewingConditions } = this;
            return new _Zcam({
              lightness: l,
              chroma: c,
              hue: h,
              viewingConditions
            }).toXyzAbs(LuminanceSource.LIGHTNESS, ChromaSource.CHROMA).toRel(viewingConditions.referenceWhite.y).toLinearSrgb();
          }, "getColor")
        });
      }
    };
    exports.Zcam = Zcam;
  }
});

// node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/tristimulus/CieXyzAbs.js
var require_CieXyzAbs = __commonJS({
  "node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/tristimulus/CieXyzAbs.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.CieXyzAbs = void 0;
    var Zcam_1 = require_Zcam();
    var math_1 = require_math2();
    var CieXyz_1 = require_CieXyz();
    var CieXyzAbs = class {
      static {
        __name(this, "CieXyzAbs");
      }
      constructor(x, y, z) {
        this.x = x;
        this.y = y;
        this.z = z;
      }
      /**
       * Convert an absolute XYZ color to relative XYZ, using the specified reference white luminance.
       *
       * @return Color in relative XYZ
       */
      toRel(luminance = CieXyz_1.DEFAULT_SDR_WHITE_LUMINANCE) {
        return new CieXyz_1.CieXyz(this.x / luminance, this.y / luminance, this.z / luminance);
      }
      /**
       * Get the perceptual appearance attributes of this color using the [Zcam] color appearance model.
       * Input colors must be relative to a reference white of D65, absolute luminance notwithstanding.
       *
       * @return [Zcam] attributes
       */
      toZcam(cond, include2D = true) {
        const [Iz, az, bz] = (0, Zcam_1.xyzToIzazbz)(this);
        const hzRaw = (0, math_1.toDegrees)(Math.atan2(bz, az));
        const hz = hzRaw < 0 ? hzRaw + 360 : hzRaw;
        const ez = (0, Zcam_1.hpToEz)(hz);
        const Qz = (0, Zcam_1.izToQz)(Iz, cond);
        const Qz_w = cond.Qz_w;
        const Jz = 100 * (Qz / Qz_w);
        const Mz = 100 * Math.pow((0, math_1.square)(az) + (0, math_1.square)(bz), 0.37) * (Math.pow(ez, 0.068) * cond.ez_coeff / cond.Mz_denom);
        const Cz = 100 * (Mz / Qz_w);
        const Sz = include2D ? 100 * cond.Sz_coeff * Math.sqrt(Mz / Qz) : NaN;
        const Vz = include2D ? Math.sqrt((0, math_1.square)(Jz - 58) + 3.4 * (0, math_1.square)(Cz)) : NaN;
        const Kz = include2D ? 100 - 0.8 * Math.sqrt((0, math_1.square)(Jz) + 8 * (0, math_1.square)(Cz)) : NaN;
        const Wz = include2D ? 100 - Math.sqrt((0, math_1.square)(100 - Jz) + (0, math_1.square)(Cz)) : NaN;
        return new Zcam_1.Zcam({
          brightness: Qz,
          lightness: Jz,
          colorfulness: Mz,
          chroma: Cz,
          hue: hz,
          saturation: Sz,
          vividness: Vz,
          blackness: Kz,
          whiteness: Wz,
          viewingConditions: cond
        });
      }
    };
    exports.CieXyzAbs = CieXyzAbs;
  }
});

// node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/tristimulus/CieXyz.js
var require_CieXyz = __commonJS({
  "node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/tristimulus/CieXyz.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.CieXyz = exports.DEFAULT_SDR_WHITE_LUMINANCE = void 0;
    var LinearRgb_1 = require_LinearRgb();
    var CieXyzAbs_1 = require_CieXyzAbs();
    exports.DEFAULT_SDR_WHITE_LUMINANCE = 200;
    var CieXyz = class {
      static {
        __name(this, "CieXyz");
      }
      constructor(x, y, z) {
        this.x = x;
        this.y = y;
        this.z = z;
      }
      /**
       * Convert a relative XYZ color to absolute XYZ, using the specified reference white luminance.
       *
       * @return Color in absolute XYZ
       */
      toAbs(luminance = exports.DEFAULT_SDR_WHITE_LUMINANCE) {
        return new CieXyzAbs_1.CieXyzAbs(this.x * luminance, this.y * luminance, this.z * luminance);
      }
      /**
       * Convert this color to the linear sRGB color space.
       *
       * @see LinearSrgb
       * @return Color in linear sRGB
       */
      toLinearSrgb() {
        const { x, y, z } = this;
        return new LinearRgb_1.LinearSrgb(3.2404541621141045 * x + -1.5371385127977162 * y + -0.4985314095560159 * z, -0.969266030505187 * x + 1.8760108454466944 * y + 0.04155601753034983 * z, 0.05564343095911474 * x + -0.2040259135167538 * y + 1.0572251882231787 * z);
      }
    };
    exports.CieXyz = CieXyz;
  }
});

// node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/rgb/LinearRgb.js
var require_LinearRgb = __commonJS({
  "node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/rgb/LinearRgb.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.LinearSrgb = void 0;
    var CieXyz_1 = require_CieXyz();
    var Srgb_1 = require_Srgb();
    var LinearSrgb = class {
      static {
        __name(this, "LinearSrgb");
      }
      constructor(r, g, b) {
        this.r = r;
        this.g = g;
        this.b = b;
      }
      /**
       * Check whether this color is within the sRGB gamut.
       * This will return false if any component is either NaN or is not within the 0-1 range.
       *
       * @return true if color is in gamut, false otherwise
       */
      isInGamut() {
        const { r, g, b } = this;
        return r >= 0 && r <= 1 && g >= 0 && g <= 1 && b >= 0 && b <= 1;
      }
      // Linear -> sRGB
      f(x) {
        if (x >= 31308e-7) {
          return 1.055 * Math.pow(x, 1 / 2.4) - 0.055;
        } else {
          return 12.92 * x;
        }
      }
      /**
       * Convert this color to standard sRGB.
       * This delinearizes the sRGB components.
       *
       * @see Srgb
       * @return Color in standard sRGB
       */
      toSrgb() {
        const { r, g, b, f } = this;
        return new Srgb_1.Srgb([f(r), f(g), f(b)]);
      }
      /**
       * Convert a linear sRGB color (D65 white point) to the CIE XYZ color space.
       *
       * @return Color in XYZ
       */
      toXyz() {
        const { r, g, b } = this;
        return new CieXyz_1.CieXyz(0.41245643908969226 * r + 0.357576077643909 * g + 0.18043748326639897 * b, 0.21267285140562256 * r + 0.715152155287818 * g + 0.07217499330655959 * b, 0.019333895582329303 * r + 0.11919202588130297 * g + 0.950304078536368 * b);
      }
    };
    exports.LinearSrgb = LinearSrgb;
  }
});

// node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/rgb/Srgb.js
var require_Srgb = __commonJS({
  "node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/rgb/Srgb.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.Srgb = void 0;
    var LinearRgb_1 = require_LinearRgb();
    var Srgb = class {
      static {
        __name(this, "Srgb");
      }
      // Convenient constructors for quantized values
      /**
       * **[string, string, string]** Create a color from 8-bit integer sRGB components.
       *
       * **number** Create a color from a packed (A)RGB8 integer.
       *
       * **string** Create a color from a hex color code (e.g. #FA00FA).
       *            Hex codes with and without leading hash (#) symbols are supported.
       */
      constructor(color) {
        let r;
        let g;
        let b;
        if (typeof color == "number") {
          color = (color & 16777215).toString(16).padStart(6, "0");
        }
        if (typeof color == "string") {
          color = color.replace("#", "").replace(/^([a-f\d])([a-f\d])([a-f\d])$/i, (_, r2, g2, b2) => r2 + r2 + g2 + g2 + b2 + b2);
          const match = color.match(/^([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/);
          if (!match) {
            throw new Error("Invalid color");
          }
          color = [
            parseInt(match[1], 16).toString(),
            parseInt(match[2], 16).toString(),
            parseInt(match[3], 16).toString()
          ];
        }
        if (Array.isArray(color) && typeof color[0] === "string") {
          color = [
            Number(color[0]) / 255,
            Number(color[1]) / 255,
            Number(color[2]) / 255
          ];
        }
        ;
        [r, g, b] = color;
        this.r = r;
        this.g = g;
        this.b = b;
      }
      /** Clamp out-of-bounds values */
      quantize8(n) {
        return Math.max(0, Math.min(Math.round(n * 255), 255));
      }
      /**
       * Convert this color to an 8-bit packed RGB integer (32 bits total)
       *
       * This is equivalent to the integer value of hex color codes (e.g. #FA00FA).
       *
       * @return color as 32-bit integer in RGB8 format
       */
      toRgb8() {
        const { r, g, b, quantize8 } = this;
        return parseInt(quantize8(r).toString(16).padStart(2, "0") + quantize8(g).toString(16).padStart(2, "0") + quantize8(b).toString(16).padStart(2, "0"), 16);
      }
      /**
       * Convert this color to an 8-bit hex color code (e.g. #FA00FA).
       *
       * @return color as RGB8 hex code
       */
      toHex() {
        return "#" + this.toRgb8().toString(16).padStart(6, "0");
      }
      /** sRGB to linear */
      fInv(x) {
        if (x >= 0.04045) {
          return Math.pow((x + 0.055) / 1.055, 2.4);
        } else {
          return x / 12.92;
        }
      }
      /**
       * Convert this color to linear sRGB.
       * This linearizes the sRGB components.
       *
       * @see LinearSrgb
       * @return Color in linear sRGB
       */
      toLinear() {
        const { r, g, b, fInv } = this;
        return new LinearRgb_1.LinearSrgb(fInv(r), fInv(g), fInv(b));
      }
      /**
       * Convert this color to Zcam
       */
      toZcam(cond, include2D = false) {
        return this.toLinear().toXyz().toAbs(cond.referenceWhite.y).toZcam(cond, include2D);
      }
    };
    exports.Srgb = Srgb;
  }
});

// node_modules/.pnpm/@monet-color+palette@0.0.1-alpha.4_@monet-color+quantize@0.0.1-alpha.1_@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/palette/score.js
var require_score = __commonJS({
  "node_modules/.pnpm/@monet-color+palette@0.0.1-alpha.4_@monet-color+quantize@0.0.1-alpha.1_@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/palette/score.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.Score = void 0;
    var math_1 = require_math2();
    var Srgb_1 = require_Srgb();
    var Score = class _Score {
      static {
        __name(this, "Score");
      }
      /**
       * Given a map with keys of colors and values of how often the color appears,
       * rank the colors based on suitability for being used for a UI theme.
       *
       * @param colorsToPopulation map with keys of colors and values of how often
       *     the color appears, usually from a source image.
       * @return Colors sorted by suitability for a UI theme. The most suitable
       *     color is the first item, the least suitable is the last. There will
       *     always be at least one color returned. If all the input colors
       *     were not suitable for a theme, a default fallback color will be
       *     provided, Google Blue.
       */
      static score(colorsToPopulation, cond) {
        let populationSum = 0;
        for (const population of colorsToPopulation.values()) {
          populationSum += population;
        }
        const colorsToProportion = /* @__PURE__ */ new Map();
        const colorsToCam = /* @__PURE__ */ new Map();
        const hueProportions = new Array(360).fill(0);
        for (const [color, population] of colorsToPopulation.entries()) {
          const proportion = population / populationSum;
          colorsToProportion.set(color, proportion);
          const cam = new Srgb_1.Srgb(color & 16777215).toLinear().toXyz().toAbs(cond.referenceWhite.y).toZcam(cond, false);
          colorsToCam.set(color, cam);
          const hue = Math.round(cam.hue);
          hueProportions[hue] += proportion;
        }
        const colorsToExcitedProportion = /* @__PURE__ */ new Map();
        for (const [color, cam] of colorsToCam.entries()) {
          const hue = Math.round(cam.hue);
          let excitedProportion = 0;
          for (let i = hue - 10; i < hue + 10; i++) {
            const neighborHue = (0, math_1.sanitizeDegrees)(i);
            excitedProportion += hueProportions[neighborHue];
          }
          colorsToExcitedProportion.set(color, excitedProportion);
        }
        const colorsToScore = /* @__PURE__ */ new Map();
        for (const [color, cam] of colorsToCam.entries()) {
          const proportion = colorsToExcitedProportion.get(color);
          const proportionScore = proportion * 100 * _Score.WEIGHT_PROPORTION;
          const chromaWeight = cam.colorfulness < _Score.TARGET_CHROMA ? _Score.WEIGHT_CHROMA_BELOW : _Score.WEIGHT_CHROMA_ABOVE;
          const chromaScore = (cam.colorfulness - _Score.TARGET_CHROMA) * chromaWeight;
          const score = proportionScore + chromaScore;
          colorsToScore.set(color, score);
        }
        const filteredColors = _Score.filter(colorsToExcitedProportion, colorsToCam).sort((c1, c2) => {
          const { colorfulness: c1Colorfulness, lightness: c1Lightness } = colorsToCam.get(c1);
          const { colorfulness: c2Colorfulness, lightness: c2Lightness } = colorsToCam.get(c2);
          return (c2Colorfulness * 0.4 + c2Lightness * 0.7) * colorsToScore.get(c2) - (c1Colorfulness * 0.4 + c1Lightness * 0.7) * colorsToScore.get(c1);
        });
        const dedupedColorsToScore = /* @__PURE__ */ new Map();
        for (const color of filteredColors) {
          let duplicateHue = false;
          const hue = colorsToCam.get(color).hue;
          for (const [alreadyChosenColor] of dedupedColorsToScore) {
            const alreadyChosenHue = colorsToCam.get(alreadyChosenColor).hue;
            if ((0, math_1.differenceDegrees)(hue, alreadyChosenHue) < 15) {
              duplicateHue = true;
              break;
            }
          }
          if (duplicateHue) {
            continue;
          }
          dedupedColorsToScore.set(color, colorsToScore.get(color));
        }
        const colorsByScoreDescending = Array.from(dedupedColorsToScore.entries());
        colorsByScoreDescending.sort((first, second) => {
          return second[1] - first[1];
        });
        const answer = colorsByScoreDescending.map((entry) => {
          return entry[0];
        });
        if (answer.length === 0) {
          if (filteredColors.length) {
            answer.push(filteredColors[0]);
          } else {
            let maxScore = 0;
            let dominantColor;
            colorsToScore.forEach((score, color) => {
              if (score > maxScore) {
                maxScore = score;
                dominantColor = color;
              }
            });
            answer.push(dominantColor || 16777215);
          }
        }
        return answer;
      }
      static filter(colorsToExcitedProportion, colorsToCam) {
        const filtered = [];
        for (const [color, cam] of colorsToCam.entries()) {
          const proportion = colorsToExcitedProportion.get(color);
          if (cam.colorfulness >= _Score.CUTOFF_CHROMA && cam.lightness >= _Score.CUTOFF_TONE && proportion >= _Score.CUTOFF_EXCITED_PROPORTION) {
            filtered.push(color);
          }
        }
        return filtered;
      }
    };
    exports.Score = Score;
    Score.TARGET_CHROMA = 25;
    Score.WEIGHT_PROPORTION = 0.4;
    Score.WEIGHT_CHROMA_ABOVE = 0.5;
    Score.WEIGHT_CHROMA_BELOW = 0.1;
    Score.CUTOFF_CHROMA = 15;
    Score.CUTOFF_TONE = 10;
    Score.CUTOFF_EXCITED_PROPORTION = 0.01;
  }
});

// node_modules/.pnpm/@monet-color+palette@0.0.1-alpha.4_@monet-color+quantize@0.0.1-alpha.1_@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/palette/palette.js
var require_palette = __commonJS({
  "node_modules/.pnpm/@monet-color+palette@0.0.1-alpha.4_@monet-color+quantize@0.0.1-alpha.1_@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/palette/palette.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.getPalette = exports.getPopulations = void 0;
    var quantize_1 = require_quantize();
    var Srgb_1 = require_Srgb();
    var score_1 = require_score();
    var MAX_CANVAS_SIZE = 100;
    function getPopulations(image, maxColors = 128, percentage = false) {
      const { width, height } = image;
      const ratio = width / height;
      const isPortrait = width < height;
      const w = isPortrait ? MAX_CANVAS_SIZE * ratio : MAX_CANVAS_SIZE;
      const h = isPortrait ? MAX_CANVAS_SIZE : MAX_CANVAS_SIZE / ratio;
      const canvas = document.createElement("canvas");
      canvas.width = w;
      canvas.height = h;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(image, 0, 0, w, h);
      const pixelData = ctx.getImageData(0, 0, w, h).data;
      const pixels = [];
      for (let i = 0; i < pixelData.length; i += 4) {
        const color = (
          // alpha
          pixelData[i + 3].toString(16).padStart(2, "0") + // red
          pixelData[i].toString(16).padStart(2, "0") + // green
          pixelData[i + 1].toString(16).padStart(2, "0") + // blue
          pixelData[i + 2].toString(16).padStart(2, "0")
        );
        pixels.push(parseInt(color, 16));
      }
      const populations = quantize_1.QuantizerCelebi.quantize(pixels, maxColors);
      if (percentage) {
        for (const [color, population] of populations.entries()) {
          populations.set(color, population / pixels.length);
        }
      }
      return populations;
    }
    __name(getPopulations, "getPopulations");
    exports.getPopulations = getPopulations;
    function getPalette2(image, cond, prePopulations) {
      const populations = prePopulations || getPopulations(image);
      const colors = score_1.Score.score(populations, cond);
      return colors.map((color) => new Srgb_1.Srgb(color).toHex());
    }
    __name(getPalette2, "getPalette");
    exports.getPalette = getPalette2;
  }
});

// node_modules/.pnpm/@monet-color+palette@0.0.1-alpha.4_@monet-color+quantize@0.0.1-alpha.1_@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/palette/index.js
var require_palette2 = __commonJS({
  "node_modules/.pnpm/@monet-color+palette@0.0.1-alpha.4_@monet-color+quantize@0.0.1-alpha.1_@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/palette/index.js"(exports) {
    "use strict";
    var __createBinding = exports && exports.__createBinding || (Object.create ? function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      Object.defineProperty(o, k2, { enumerable: true, get: /* @__PURE__ */ __name(function() {
        return m[k];
      }, "get") });
    } : function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      o[k2] = m[k];
    });
    var __exportStar = exports && exports.__exportStar || function(m, exports2) {
      for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports2, p)) __createBinding(exports2, m, p);
    };
    Object.defineProperty(exports, "__esModule", { value: true });
    __exportStar(require_palette(), exports);
  }
});

// node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/data/Illuminants.js
var require_Illuminants = __commonJS({
  "node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/data/Illuminants.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.Illuminants = void 0;
    var CieXyz_1 = require_CieXyz();
    var xyToX = /* @__PURE__ */ __name((x, y) => x / y, "xyToX");
    var xyToZ = /* @__PURE__ */ __name((x, y) => (1 - x - y) / y, "xyToZ");
    exports.Illuminants = {
      /**
       * ASTM variant of CIE Standard Illuminant D65. ~6500K color temperature; approximates average daylight in Europe.
       * This uses the XYZ values defined in the ASTM E‑308 document.
       *
       * @see <a href="https://en.wikipedia.org/wiki/Illuminant_D65">Wikipedia: Illuminant D65</a>
       */
      get D65() {
        return new CieXyz_1.CieXyz(0.95047, 1, 1.08883);
      },
      /**
       * sRGB variant of CIE Standard Illuminant D65. ~6500K color temperature; approximates average daylight in Europe.
       * This uses the white point chromaticities defined in the sRGB specification.
       *
       * @see <a href="https://en.wikipedia.org/wiki/SRGB">Wikipedia: sRGB</a>
       */
      get D65_SRGB() {
        return new CieXyz_1.CieXyz(xyToX(0.3127, 0.329), 1, xyToZ(0.3127, 0.329));
      },
      /**
       * Raw precise variant of CIE Standard Illuminant D65. ~6500K color temperature; approximates average daylight in Europe.
       * This uses XYZ values calculated from raw 1nm SPD data, combined with the CIE 1931 2-degree
       * standard observer.
       *
       * @see <a href="https://www.rit.edu/cos/colorscience/rc_useful_data.php">RIT - Useful Color Data</a>
       */
      get D65_CIE() {
        return new CieXyz_1.CieXyz(0.9504705586542832, 1, 1.088828736395884);
      },
      /**
       * CIE Standard Illuminant D50. ~5000K color temperature.
       */
      get D50() {
        return new CieXyz_1.CieXyz(xyToX(0.3457, 0.3585), 1, xyToZ(0.3457, 0.3585));
      }
    };
  }
});

// node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/lab/CieLab.js
var require_CieLab = __commonJS({
  "node_modules/.pnpm/@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/tools/lab/CieLab.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.CieLab = void 0;
    var Illuminants_1 = require_Illuminants();
    var math_1 = require_math2();
    var CieXyz_1 = require_CieXyz();
    var CieLab = class {
      static {
        __name(this, "CieLab");
      }
      constructor(L, a, b, referenceWhite = Illuminants_1.Illuminants.D65) {
        this.L = L;
        this.a = a;
        this.b = b;
        this.referenceWhite = referenceWhite;
      }
      toXyz() {
        const lp = (this.L + 16) / 116;
        return new CieXyz_1.CieXyz(this.referenceWhite.x * this.fInv(lp + this.a / 500), this.referenceWhite.y * this.fInv(lp), this.referenceWhite.z * this.fInv(lp - this.b / 200));
      }
      // private f(x: number) {
      //   if (x > 216.0 / 24389.0) {
      //     return Math.cbrt(x);
      //   } else {
      //     return x / (108.0 / 841.0) + 4.0 / 29.0;
      //   }
      // }
      fInv(x) {
        if (x > 6 / 29) {
          return (0, math_1.cube)(x);
        } else {
          return 108 / 841 * (x - 4 / 29);
        }
      }
    };
    exports.CieLab = CieLab;
  }
});

// node_modules/.pnpm/@monet-color+theme@0.0.1-alpha.4_@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/theme/ColorScheme.js
var require_ColorScheme = __commonJS({
  "node_modules/.pnpm/@monet-color+theme@0.0.1-alpha.4_@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/theme/ColorScheme.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.ColorScheme = void 0;
    var ColorScheme = class {
      static {
        __name(this, "ColorScheme");
      }
      // Helpers
      get accentColors() {
        return [this.accent1, this.accent2, this.accent3];
      }
      get neutralColors() {
        return [this.neutral1, this.neutral2];
      }
    };
    exports.ColorScheme = ColorScheme;
  }
});

// node_modules/.pnpm/@monet-color+theme@0.0.1-alpha.4_@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/theme/MaterialYouTargets.js
var require_MaterialYouTargets = __commonJS({
  "node_modules/.pnpm/@monet-color+theme@0.0.1-alpha.4_@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/theme/MaterialYouTargets.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.MaterialYouTargets = void 0;
    var Zcam_1 = require_Zcam();
    var Srgb_1 = require_Srgb();
    var CieLab_1 = require_CieLab();
    var ColorScheme_1 = require_ColorScheme();
    var SHADE_TO_LIGHTNESS = [
      [0, 100],
      [10, 99],
      [20, 98],
      [50, 95],
      [100, 90],
      [200, 80],
      [300, 70],
      [400, 60],
      [500, 50],
      [600, 40],
      [650, 35],
      [700, 30],
      [800, 20],
      [900, 10],
      [950, 5],
      [1e3, 0]
    ];
    var LINEAR_LIGHTNESS_MAP = new Map(SHADE_TO_LIGHTNESS);
    var CIELAB_LIGHTNESS_MAP = new Map(SHADE_TO_LIGHTNESS.map(([key, value]) => [key, value == 50 ? 49.6 : value]));
    var REF_ACCENT1_COLORS = [
      13886461,
      11061242,
      8170744,
      5017078,
      1797875,
      743376,
      541344,
      405103,
      269897
    ];
    var ACCENT1_REF_CHROMA_FACTOR = 1.2;
    var MaterialYouTargets = class extends ColorScheme_1.ColorScheme {
      static {
        __name(this, "MaterialYouTargets");
      }
      constructor(chromaFactor = 1, cond, useLinearLightness = false) {
        super();
        this.chromaFactor = chromaFactor;
        this.cond = cond;
        const lightnessMap = useLinearLightness ? LINEAR_LIGHTNESS_MAP : this.calcCieLabLightnessMap();
        const accent1Chroma = this.calcAccent1Chroma(cond) * ACCENT1_REF_CHROMA_FACTOR;
        const accent2Chroma = accent1Chroma / 3;
        const accent3Chroma = accent2Chroma * 2;
        const neutral1Chroma = accent1Chroma / 8;
        const neutral2Chroma = accent1Chroma / 5;
        this.neutral1 = this.shadesWithChroma(neutral1Chroma, lightnessMap);
        this.neutral2 = this.shadesWithChroma(neutral2Chroma, lightnessMap);
        this.accent1 = this.shadesWithChroma(accent1Chroma, lightnessMap);
        this.accent2 = this.shadesWithChroma(accent2Chroma, lightnessMap);
        this.accent3 = this.shadesWithChroma(accent3Chroma, lightnessMap);
      }
      calcCieLabLightnessMap() {
        const arr = [];
        CIELAB_LIGHTNESS_MAP.forEach((value, key) => arr.push([key, this.cielabL(value)]));
        return new Map(arr);
      }
      cielabL(l) {
        return new CieLab_1.CieLab(l, 0, 0).toXyz().toAbs(this.cond.referenceWhite.y).toZcam(this.cond, false).lightness;
      }
      calcAccent1Chroma(cond) {
        const chromaSum = REF_ACCENT1_COLORS.reduce((prev, curr) => {
          return prev + new Srgb_1.Srgb(curr).toLinear().toXyz().toAbs(cond.referenceWhite.y).toZcam(cond, false).chroma;
        }, 0);
        return chromaSum / REF_ACCENT1_COLORS.length;
      }
      shadesWithChroma(chroma, lightnessMap) {
        const chromaAdj = chroma * this.chromaFactor;
        const arr = [];
        lightnessMap.forEach((value, key) => arr.push([
          key,
          new Zcam_1.Zcam({
            lightness: value,
            chroma: chromaAdj,
            hue: 0,
            viewingConditions: this.cond
          })
        ]));
        return new Map(arr);
      }
    };
    exports.MaterialYouTargets = MaterialYouTargets;
  }
});

// node_modules/.pnpm/@monet-color+theme@0.0.1-alpha.4_@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/theme/WhiteLuminance.js
var require_WhiteLuminance = __commonJS({
  "node_modules/.pnpm/@monet-color+theme@0.0.1-alpha.4_@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/theme/WhiteLuminance.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.parseUserWhiteLuminance = exports.WHITE_LUMINANCE_USER_DEFAULT = exports.WHITE_LUMINANCE_USER_STEP = exports.WHITE_LUMINANCE_USER_MAX = void 0;
    var WHITE_LUMINANCE_MIN = 1;
    var WHITE_LUMINANCE_MAX = 1e4;
    exports.WHITE_LUMINANCE_USER_MAX = 1e3;
    exports.WHITE_LUMINANCE_USER_STEP = 25;
    exports.WHITE_LUMINANCE_USER_DEFAULT = 425;
    function parseUserWhiteLuminance(userValue = exports.WHITE_LUMINANCE_USER_DEFAULT) {
      const userSrc = userValue / exports.WHITE_LUMINANCE_USER_MAX;
      const userInv = 1 - userSrc;
      return Math.max(Math.pow(10, userInv * Math.log10(WHITE_LUMINANCE_MAX)), WHITE_LUMINANCE_MIN);
    }
    __name(parseUserWhiteLuminance, "parseUserWhiteLuminance");
    exports.parseUserWhiteLuminance = parseUserWhiteLuminance;
  }
});

// node_modules/.pnpm/@monet-color+theme@0.0.1-alpha.4_@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/theme/DynamicColorScheme.js
var require_DynamicColorScheme = __commonJS({
  "node_modules/.pnpm/@monet-color+theme@0.0.1-alpha.4_@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/theme/DynamicColorScheme.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.DynamicColorScheme = void 0;
    var Zcam_1 = require_Zcam();
    var Srgb_1 = require_Srgb();
    var LchGamut_1 = require_LchGamut();
    var ColorScheme_1 = require_ColorScheme();
    var ACCENT3_HUE_SHIFT_DEGREES = 60;
    var DynamicColorScheme = class extends ColorScheme_1.ColorScheme {
      static {
        __name(this, "DynamicColorScheme");
      }
      constructor(targets, seedColor, chromaFactor = 1, cond, accurateShades = true, complementColor = null) {
        super();
        this.targets = targets;
        this.seedColor = seedColor;
        this.chromaFactor = chromaFactor;
        this.cond = cond;
        this.accurateShades = accurateShades;
        this.complementColor = complementColor;
        const seedNeutral = new Srgb_1.Srgb(seedColor).toLinear().toXyz().toAbs(cond.referenceWhite.y).toZcam(cond, false);
        seedNeutral.chroma = seedNeutral.chroma * chromaFactor;
        const seedAccent = seedNeutral;
        const seedAccent3 = new Zcam_1.Zcam({
          ...seedAccent,
          chroma: seedAccent.chroma * 0.8,
          hue: complementColor ? new Srgb_1.Srgb(complementColor).toLinear().toXyz().toAbs(cond.referenceWhite.y).toZcam(cond, false).hue : seedAccent.hue + ACCENT3_HUE_SHIFT_DEGREES
        });
        this.accent1 = this.transformSwatch(targets.accent1, seedAccent, targets.accent1);
        this.accent2 = this.transformSwatch(targets.accent2, seedAccent, targets.accent1);
        this.accent3 = this.transformSwatch(targets.accent3, seedAccent3, targets.accent1);
        this.neutral1 = this.transformSwatch(targets.neutral1, seedNeutral, targets.neutral1);
        this.neutral2 = this.transformSwatch(targets.neutral2, seedNeutral, targets.neutral1);
      }
      transformSwatch(swatch, seed, referenceSwatch) {
        const arr = [];
        swatch.forEach((color, shade) => {
          const target = color;
          const reference = referenceSwatch.get(shade);
          const newLch = this.transformColor(target, seed, reference);
          const newSrgb = newLch.toSrgb();
          arr.push([shade, newSrgb.toHex()]);
        });
        return new Map(arr);
      }
      transformColor(target, seed, reference) {
        const lightness = target.lightness;
        const scaleC = reference.chroma == 0 ? (
          // Zero reference chroma won't have chroma anyway, so use 0 to avoid a divide-by-zero
          0
        ) : (
          // Non-zero reference chroma = possible chroma scale
          Math.max(0, Math.min(seed.chroma, reference.chroma)) / reference.chroma
        );
        const chroma = target.chroma * scaleC;
        const hue = seed.hue;
        const newColor = new Zcam_1.Zcam({
          lightness,
          chroma,
          hue,
          viewingConditions: this.cond
        });
        return this.accurateShades ? newColor.clipToLinearSrgb(LchGamut_1.ClipMethod.PRESERVE_LIGHTNESS) : newColor.clipToLinearSrgb(LchGamut_1.ClipMethod.ADAPTIVE_TOWARDS_MID, 5);
      }
    };
    exports.DynamicColorScheme = DynamicColorScheme;
  }
});

// node_modules/.pnpm/@monet-color+theme@0.0.1-alpha.4_@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/theme/index.js
var require_theme = __commonJS({
  "node_modules/.pnpm/@monet-color+theme@0.0.1-alpha.4_@monet-color+tools@0.0.1-alpha.4/node_modules/@monet-color/theme/index.js"(exports) {
    "use strict";
    var __createBinding = exports && exports.__createBinding || (Object.create ? function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      Object.defineProperty(o, k2, { enumerable: true, get: /* @__PURE__ */ __name(function() {
        return m[k];
      }, "get") });
    } : function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      o[k2] = m[k];
    });
    var __exportStar = exports && exports.__exportStar || function(m, exports2) {
      for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports2, p)) __createBinding(exports2, m, p);
    };
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.createColorScheme = exports.DEFAULT_VIEWING_CONDITIONS = exports.createZcamViewingConditions = void 0;
    var Zcam_1 = require_Zcam();
    var CieLab_1 = require_CieLab();
    var Illuminants_1 = require_Illuminants();
    var MaterialYouTargets_1 = require_MaterialYouTargets();
    var WhiteLuminance_1 = require_WhiteLuminance();
    var DynamicColorScheme_1 = require_DynamicColorScheme();
    __exportStar(require_ColorScheme(), exports);
    __exportStar(require_DynamicColorScheme(), exports);
    __exportStar(require_MaterialYouTargets(), exports);
    function createZcamViewingConditions(whiteLuminance) {
      return new Zcam_1.ViewingConditions(
        Zcam_1.ViewingConditions.SURROUND_AVERAGE,
        // sRGB
        0.4 * whiteLuminance,
        // Gray world
        new CieLab_1.CieLab(50, 0, 0).toXyz().y * whiteLuminance,
        Illuminants_1.Illuminants.D65.toAbs(whiteLuminance)
      );
    }
    __name(createZcamViewingConditions, "createZcamViewingConditions");
    exports.createZcamViewingConditions = createZcamViewingConditions;
    var SRGB_WHITE_LUMINANCE = 200;
    exports.DEFAULT_VIEWING_CONDITIONS = createZcamViewingConditions(SRGB_WHITE_LUMINANCE);
    function createColorScheme2(color, chromaFactor = 1, whiteLuminance, complementColor) {
      const cond = createZcamViewingConditions((0, WhiteLuminance_1.parseUserWhiteLuminance)(whiteLuminance));
      const targets = new MaterialYouTargets_1.MaterialYouTargets(chromaFactor, cond, false);
      return new DynamicColorScheme_1.DynamicColorScheme(targets, color, chromaFactor, cond, true, complementColor);
    }
    __name(createColorScheme2, "createColorScheme");
    exports.createColorScheme = createColorScheme2;
  }
});

// src/index.ts
var import_palette = __toESM(require_palette2());
var import_theme = __toESM(require_theme());
function adjustLineHeight() {
  const trElements = document.querySelectorAll(
    ".station-table tbody tr"
  );
  for (const trElem of trElements) {
    const lineHeight = trElem.offsetHeight;
    const pointElem = trElem.querySelector(".station-point");
    pointElem?.style.setProperty("--line-height", `${lineHeight - 8}px`);
  }
}
__name(adjustLineHeight, "adjustLineHeight");
async function changeThemeColor() {
  const bgUrl = "/bg";
  const resp = await fetch(bgUrl);
  const blob = await resp.blob();
  const dataUrl = URL.createObjectURL(blob);
  const imgElem = document.createElement("img");
  imgElem.src = dataUrl;
  await new Promise((resolve, reject) => {
    imgElem.addEventListener("load", resolve);
    imgElem.addEventListener("error", reject);
  });
  const colors = (0, import_palette.getPalette)(imgElem, import_theme.DEFAULT_VIEWING_CONDITIONS);
  const scheme = (0, import_theme.createColorScheme)(colors[0]);
  const cssWillAppend = `.bg-wrapper { background-image: url('${dataUrl}'); }
* { --top-bg-color: ${scheme.accent1.get(400)}aa; --top-title-color: ${scheme.accent2.get(50)}; --station-table-head-bg-color: ${scheme.accent1.get(100)}aa; --station-table-arrived-line-color: ${scheme.accent1.get(300)}; --station-table-head-color: ${scheme.accent1.get(400)}; }`;
  const styleElem = document.createElement("style");
  styleElem.innerHTML = cssWillAppend;
  document.head.appendChild(styleElem);
}
__name(changeThemeColor, "changeThemeColor");
(async () => {
  adjustLineHeight();
  await changeThemeColor();
  const doneDivElem = document.createElement("div");
  doneDivElem.id = "done";
  document.body.appendChild(doneDivElem);
})();
/*! Bundled license information:

@monet-color/quantize/index.js:
  (** @license ConanXie v0.0.1-alpha.1
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)

@monet-color/palette/index.js:
  (** @license ConanXie v0.0.1-alpha.4
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)

@monet-color/theme/index.js:
  (** @license ConanXie v0.0.1-alpha.4
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)
*/
