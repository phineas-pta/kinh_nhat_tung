---
# placholder for Jekyll to recognize this file
---

y = 'yesssss' # to save some data
dkey = 'dark' # keyword for dark theme
stdSpace = '0.5em' # for ruby annotation spacing
prevScrollPos = 0 # placeholder value
hamburgerHeight = '0' # placeholder value

$(window).on({
	'scroll': -> # when scroll down, hide the topbar, when scroll up, show the topbar
		currentScrollPos = $(window).scrollTop()
		effectScrollPos = if currentScrollPos > 500 then currentScrollPos else 0 # meaningful only
		pxToHide = if prevScrollPos > effectScrollPos then '0' else hamburgerHeight # value def below
		$('#hamburger').css 'top', pxToHide # cannot use toggle because of sticky position
		prevScrollPos = effectScrollPos
		return null
	,

	'load': ->

		hamburgerHeight = "-#{$('#hamburger').outerHeight(true)}px"

		# set locale for Viet ruby annotation of Chinese texts (font rendering problem)
		$('rt:lang(zh-Hant)').attr 'lang', 'vi'

		# adjust space within ruby annotation # ATTENTION ORDER
		$('rb').each rubyAdjust # for each ruby base

		# hamburger button: open sidenav
		$('#hamburger button:has(svg)').on 'click', {cmd: 'open'}, open_close_sidenav

		# close sidenav when clicking a link or the main content
		$('#sidenav').on 'click', {cmd: 'close'}, open_close_sidenav # also delegate to all children of #sidenav

		# langForm checkboxes: show/hide langs
		$('#langForm').on 'change', 'input', langToggle
		for langg in ['en', 'fr', 'de', 'it', 'zh-Hant'] # compatibility with old site
			if window.localStorage.getItem(langg) == y # check previous state
				$("#langForm input[value=#{langg}]").prop "checked", true
		$('#langForm input').trigger 'change' # check initial state

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
rubyAdjust = (i, el) -> # for each ruby base
	rt_elem = $(el).next()
	if $(rt_elem).is(':empty') # punctuation (case of zh)
		addSpace = '0'
	else
		rbW = $(el).width() # take its width
		rtW = $(rt_elem).width() # its associated ruby text width
		diff = (rtW - rbW).toFixed(0) # excess amount
		next_rb_elem = $(rt_elem).next() # next character
		if $(next_rb_elem).length == 0 or $(next_rb_elem).next().is(':empty') # end of sentence or before punctuation
			addSpace = if diff > 0 then "#{diff}px" else '0'
		else # normal
			addSpace = if diff > 0 then "calc(#{stdSpace} + #{diff}px)" else stdSpace
	$(el).css 'margin-right', addSpace
	return null

open_close_sidenav = (event) ->
	switch event.data.cmd
		when 'open' # hamburger button: open sidenav
			sidenav_style = 'min(700px, 75%)'
			body_style = 'blur(5px)'
		when 'close' # sidenav links: close sidenav
			sidenav_style = '0'
			body_style = 'none'
		else throw 'not recognized command'

	$('#sidenav').css 'width', sidenav_style
	$('body > *:not(#sidenav)').css 'filter', body_style
	return null

# langForm checkboxes: show/hide langs
langToggle = ->
	lang = $(this).val()
	checked = $(this).prop 'checked'

	$ "header :lang(#{lang}), .multi-lang :lang(#{lang}), .wait-multi-lang :lang(#{lang}), .mantra-seg :lang(#{lang})"
		.toggle checked  # checked = shown, unchecked = hidden
		.prev('br').toggle checked # also line break

	if checked
		window.localStorage.setItem lang, y
	else
		window.localStorage.removeItem lang
	return null

# dark mode toggle
darkToggle = ->
	if $(this).prop 'checked'
		$('html').attr 'data-theme', dkey
		this.nextSibling.textContent = '\uD83C\uDF19' # 🌙 surrogate pair
		window.localStorage.setItem dkey, y
	else
		$('html').removeAttr 'data-theme'
		this.nextSibling.textContent = '\u2600\uFE0F' # ☀️ surrogate pair
		window.localStorage.setItem dkey, 'tdyutrghjtucvghjtc' # something random not important
	return null
