const fs = require('fs');
const path = require('path');

const outDir = path.join(__dirname, 'public', 'google_tiles');
if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

// Creech AFB Center at Zoom 16: x = 11710, y = 25602
const z = 16;
const startX = 11707;
const startY = 25599;
const gridSize = 8; // 8x8 = 64 tiles (covering ~4km x 4km at sub-meter resolution)

async function run() {
  console.log('Downloading Google Satellite tiles...');
  const tasks = [];

  for (let row = 0; row < gridSize; row++) {
    for (let col = 0; col < gridSize; col++) {
      const tileX = startX + col;
      const tileY = startY + row;
      const url = `https://mt1.google.com/vt/lyrs=s&x=${tileX}&y=${tileY}&z=${z}`;
      const filePath = path.join(outDir, `tile_${row}_${col}.jpg`);

      tasks.push(
        fetch(url)
          .then((res) => {
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.arrayBuffer();
          })
          .then((buf) => {
            fs.writeFileSync(filePath, Buffer.from(buf));
          })
          .catch((err) => {
            console.error(`Error on tile ${row}_${col}:`, err.message);
          })
      );
    }
  }

  await Promise.all(tasks);
  console.log('All Google Satellite tiles successfully downloaded to public/google_tiles!');
}

run();
