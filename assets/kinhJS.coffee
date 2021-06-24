---
# placholder for Jekyll to recognize this file
---

y = 'yesssss' # to save some data
dkey = 'dark' # keyword for dark theme
stdSpace = '0.5em' # for ruby annotation spacing
prevScrollPos = 0 # placeholder value
hamburgerHeight = '0' # placeholder value

Element.prototype.isEmpty = -> # new method for all elements
	return this.textContent.trim() == "" # cleaning + make sure it's empty

Element.prototype.toggleShowHide = (boolean) ->
	this.style.display = if boolean then 'unset' else 'none'

lang_change_ev = document.createEvent('HTMLEvents') # to replace jQuery trigger
lang_change_ev.initEvent('change', true, false)

$(window).on({
	'scroll': -> # when scroll down, hide the topbar, when scroll up, show the topbar
		currentScrollPos = document.documentElement.scrollTop
		effectScrollPos = if currentScrollPos > 500 then currentScrollPos else 0 # meaningful only
		pxToHide = if prevScrollPos > effectScrollPos then '0' else hamburgerHeight # value def below
		document.getElementById("hamburger").style.top = pxToHide # cannot use toggle because of sticky position
		prevScrollPos = effectScrollPos
		return null
	, # attention comma

	'load': ->

		hamburgerHeight = "-#{$('#hamburger').outerHeight(true)}px"

		# adjust space within ruby annotation # ATTENTION ORDER
		Array.from(document.getElementsByTagName('rb')).forEach rubyAdjust # for each ruby base

		# hamburger button: open sidenav
		document.querySelector('#hamburger > button').addEventListener 'click', () => open_close_sidenav 'open'

		# close sidenav when clicking a link or the main content: delegate to all children of #sidenav
		Array.from(document.getElementById('sidenav').children).forEach (el) => el.addEventListener 'click', () => open_close_sidenav 'close'

		# langForm checkboxes: show/hide langs
		for langg in ['en', 'fr', 'de', 'it', 'zh-Hant'] # zh-Hant: compatibility with old site
			if window.localStorage.getItem(langg) == y # check previous state
				document.querySelector("#langForm input[value=#{langg}]").checked = true
		Array.from(document.querySelectorAll('#langForm input')).forEach (el) ->
			el.addEventListener 'change', langToggle
			el.dispatchEvent lang_change_ev # check initial state

		# dark mode toggle
		$('#themeSwitch').on 'change', darkToggle
		dstate = window.localStorage.getItem(dkey)
		if dstate == y or (dstate is null and window.matchMedia("(prefers-color-scheme: #{dkey})").matches)
			$('#themeSwitch').prop 'checked', true # pre-check the dark-theme checkbox
		$('#themeSwitch').trigger 'change' # check initial state

		# remove the loader as page loaded
		$('main').css 'filter', 'none'
		$('#loader').remove()

		return null

})

# adjust space within ruby annotation
rubyAdjust = (el) -> # for each ruby base
	rt_elem = el.nextElementSibling
	if rt_elem.isEmpty() # punctuation (case of zh)
		addSpace = '0'
	else
		rbW = el.clientWidth # take its width
		rtW = rt_elem.clientWidth # its associated ruby text width
		diff = (rtW - rbW).toFixed(0) # excess amount
		next_rb_elem = rt_elem.nextElementSibling # next character
		if not next_rb_elem? or next_rb_elem.nextElementSibling.isEmpty() # end of sentence or before punctuation
			addSpace = if diff > 0 then "#{diff}px" else '0'
		else # normal
			addSpace = if diff > 0 then "calc(#{stdSpace} + #{diff}px)" else stdSpace
	el.style.marginRight = addSpace
	return null

open_close_sidenav = (cmd) ->
	switch cmd
		when 'open' # hamburger button: open sidenav
			sidenav_style = 'min(700px, 75%)'
			body_style = 'blur(5px)'
		when 'close' # sidenav links: close sidenav
			sidenav_style = '0'
			body_style = 'none'
		else throw 'not recognized command'

	document.getElementById("sidenav").style.width = sidenav_style
	Array.from(document.body.children).forEach (el) => if el.id != 'sidenav' then el.style.filter = body_style
	return null

# langForm checkboxes: show/hide langs
langToggle = ->
	lang = this.value
	checked = this.checked

	Array.from(document.querySelectorAll("h2 :lang(#{lang}), h3 :lang(#{lang}), .multi-lang :lang(#{lang}), .wait-multi-lang :lang(#{lang}), .mantra-seg :lang(#{lang})")).forEach (el) ->
		el.toggleShowHide checked # checked = shown, unchecked = hidden
		prev_el = el.previousElementSibling # also line break
		if prev_el? and prev_el.tagName.toLowerCase() == "br" # check existence first
			prev_el.toggleShowHide checked

	if checked
		window.localStorage.setItem lang, y
	else
		window.localStorage.removeItem lang
	return null

# dark mode toggle
darkToggle = ->
	if this.checked
		document.body.setAttribute 'data-theme', dkey
		this.nextSibling.textContent = '\uD83C\uDF19' # 🌙 surrogate pair
		window.localStorage.setItem dkey, y
	else
		document.body.removeAttribute 'data-theme'
		this.nextSibling.textContent = '\u2600\uFE0F' # ☀️ surrogate pair
		window.localStorage.setItem dkey, 'tdyutrghjtucvghjtc' # something random not important
	return null
