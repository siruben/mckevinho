/* Service worker: deixa o jogo funcionar offline. Sobe o número da versão a cada alteração. */
const VERSION = 'chuva-brigadeiro-v13';
const FILES = [
  './', 'index.html', 'manifest.json',
  'icons/icon-192.png', 'icons/icon-512.png', 'icons/icon-maskable-512.png', 'icons/apple-touch-icon.png',
  'assets/palco.jpg', 'assets/kevinho.png', 'assets/brigadeiro.png',
  'audio/intro-cai-brigadeiro.mp3', 'audio/musica-mc-kevinho.mp3',
  'audio/game-over-brigadeiros.m4a', 'audio/game-over-brigadeiros.webm'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(FILES.map(f => new Request(f, { cache: 'reload' })))).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});

// O áudio pede intervalos de bytes (Range); a cache guarda o ficheiro inteiro, por isso fatiamos aqui.
async function rangeFrom(req, res) {
  const buf = await res.arrayBuffer(), len = buf.byteLength;
  const m = /bytes=(\d*)-(\d*)/.exec(req.headers.get('range') || '');
  if (!m) return res;
  let start = m[1] === '' ? Math.max(0, len - Number(m[2])) : Number(m[1]);
  let end = m[1] === '' || m[2] === '' ? len - 1 : Math.min(Number(m[2]), len - 1);
  if (start >= len) return new Response(null, { status: 416, headers: { 'Content-Range': `bytes */${len}` } });
  return new Response(buf.slice(start, end + 1), {
    status: 206, statusText: 'Partial Content',
    headers: { 'Content-Type': res.headers.get('Content-Type') || 'application/octet-stream',
               'Content-Range': `bytes ${start}-${end}/${len}`, 'Content-Length': String(end - start + 1), 'Accept-Ranges': 'bytes' }
  });
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;

  // Página: tenta a rede (para apanhar atualizações) e cai para a cache se estiver offline
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).then(r => { const copy = r.clone(); caches.open(VERSION).then(c => c.put('index.html', copy)); return r; })
        .catch(() => caches.match('index.html', { ignoreSearch: true }).then(r => r || caches.match('./', { ignoreSearch: true })))
    );
    return;
  }
  // Resto: cache primeiro
  e.respondWith((async () => {
    const hit = await caches.match(req, { ignoreSearch: true });
    const res = hit || await fetch(req);
    return req.headers.has('range') && res.status === 200 ? rangeFrom(req, res) : res;
  })());
});
