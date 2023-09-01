---
layout: none
search: exclude
sitemap: false
---

// this file somehow must be at root dir

const cacheName = "mycache-v1", // update ver to update cache
      cacheContent = [
      	"{{ site.baseurl }}/index.html",
      	"{{ site.baseurl }}/assets/kinhJS.js",
      	"{{ site.baseurl }}/assets/kinhCSS.css",
      	{% for file in site.static_files %} {% if file.extname == ".woff2" %}
      	"{{ file.path | prepend: site.baseurl }}",
      	{% endif %} {% endfor %}
      ];

// initialize the cache and add files to it for offiline use
self.addEventListener("install", (e) => {
	console.log("[Servic Worker] installing");
	e.waitUntil(tmp0());
});

// clear old cache
self.addEventListener("activate", (e) => {
	console.log("[Servic Worker] activating");
	e.waitUntil(caches.keys().then(tmp1));
});

// retrieve from server, if offline then retrieve from cache
self.addEventListener("fetch", (e) => console.log(`[Servic Worker] fetching resource ${e.request.url}`));

async function tmp0() {
	const cache = await caches.open(cacheName);
	console.log("[Servic Worker] caching all");
	await cache.addAll(cacheContent);
}

function tmp1(keyList) {
	var yolo = keyList.map((key) => key === cacheName ? undefined : caches.delete(key));
	return Promise.all(yolo);
}
