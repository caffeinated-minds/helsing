import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const extensionRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const repositoryRoot = path.resolve(extensionRoot, "../..");
const requested = process.argv.slice(2);

if (requested.length === 0) {
  console.error("run-python.mjs requires a Python script and its arguments");
  process.exit(2);
}

const candidates = [
  process.env.HELSING_PYTHON,
  path.join(repositoryRoot, ".venv/bin/python"),
  path.join(repositoryRoot, ".venv/Scripts/python.exe"),
  "python3",
  "python",
].filter(Boolean);

for (const candidate of candidates) {
  if (candidate.includes(path.sep) && !fs.existsSync(candidate)) {
    continue;
  }

  const result = spawnSync(candidate, requested, {
    cwd: extensionRoot,
    stdio: "inherit",
  });
  if (result.error?.code === "ENOENT") {
    continue;
  }
  if (result.error) {
    throw result.error;
  }
  process.exit(result.status ?? 1);
}

console.error("No usable Python interpreter was found");
process.exit(1);
