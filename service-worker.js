for (let i of ['install', 'activate', 'fetch']) {
	self.addEventListener(i, (event) => {
		console.log('[ServiceWorker] ' + i);
	});
}

importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

workbox.routing.registerRoute(
	new RegExp('/*'),
	new workbox.strategies.StaleWhileRevalidate({
		cacheName: 'offline'
	})
);

workbox.routing.registerRoute(
	new RegExp('/*'),
	new workbox.strategies.CacheFirst({
		cacheName: 'precache'
	})
);
