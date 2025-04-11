const CACHE_NAME = 'mi-app-cache-v1';
const urlsToCache = [
    '/offline-template-app-neeva', // Página que se mostrará cuando no haya conexión
];

self.addEventListener('install', function(event) {
    // Almacenar los recursos en caché durante la instalación del Service Worker
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                // Si el recurso está en caché, se devuelve, de lo contrario se hace una solicitud de red
                if (response) {
                    return response;
                }
                return fetch(event.request);
            }).catch(function() {
                // Si no hay conexión, se muestra la página offline.html
                return caches.match('/offline-template-app-neeva');
            })
    );
});

self.addEventListener('activate', function(event) {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
