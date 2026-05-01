const CACHE_NAME = 'lifestream-v2';
const ASSETS = [
  '/',
  '/static/images/bg.png',
  '/static/manifest.json',
  '/static/images/icon.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request).catch(() => {
          // If network fails and it's a page request, show offline info
          if (event.request.mode === 'navigate') {
              return caches.match('/offline');
          }
      });
    })
  );
});
