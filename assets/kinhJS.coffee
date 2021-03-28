---
# placholder for Jekyll to recognize this file
---

y = 'yesssss' # to save some data
dkey = 'dark' # keyword for dark theme
stdSpace = '1em' # for ruby annotation spacing
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

		hamburgerHeight = "-#{$('#hamburger').outerHeight(true).toString()}px"

		# set locale for Viet ruby annotation of Chinese texts (font rendering problem)
		$('rt:lang(zh-Hant)').attr 'lang', 'vi'

		# insert carriage return character to improve readability when wrapping text
		$('.multi-lang br, .wait-multi-lang br').before '<span class="CR-LF">&nbsp;↵</span>'

		# change font style
		$('.mantra-seg span:lang(vi), .multi-lang rt:lang(vi), .wait-multi-lang rt:lang(vi)').addClass 'in-dam'
		$('.mantra-seg span:lang(sa), .multi-lang ruby:lang(sa), .wait-multi-lang ruby:lang(sa), .multi-lang ruby:lang(pi)').addClass 'to-vang'

		# adjust space within ruby annotation # ATTENTION ORDER
		$('rb').each rubyAdjust # for each ruby base

		# hamburger button: open sidenav
		$('#hamburger button:has(svg)').on 'click', openNav

		# close sidenav when clicking a link or the main content
		$('#sidenav, main').on 'click', closeNav # also delegate to all children of #sidenav

		# langForm checkboxes: show/hide langs
		$('#langForm').on 'change', 'input', langToggle
		for langg in ['en', 'fr', 'de', 'it'] # check previous state
			if window.localStorage.getItem(langg) == y
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
	rbW = $(el).width() # take its width
	rtW = $(el).next('rt').width() # its associated ruby text width
	diff = (rtW - rbW).toFixed(0) # excess amount
	addSpace = if diff > 0 then "calc(#{stdSpace} + #{diff.toString()}px)" else stdSpace
	$(el).css 'margin-right', addSpace
	return null

# hamburger button: open sidenav
openNav = ->
	$('#sidenav').css 'width', 'min(700px, 75%)'
	$('#page-header, #hamburger, main').css 'filter', 'blur(5px)'
	return null

# sidenav links: close sidenav, also close top bar
closeNav = ->
	$('#sidenav').css 'width', '0'
	$('#page-header, #hamburger, main').css 'filter', 'none'
	return null

# langForm checkboxes: show/hide langs
langToggle = ->
	langCheck = $(this).val()
	checked = $(this).prop 'checked'

	$ ":lang(#{langCheck})"
		.toggle checked  # checked = shown, unchecked = hidden
		.prev('br').toggle checked # also line break
	$ ".multi-lang > span:lang(#{langCheck})"
		.prev('br').prev('span.CR-LF').toggle checked # also carriage return character

	if checked
		window.localStorage.setItem langCheck, y
	else
		window.localStorage.removeItem langCheck
	return null

# dark mode toggle
darkToggle = ->
	if $(this).prop 'checked'
		$('html').attr 'data-theme', dkey
		this.nextSibling.textContent = '🌙' # no jQuery equivalent
		window.localStorage.setItem dkey, y
	else
		$('html').removeAttr 'data-theme'
		this.nextSibling.textContent = '☀️' # no jQuery equivalent
		window.localStorage.setItem dkey, 'tdyutrghjtucvghjtc' # something not important
	return null
