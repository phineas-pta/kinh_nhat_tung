const
	cacheName = 'mycache-v1', // update ver to update cache
	cacheContent = [
		'/kinh_nhat_tung/index.html',
		'/kinh_nhat_tung/assets/kinhJS.js',
		'/kinh_nhat_tung/assets/kinhCSS.css',
		'/kinh_nhat_tung/assets/fonts/Charmonman-Regular.woff2',
		'/kinh_nhat_tung/assets/fonts/GrenzeGotisch-ExtraBold.woff2',
		'/kinh_nhat_tung/assets/fonts/MuseoModerno-Regular.woff2',
		'/kinh_nhat_tung/assets/fonts/NotoSansSiddham-Regular.woff2',
		'/kinh_nhat_tung/assets/fonts/UKaiHK-02.woff2',
	]
;

// initialize the cache and add files to it for offiline use
self.addEventListener('install', (e) => {
	console.log('[Servic Worker] installing');
	e.waitUntil((async () => {
		const cache = await caches.open(cacheName);
		console.log('[Servic Worker] caching fonts');
		await cache.addAll(cacheContent);
	})());
});

// clear old cache
self.addEventListener('activate', (e) => {
	console.log('[Servic Worker] activating');
	e.waitUntil(caches.keys().then((keyList) => {
		return Promise.all(keyList.map((key) => {
			if (key === cacheName) {
				return;
			} else {
				return caches.delete(key);
			}
		}));
	}));
});

// retrieve from server, if offline then retrieve from cache
self.addEventListener('fetch', (e) => {
	console.log(`[Servic Worker] fetching resource ${e.request.url}`);
	e.respondWith(async () => {
		try {
			var
				res = await fetch(e.request),
				cache = await caches.open(cacheName)
			;
			cache.put(e.request, res.clone());
			return res;
		} catch (error) {
			return caches.match(e.request);
		}
	});
});
