---
# placholder for Jekyll to recognize this file
---

'use strict'

y = 'yesssss' # to save some data
dkey = 'dark' # keyword for dark theme
prevScrollPos = hamburgerHeight = 0 # placeholder global value
langElemMap = new Map # cache all elem of each lang

Element.prototype.isEmpty = -> # new method for all elements
	return this.textContent.trim() == "" # cleaning + make sure it's empty

Element.prototype.toggleShowHide = (boolean) ->
	this.style.display = if boolean then 'unset' else 'none'

window.onload = =>

	hamburger = document.getElementById 'hamburger' # save this to avoid repetition
	hamburgerStyle = window.getComputedStyle hamburger
	hamburgerHeight = hamburger.offsetHeight + parseInt(hamburgerStyle.getPropertyValue 'margin-top') + parseInt(hamburgerStyle.getPropertyValue 'margin-bottom')

	# hamburger button: open sidenav
	hamburger.querySelector('button').onclick = open_sidenav

	# close sidenav when clicking a link or the main content: delegate to all children of #sidenav
	sidenav = document.getElementById 'sidenav' # save this to avoid repetition
	for el in sidenav.children
		el.onclick = close_sidenav

	# langForm checkboxes: show/hide langs
	langForm = document.getElementById 'langForm' # save this to avoid repetition
	for langg in ['en', 'fr', 'de', 'it']
		# save the string because it's too long
		queryString = "h2 :lang(#{langg}), h3 :lang(#{langg}), .multi-lang :lang(#{langg}), .wait-multi-lang :lang(#{langg}), .mantra-seg :lang(#{langg})"
		langElemMap.set langg, document.querySelectorAll queryString # cache all elem of each lang
		if window.localStorage.getItem(langg) == y # check previous state
			langForm.querySelector("input[value=#{langg}]").checked = true

	for el in langForm.querySelectorAll 'input'
		el.onchange = langToggle
		el.onchange() # check initial state

	# dark mode toggle
	themeSwitch = document.getElementById 'themeSwitch' # save this to avoid repetition
	themeSwitch.onchange = darkToggle
	dstate = window.localStorage.getItem dkey
	if dstate == y or (not dstate? and window.matchMedia("(prefers-color-scheme: #{dkey})").matches)
		themeSwitch.checked = true # pre-check the dark-theme checkbox
	themeSwitch.onchange() # check initial state

	# remove the loader as page loaded
	document.getElementsByTagName('main')[0].style.filter = 'none'
	document.getElementById('loader').remove()

window.onscroll = => # when scroll down, hide the topbar, when scroll up, show the topbar
	currentScrollPos = document.documentElement.scrollTop
	effectScrollPos = if currentScrollPos > 500 then currentScrollPos else 0 # meaningful only
	pxToHide = if prevScrollPos > effectScrollPos then '0' else "-#{hamburgerHeight}px"# value def below
	hamburger.style.top = pxToHide # cannot use toggle because of sticky position
	prevScrollPos = effectScrollPos

window.onpopstate = (e) => # event: click back/forward button in browser
	# change url without reloading
	fetch window.location.pathname
		.then (response) => response.text()
		.then (newPageHTML) => # ATTENTION no window.history.pushState
			document.body.innerHTML = newPageHTML
			window.onload()

open_sidenav = ->
	sidenav.style.width = 'min(700px, 75%)' # case of small screen = 75%
	for el in document.body.children
		if el.id != 'sidenav' then el.style.filter = 'blur(5px)'

close_sidenav = ->
	sidenav.style.width = '0'
	for el in document.body.children
		if el.id != 'sidenav' then el.style.filter = 'none'

# langForm checkboxes: show/hide langs
langToggle = ->
	lang = this.value
	checked = this.checked

	# show/hide
	for el in langElemMap.get(lang)
		elLangShowHide el, checked

	# save state
	if checked
		window.localStorage.setItem lang, y
	else
		window.localStorage.removeItem lang

# show/hide elem of lang
elLangShowHide = (el, checked) ->
	el.toggleShowHide checked # checked = shown, unchecked = hidden
	prev_el = el.previousElementSibling # also line break
	if prev_el? and prev_el.tagName.toLowerCase() == 'br' # check existence first
		prev_el.toggleShowHide checked

# dark mode toggle
darkToggle = ->
	if this.checked
		document.documentElement.setAttribute 'data-theme', dkey # do not set for <body> because it breaks position fixed of sidenav
		this.nextSibling.textContent = '\uD83C\uDF19' # \u{1F319} 🌙 surrogate pair
		window.localStorage.setItem dkey, y # save state
	else
		document.documentElement.removeAttribute 'data-theme'
		this.nextSibling.textContent = '\u2600\uFE0F' # ☀️ with modifier
		window.localStorage.setItem dkey, 'tdyutrghjtucvghjtc' # something random not important
