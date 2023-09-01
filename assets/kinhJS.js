---
layout: none
search: exclude
sitemap: false
---

"use strict";

// placeholder global value
const y = "yesssss", dkey = "dark"; // keyword for dark theme
var sidenav, // used in open_sidenav & close_sidenav
    prevScrollPos = 0,
    hamburgerHeight = 0, // used in onscroll
    langElemMap = new Map; // cache all elem of each lang

// PWA things
if ("serviceWorker" in navigator) navigator.serviceWorker
	.register("{{ site.baseurl }}/service-worker.js")
	.then(() => console.log("register service worker for pwa"))
	.catch(() => console.error("pwa failed"));

// when everything ready
window.onload = () => {

	var hamburger = document.getElementById("hamburger"),
	    hamburgerStyle = window.getComputedStyle(hamburger);
	hamburgerHeight = hamburger.offsetHeight
		+ parseInt(hamburgerStyle.getPropertyValue("margin-top"))
		+ parseInt(hamburgerStyle.getPropertyValue("margin-bottom"));

	sidenav = document.getElementById("sidenav");
	for (let el of sidenav.querySelectorAll("a"))
		el.onclick = noHistoryChange; // def below

	// hamburger button: open sidenav
	hamburger.querySelector("button").onclick = open_sidenav; // def below

	// close sidenav when clicking a link or the main content: delegate to all children of #sidenav
	for (let el of sidenav.children)
		el.onclick = close_sidenav; // def below

	// langForm checkboxes: show/hide langs
	var langForm = document.getElementById("langForm");
	for (let lg of ["en", "fr", "de", "it"]) {
		// save the string because it's too long
		var queryString = `h2 :lang(${lg}), h3 :lang(${lg}), .multi-lang :lang(${lg}), .wait-multi-lang :lang(${lg}), .mantra-seg :lang(${lg})`;
		langElemMap.set(lg, document.querySelectorAll(queryString)); // cache all elem of each lang
		if (window.localStorage.getItem(lg) === y) // check previous state
			langForm.querySelector(`input[value=${lg}]`).checked = true;
	}
	for (let el of langForm.getElementsByTagName("input")) {
		el.onchange = langToggle;
		el.onchange(); // check initial state
	}

	// dark mode toggle
	var themeSwitch = document.getElementById("themeSwitch");
	themeSwitch.onchange = darkToggle;
	var dstate = window.localStorage.getItem(dkey);
	if (dstate === y || (dstate == null && window.matchMedia(`(prefers-color-scheme: ${dkey})`).matches))
		themeSwitch.checked = true; // pre-check the dark-theme checkbox
	themeSwitch.onchange(); // check initial state

	// auto create clickable links
	for (let el of document.querySelectorAll("a.my-ref")) {
		el.setAttribute("href", el.textContent);
		el.setAttribute("target", "_blank");
		el.setAttribute("rel", "noreferrer");
	}

	// remove the loader once page loaded
	document.getElementsByTagName("main")[0].style.filter = "none";
	document.getElementById("loader").remove();
}

// when scroll down, hide the topbar, when scroll up, show the topbar
window.onscroll = () => {
	var currentScrollPos = document.documentElement.scrollTop;
	var effectScrollPos = currentScrollPos > 500 ? currentScrollPos : 0; // meaningful only
	var pxToHide = prevScrollPos > effectScrollPos ? "0" : `-${hamburgerHeight}px`; // value def below
	hamburger.style.top = pxToHide; // cannot use toggle because of sticky position
	prevScrollPos = effectScrollPos;
};

// event: click back/forward button in browser => change url without reloading
window.onpopstate = (e) => {
	fetch(window.location.pathname)
		.then((response) => response.text())
		.then((newPageHTML) => { // ATTENTION no window.history.pushState
			document.body.innerHTML = newPageHTML;
			window.onload();
		});
};

function open_sidenav() {
	sidenav.style.width = "min(700px, 75%)"; // case of small screen = 75%
	for (let el of document.body.children)
		if (el.id !== "sidenav")
			el.style.filter = "blur(5px)";
}

function close_sidenav() {
	sidenav.style.width = "0";
	for (let el of document.body.children)
		if (el.id !== "sidenav")
			el.style.filter = "none";
}

// langForm checkboxes: show/hide langs
function langToggle() {
	var lang = this.value,
	    checked = this.checked;

	// show/hide
	for (let el of langElemMap.get(lang))
		elLangShowHide(el, checked);

	// save state
	if (checked)
		return window.localStorage.setItem(lang, y);
	else
		return window.localStorage.removeItem(lang);
}

// show/hide elem of lang
function elLangShowHide(el, checked) {
	el.style.display = checked ? "unset" : "none"; // checked = shown, unchecked = hidden
	var prev_el = el.previousElementSibling; // also line break
	if ((prev_el != null) && prev_el.tagName.toLowerCase() === "br") // check existence first
		return prev_el.style.display = checked ? "unset" : "none";
}

// dark mode toggle
function darkToggle() {
	if (this.checked) {
		document.documentElement.setAttribute("data-theme", dkey); // do not set for <body> because it breaks position fixed of sidenav
		this.nextSibling.textContent = "\uD83C\uDF19"; // \u{1F319} 🌙 surrogate pair
		return window.localStorage.setItem(dkey, y); // save state
	} else {
		document.documentElement.removeAttribute("data-theme");
		this.nextSibling.textContent = "\u2600\uFE0F"; // ☀️ with modifier
		return window.localStorage.setItem(dkey, "tdyutrghjtucvghjtc"); // something random not important
	}
}

// change url without reloading
function noHistoryChange(event) {
	event.preventDefault(); // prevent loading when clicking
	fetch(this.href)
		.then((response) => response.text())
		.then((newPageHTML) => { // load the new page
			window.history.pushState(null, null, this.href); // change url
			document.body.innerHTML = newPageHTML; // load page content
			window.onload(); // trigger redering
		})
	return null;
}
