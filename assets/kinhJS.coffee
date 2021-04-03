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
		$('#hamburger button:has(svg)').on 'click', openNav

		# close sidenav when clicking a link or the main content
		$('#sidenav, main').on 'click', closeNav # also delegate to all children of #sidenav

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
	if $(rt_elem).is(':empty') # punctuation
		addSpace = "0"
	else
		next_rb_elem = $(rt_elem).next()
		if $(next_rb_elem).length == 0 # end of sentence
			addSpace = "0"
		else if $(next_rb_elem).next().is(':empty') # punctuation
			addSpace = "0"
		else
			rbW = $(el).width() # take its width
			rtW = $(rt_elem).width() # its associated ruby text width
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

	$ "article header :lang(#{langCheck}), .multi-lang :lang(#{langCheck}), .wait-multi-lang :lang(#{langCheck})"
		.toggle checked  # checked = shown, unchecked = hidden
		.prev('br').toggle checked # also line break

	if checked
		window.localStorage.setItem langCheck, y
	else
		window.localStorage.removeItem langCheck
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
		window.localStorage.setItem dkey, 'tdyutrghjtucvghjtc' # something not important
	return null
