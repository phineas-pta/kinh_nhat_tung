---
# placholder for Jekyll to recognize this file
---

y = 'yesssss' # to save some data
dkey = 'dark' # keyword for dark theme
stdSpace = '0.5em' # for ruby annotation spacing
prevScrollPos = 0 # placeholder value
hamburgerHeight = '0' # placeholder value
langElemMap = new Map() # cache all elem of each lang

Element.prototype.isEmpty = -> # new method for all elements
	return this.textContent.trim() == "" # cleaning + make sure it's empty

Element.prototype.toggleShowHide = (boolean) ->
	this.style.display = if boolean then 'unset' else 'none'

checkbox_change_ev = document.createEvent 'HTMLEvents' # to replace jQuery trigger
checkbox_change_ev.initEvent 'change', true, false

window.addEventListener 'load', ->

	hamburger = document.getElementById 'hamburger' # save this to avoid repetition
	hamburgerHeight = hamburger.offsetHeight
	hamburgerStyle = getComputedStyle(hamburger)
	hamburgerHeight += parseInt(hamburgerStyle.marginTop) + parseInt(hamburgerStyle.marginBottom)

	# hamburger button: open sidenav
	document.querySelector('#hamburger > button').addEventListener 'click', open_sidenav

	# close sidenav when clicking a link or the main content: delegate to all children of #sidenav
	sidenav = document.getElementById 'sidenav' # save this to avoid repetition
	Array.from(sidenav.children).forEach (el) => el.addEventListener 'click', close_sidenav

	# langForm checkboxes: show/hide langs
	langForm = document.getElementById 'langForm' # save this to avoid repetition
	for langg in ['en', 'fr', 'de', 'it']
		# save the string because it's too long
		queryString = "h2 :lang(#{langg}), h3 :lang(#{langg}), .multi-lang :lang(#{langg}), .wait-multi-lang :lang(#{langg}), .mantra-seg :lang(#{langg})"
		langElemMap.set langg, Array.from document.querySelectorAll queryString
		if window.localStorage.getItem(langg) == y # check previous state
			langForm.querySelector("input[value=#{langg}]").checked = true

	Array.from(langForm.querySelectorAll 'input').forEach (el) ->
		el.addEventListener 'change', langToggle
		el.dispatchEvent checkbox_change_ev # check initial state

	# dark mode toggle
	themeSwitch = document.getElementById 'themeSwitch' # save this to avoid repetition
	themeSwitch.addEventListener 'change', darkToggle
	dstate = window.localStorage.getItem dkey
	if dstate == y or (not dstate? and window.matchMedia("(prefers-color-scheme: #{dkey})").matches)
		themeSwitch.checked = true # pre-check the dark-theme checkbox
	themeSwitch.dispatchEvent checkbox_change_ev # check initial state

	# remove the loader as page loaded
	document.getElementsByTagName('main')[0].style.filter = 'none'
	document.body.removeChild document.getElementById 'loader'

	return null

window.addEventListener 'scroll', -> # when scroll down, hide the topbar, when scroll up, show the topbar
	currentScrollPos = document.documentElement.scrollTop
	effectScrollPos = if currentScrollPos > 500 then currentScrollPos else 0 # meaningful only
	pxToHide = if prevScrollPos > effectScrollPos then '0' else "-#{hamburgerHeight}px"# value def below
	hamburger.style.top = pxToHide # cannot use toggle because of sticky position
	prevScrollPos = effectScrollPos
	return null

open_sidenav = ->
	sidenav.style.width = 'min(700px, 75%)' # case of small screen = 75%
	Array.from(document.body.children).forEach (el) => if el.id != 'sidenav' then el.style.filter = 'blur(5px)'
	return null

close_sidenav = ->
	sidenav.style.width = '0'
	Array.from(document.body.children).forEach (el) => if el.id != 'sidenav' then el.style.filter = 'none'
	return null

# langForm checkboxes: show/hide langs
langToggle = ->
	lang = this.value
	checked = this.checked

	langElemMap.get(lang).forEach (el) => elLangShowHide el, checked

	if checked
		window.localStorage.setItem lang, y
	else
		window.localStorage.removeItem lang
	return null

# show/hide elem of lang
elLangShowHide = (el, checked) ->
	el.toggleShowHide checked # checked = shown, unchecked = hidden
	prev_el = el.previousElementSibling # also line break
	if prev_el? and prev_el.tagName.toLowerCase() == 'br' # check existence first
		prev_el.toggleShowHide checked
	return null

# dark mode toggle
darkToggle = ->
	if this.checked
		document.documentElement.setAttribute 'data-theme', dkey # do not set for <body> because it breaks position fixed of sidenav
		this.nextSibling.textContent = '\uD83C\uDF19' # \u{1F319} 🌙 surrogate pair
		window.localStorage.setItem dkey, y
	else
		document.documentElement.removeAttribute 'data-theme'
		this.nextSibling.textContent = '\u2600\uFE0F' # ☀️ with modifier
		window.localStorage.setItem dkey, 'tdyutrghjtucvghjtc' # something random not important
	return null
