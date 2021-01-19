const stdSpace = "1em"; // for ruby annotation spacing
var prevScrollPos = 0, hamburgerHeight = "0"; // placeholder value

$(window).on({
	"scroll": function () { // when scroll down, hide the topbar, when scroll up, show the topbar
		var currentScrollPos = $(window).scrollTop(),
		    effectScrollPos = (currentScrollPos > 500) ? currentScrollPos : 0, // meaningful only
		    pxToHide = prevScrollPos > effectScrollPos ? "0" : hamburgerHeight; // value def below
		$("#hamburger").css("top", pxToHide); // cannot use toggle because of sticky position
		prevScrollPos = effectScrollPos;
	},

	"load": function () {

		hamburgerHeight = "-" + $("#hamburger").outerHeight(true).toString() + "px";

		// set locale for Viet ruby annotation of Chinese texts (font rendering problem)
		$("rt:lang(zh-Hant)").attr("lang", "vi");

		// insert carriage return character to improve readability when wrapping text
		$(".multi-lang br, .wait-multi-lang br").before('<span class="CR-LF">&nbsp;↵</span');

		// change font style
		$(".mantra-seg span:lang(vi),\
		   .multi-lang rt:lang(vi),\
		   .wait-multi-lang rt:lang(vi)").addClass("in-dam");
		$(".mantra-seg span:lang(sa),\
		   .multi-lang > :lang(sa),\
		   .multi-lang > :lang(pi)").addClass("to-vang");

		// adjust space within ruby annotation // ATTENTION ORDER
		$("rb").each(rubyAdjust); // for each ruby base

		// hamburger button: open sidenav
		$("#hamburger button:has(svg)").on("click", openNav);

		// close sidenav when clicking a link or the main content
		$("#sidenav, main").on("click", closeNav); // also delegate to all children of #sidenav

		// langForm checkboxes: show/hide langs
		$("#langForm").on("change", "input", langToggle);
		$("#langForm input").trigger("change"); // check initial state

		// dark mode toggle
		$("#themeSwitch").on("change", darkToggle);
		if (window.matchMedia("(prefers-color-scheme: dark)").matches) { // if dark-theme is set
			$("#themeSwitch").prop("checked", true); // pre-check the dark-theme checkbox
		}
		$("#themeSwitch").trigger("change"); // check initial state

		// tab navigation
		$("#tabPanel").on("click", "button", tabClick);
		$("#tabPanel > button[value='home']").trigger("click"); // select 'home' tab

		// remove the loader as page loaded
		$("main").css("filter", "none");
		$("#loader").remove();
	}
})


// adjust space within ruby annotation
function rubyAdjust(i, el) { // for each ruby base
	const rbW = $(el).width(), // take its width
	      rtW = $(el).next("rt").width(), // its associated ruby text width
	      diff = (rtW - rbW).toFixed(0), // excess amount
	      addSpace = diff > 0
	                 ? `calc(${stdSpace} + ${diff.toString()}px)`
	                 : stdSpace;
	$(el).css("margin-right", addSpace);
}

// hamburger button: open sidenav
function openNav() {
	$("#sidenav").css("width", "300px");
	$("#page-header, #hamburger, main").css("filter", "blur(5px)");
}

// sidenav links: close sidenav, also close top bar
function closeNav() {
	$("#sidenav").css("width", "0");
	$("#page-header, #hamburger, main").css("filter", "none");
}

// langForm checkboxes: show/hide langs
function langToggle() {
	const langCheck = $(this).val(),
	      checked = $(this).prop("checked");
	$(`:lang(${langCheck})`)
		.toggle(checked) // checked = shown, unchecked = hidden
		.prev("br").toggle(checked); // also line break
	$(`.multi-lang > span:lang(${langCheck})`)
		.prev("br").prev("span.CR-LF").toggle(checked); // also carriage return character
}

// dark mode toggle
function darkToggle() {
	if ($(this).prop("checked")) {
		$("html").attr("data-theme", "dark");
		this.nextSibling.textContent = "🌙"; // no jQuery equivalent
	} else {
		$("html").removeAttr("data-theme");
		this.nextSibling.textContent = "☀️"; // no jQuery equivalent
	}
}

// tab navigation
function tabClick() {
	// remove any class="current" then re-add to the selected tab
	$(this)
		.addClass("current-tab") // attention to operation order
		.siblings().removeClass("current-tab");
	// hide all elements with class="tabcontent" and show the selected one
	var tabName = $(this).val();
	$(".tabcontent, .tabcontent ~ hr").hide();
	$(`.tabcontent.${tabName}`)
		.show()
		.next("hr").show();
	// back to top + open side nav bar
	$(document).scrollTop(0);
	var itemsCount = $(`#sidenav > ul > section.${tabName} > li`).length;
	if (itemsCount > 1) {openNav();}
}

// insert HTML file using <iframe>, copy from somewhere
function importHTML(obj) {
	for (let ele of obj.contentWindow.document.body.children) { // access content
		obj.before(ele); // inject content
	}
	obj.remove(); // remove <iframe>
}
