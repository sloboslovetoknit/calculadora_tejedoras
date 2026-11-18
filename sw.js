// Permite que la calculadora funcione sin internet después de la primera visita.
// Siempre intenta traer la versión más nueva; si no hay internet, usa la copia guardada.
// No es necesario modificar este archivo cuando cambies la app.

const CACHE = "calculadora-tejedoras";
const ARCHIVOS = [
  "./",
  "index.html",
  "manifest.webmanifest",
  "icon-192.png",
  "icon-512.png",
  "apple-touch-icon.png",
  "Logo.png.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) =>
      Promise.all(ARCHIVOS.map((archivo) => cache.add(archivo).catch(() => {})))
    )
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  event.respondWith(
    fetch(event.request)
      .then((respuesta) => {
        const copia = respuesta.clone();
        caches.open(CACHE).then((cache) => cache.put(event.request, copia));
        return respuesta;
      })
      .catch(() => caches.match(event.request, { ignoreSearch: true }))
  );
});
