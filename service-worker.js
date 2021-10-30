for (let i of ['install', 'activate', 'fetch']) {
	self.addEventListener(i, (event) => {
		console.log('[ServiceWorker] ' + i);
	});
}
