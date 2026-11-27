// news-image-20261127 entrypoint.
// Copies the rendered entry.png (drawn by render.py, committed beside this
// file) into the output directory and verifies the copy byte for byte.
// Node 22, standard library only; runs with no network.
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = new URL("./entry.png", import.meta.url);

if (!existsSync(src)) {
  throw new Error("entry.png is missing next to main.ts");
}

const source = readFileSync(src);
if (source.length === 0) {
  throw new Error("entry.png is empty");
}
// PNG files start with the 8-byte signature; bytes 1..3 spell "PNG".
if (source.subarray(1, 4).toString("ascii") !== "PNG") {
  throw new Error("entry.png does not look like a PNG file");
}
if (source.length > 1024 * 1024) {
  throw new Error(`entry.png is ${source.length} bytes, over the 1 MiB limit`);
}
// IHDR follows the 8-byte signature + 8-byte chunk header: width and height
// are big-endian uint32 at offsets 16 and 20. The gate caps at 1024x1024.
if (source.length < 24 || source.subarray(12, 16).toString("ascii") !== "IHDR") {
  throw new Error("entry.png has no IHDR chunk where one is expected");
}
const width = source.readUInt32BE(16);
const height = source.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);

const copied = readFileSync(dest);
if (!copied.equals(source)) {
  throw new Error("copied entry.png differs from the source");
}
const size = statSync(dest).size;
if (size !== source.length) {
  throw new Error(`size mismatch after copy: ${size} vs ${source.length}`);
}

console.log(`entry.png copied to ${dest} (${size} bytes, verified byte-identical)`);
