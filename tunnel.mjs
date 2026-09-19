import { startTunnel } from 'untun';
import fs from 'node:fs';

async function main() {
  console.log('='.repeat(70));
  console.log('  RUSTOM-II MALE UAV SIMULATOR - SECURE PUBLIC INTERNET TUNNEL');
  console.log('='.repeat(70));
  console.log('  [+] Forwarding local server: http://localhost:3000');
  console.log('  [+] Initializing Cloudflare secure edge tunnel...\n');

  try {
    const tunnel = await startTunnel({ port: 3000 });
    const publicUrl = await tunnel.getURL();
    try {
      fs.writeFileSync('tunnel_url.txt', publicUrl, 'utf8');
    } catch (err) {}

    // Inform local backend of public tunnel URL with retries
    for (let attempt = 1; attempt <= 15; attempt++) {
      try {
        const resp = await fetch('http://localhost:3000/api/tunnel-info', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ publicUrl })
        });
        if (resp.ok) break;
      } catch (e) {
        await new Promise((r) => setTimeout(r, 1000));
      }
    }

    console.log('='.repeat(70));
    console.log('  PUBLIC LIVE URL (Worldwide WebGL Simulation):');
    console.log(`  >>> ${publicUrl} <<<`);
    console.log('='.repeat(70));
    console.log('  MOBILE RC CONTROLLER URL (Open on your phone):');
    console.log(`  >>> ${publicUrl}/?mode=remote <<<`);
    console.log('='.repeat(70));
    console.log('\n  * Scan QR code or open the link on your phone to fly the drone!');
    console.log('  * Works worldwide over 4G/5G mobile internet & Wi-Fi.');
    console.log('  * Keep this process running to keep the tunnel alive.');
    console.log('  * Press Ctrl+C to close.\n');
  } catch (error) {
    console.error('Error starting Cloudflare tunnel:', error);
  }
}

main();
