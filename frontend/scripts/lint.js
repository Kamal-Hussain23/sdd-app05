// Simple lint for the frontend HTML files.
// Checks that each page is a complete HTML document with a <title>.
// This keeps tooling simple (no frameworks or extra dependencies).

const fs = require("fs");
const path = require("path");

const pages = ["index.html", "staff.html"];
let failed = false;

for (const page of pages) {
  const file = path.join(__dirname, "..", page);
  if (!fs.existsSync(file)) {
    console.error("Missing page: " + page);
    failed = true;
    continue;
  }
  const html = fs.readFileSync(file, "utf8");
  const checks = [
    ["<title>", html.includes("<title>")],
    ["</title>", html.includes("</title>")],
    ["</html>", html.includes("</html>")],
  ];
  for (const [label, ok] of checks) {
    if (!ok) {
      console.error(page + " is missing " + label);
      failed = true;
    }
  }
}

if (failed) {
  process.exit(1);
}
console.log("Frontend lint passed.");
