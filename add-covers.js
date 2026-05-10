const fs = require('fs');
const path = require('path');

const reviewsDir = '/Users/mike/.openclaw/workspace-bacottibot/websites/bithues-hugo-work/hugo-src/content/reviews/';
const files = fs.readdirSync(reviewsDir).filter(f => f.endsWith('.md'));

let updated = 0;
let skipped = 0;

for (const file of files) {
  const filePath = path.join(reviewsDir, file);
  let content = fs.readFileSync(filePath, 'utf8');

  // Extract ISBN
  const isbnMatch = content.match(/^isbn:\s*"?([^"\n]+)"?/m);
  if (!isbnMatch) {
    console.log(`No ISBN for ${file}, skipping`);
    skipped++;
    continue;
  }
  const isbn = isbnMatch[1].trim();
  const coverUrl = `https://covers.openlibrary.org/b/isbn/${isbn}-M.jpg`;

  // Add or replace cover field
  if (/^cover:\s*/m.test(content)) {
    content = content.replace(/^cover:\s*[^\n]+\n/m, `cover: "${coverUrl}"\n`);
  } else {
    // Add cover after isbn line
    content = content.replace(/^isbn:\s*[^\n]+\n/m, `isbn: "${isbn}"\ncover: "${coverUrl}"\n`);
  }

  fs.writeFileSync(filePath, content);
  updated++;
  console.log(`Updated ${file} → ${coverUrl}`);
}

console.log(`\nTotal updated: ${updated}, skipped: ${skipped}`);
