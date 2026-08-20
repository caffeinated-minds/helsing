import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const extensionRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const repositoryRoot = path.resolve(extensionRoot, "../..");
const failures = [];

function read(relativePath) {
  return fs.readFileSync(path.join(extensionRoot, relativePath));
}

function requireFile(relativePath) {
  const absolutePath = path.join(extensionRoot, relativePath);
  if (!fs.existsSync(absolutePath)) {
    failures.push(`missing ${relativePath}`);
    return false;
  }
  return true;
}

function requirePng(relativePath) {
  if (!requireFile(relativePath)) {
    return;
  }

  const signature = read(relativePath).subarray(0, 8).toString("hex");
  if (signature !== "89504e470d0a1a0a") {
    failures.push(`${relativePath} is not a PNG file`);
  }
}

const manifest = JSON.parse(read("package.json").toString("utf8"));
JSON.parse(read("themes/helsing-color-theme.json").toString("utf8"));

const palette = fs.readFileSync(
  path.join(repositoryRoot, "docs/helsing-palette.yml"),
  "utf8",
);
const paletteVersion = palette.match(/^version:\s*["']?([^\s"']+)/m)?.[1];

if (!paletteVersion) {
  failures.push("could not read the canonical palette version");
} else if (manifest.version !== paletteVersion) {
  failures.push(
    `manifest version ${manifest.version} does not match palette ${paletteVersion}`,
  );
}

if (manifest.publisher !== "caffeinatedminds") {
  failures.push("publisher must be confirmed as caffeinatedminds");
}

if (manifest.icon !== "images/icon.png") {
  failures.push('package.json must set "icon" to "images/icon.png"');
}

if (!manifest.license) {
  failures.push("package.json has no licence field");
}

for (const requiredEntry of ["themes", "images", "LICENSE", "README.md", "CHANGELOG.md"]) {
  if (!manifest.files?.includes(requiredEntry)) {
    failures.push(`package.json files allowlist is missing ${requiredEntry}`);
  }
}

requireFile("LICENSE");
requirePng("images/icon.png");
requirePng("images/screenshot.png");

const readme = read("README.md").toString("utf8");
if (!readme.includes("images/screenshot.png")) {
  failures.push("README.md does not display images/screenshot.png");
}

if (failures.length > 0) {
  console.error("Release check failed:");
  for (const failure of failures) {
    console.error(`- ${failure}`);
  }
  process.exit(1);
}

console.log("Release metadata, assets and generated JSON are ready for packaging.");
