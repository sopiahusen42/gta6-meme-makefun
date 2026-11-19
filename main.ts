// gta6-meme-x-01 entry program (Node 22, stdlib only).
// Copies POST.json from the repository to the output directory, byte for byte,
// after checking it is a JSON object of at most 16384 bytes whose url is an X
// post address (https://x.com/<handle>/status/<id>, twitter.com likewise).
// The placeholder {"url": "PENDING"} is copied with a warning: the real post
// URL is filled in after the post is made on X.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const MAX_BYTES = 16384;
const X_POST_URL =
  /^https:\/\/(?:www\.|mobile\.)?(?:x\.com|twitter\.com)\/[A-Za-z0-9_]{1,15}\/status\/[0-9]+(?:[?#].*)?$/;

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const bytes = readFileSync(join(botDir, "POST.json"));
if (bytes.length > MAX_BYTES) {
  console.error(`POST.json is ${bytes.length} bytes; the cap is ${MAX_BYTES}`);
  process.exit(1);
}

let post: unknown;
try {
  post = JSON.parse(bytes.toString("utf8"));
} catch (err) {
  console.error(`POST.json is not valid JSON: ${(err as Error).message}`);
  process.exit(1);
}
if (typeof post !== "object" || post === null || Array.isArray(post)) {
  console.error("POST.json must be a JSON object");
  process.exit(1);
}
const url = (post as Record<string, unknown>).url;
if (typeof url !== "string") {
  console.error('POST.json must hold a string "url"');
  process.exit(1);
}
if (url === "PENDING") {
  console.warn("warning: url is PENDING; replace it with the real X post URL before submitting");
} else if (!X_POST_URL.test(url)) {
  console.error(`url is not an X post address: ${url}`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "POST.json"), bytes);
console.log(`copied POST.json (${bytes.length} bytes) to ${join(outDir, "POST.json")}`);
