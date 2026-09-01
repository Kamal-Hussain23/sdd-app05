// Simple frontend test.
// Verifies each page has the expected key elements that the app depends on.
// No test framework — just plain Node checks.

const fs = require("fs");
const path = require("path");

const pages = { "index.html": ["Cafe", "place-order", "/api/menu", "track-order", "/api/orders/"], "staff.html": ["Staff", "board", "/api/orders", "done"] };
let failed = false;

for (const [page, needles] of Object.entries(pages)) {
  const file = path.join(__dirname, "..", page);
  if (!fs.existsSync(file)) {
    console.error("Missing page: " + page);
    failed = true;
    continue;
  }
  const html = fs.readFileSync(file, "utf8");
  for (const needle of needles) {
    if (!html.includes(needle)) {
      console.error(page + " is missing expected content: " + needle);
      failed = true;
    }
  }
}

if (failed) {
  process.exit(1);
}
console.log("Frontend tests passed.");
