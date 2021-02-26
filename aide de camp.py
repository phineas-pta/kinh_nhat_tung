# -*- coding: utf-8 -*-

import re, os, html, requests as req

def escapeHTML(txt: str) -> str: # to unescape: html.unescape
	"""transform Unicode character  -> DEC numerical entity"""
	return txt.encode('ascii', 'xmlcharrefreplace').decode()

# API conversion multiple scripts
escapeHTML(req.get( # romanization: "IAST", "IPA", "ISO"
	"https://aksharamukha-plugin.appspot.com/api/public",
	params = dict(source = "Devanagari", target = "Siddham", text = "बुद्ध")
).text)

# %%

def pali(textDeva, textLatn, esc = True):
	textLatn_ = textLatn.split(" ") # split each word
	if esc:
		textDeva_ = [escapeHTML(x) for x in textDeva.split(" ")]
	else:
		textDeva_ = textDeva.split(" ")
	if len(textDeva_) != len(textLatn_): raise ValueError
	res = "<ruby>"
	for i in range(len(textDeva_)):
		res += "<rb>" + textDeva_[i] + "</rb><rt>" + textLatn_[i] + " </rt> "
	res = res[:-7] + "</rt></ruby>" # remove last space
	return res

prompt = ""
while prompt != "stop":
	textDeva = input("text Deva: ")
	textLatn = input("text Latn: ")
	print(pali(textDeva, textLatn))
	prompt = input("continue? ")

# %%

def combo(textHan, textViet, esc = True, printed = True):
	"""combine text (1 line) into ruby annotation in HTML"""
	if esc:
		textHan_ = [escapeHTML(x) for x in list(textHan) if x != " "] # split each character + remove spaces
	else:
		textHan_ = [x for x in list(textHan) if x != " "] # split each character + remove spaces
	textHan__, i = [], 0 # combine punctuation character with a loop (see below)
	while i < len(textHan_):
		try:
			x, y = textHan_[i], textHan_[i+1]
			if (x in ["『", "［", '&#12302;', '&#65339;'] or
			    y in ["，", "：", "；", "、", "。", "！", "？", "』", "］",
			          '&#65292;', '&#65306;', '&#65307;', '&#12289;', '&#12290;', '&#65281;', '&#65311;', '&#12303;', '&#65341;']):
				textHan__.append(x + y)
				i += 2
			else:
				textHan__.append(x)
				i += 1
		except IndexError:
			textHan__.append(textHan_[i])
			i += 1

	textViet_ = textViet.split(" ") # split each word
	if len(textHan__) != len(textViet_): raise ValueError
	res = "<ruby>"
	for i in range(len(textHan__)):
		res += "<rb>" + textHan__[i] + "</rb><rt>" + textViet_[i] + " </rt>"
	res = res[:-6] + "</rt></ruby>" # remove trailing space
	if printed: print(res)
	else: return res

def verse_noTabs(textHan, textViet, tabs, esc = True, printed = True):
	"""ombine text (multiple lines) into ruby annotation in HTML"""
	text1, text2 = textHan.split("\n"), textViet.split("\n")
	res = ""
	for i in range(len(text1)):
		res += "\t"*tabs + combo(text1[i], text2[i], esc, False) + "<br />\n"
	if printed: print(res)
	else: return res

# %%

langs = ["en", "fr", "de", "it"]
span = lambda x, y: '<span lang="{}">{}</span>'.format(x, y)

def header(text, esc = True, printed = True):
	"""parse a header (2 lines)"""
	text1 = text.split("\n") # split each line
	res = '<span lang="zh-Hant">'
	textViet, textHan = text1[0].split("\t") #1st line
	res += combo(textHan, textViet, esc, False) + "</span><br />\n" + "\t"*4
	text2 = text1[1].split(" / ") #2nd line
	if len(text2) != 4: raise ValueError
	else:
		for i in range(3): res += span(langs[i], text2[i]) + "<br />\n"  + "\t"*4
		res += span(langs[3], text2[3]) # last ele: IT
		if printed: print(res)
		else: return res

def verse(text, tabs, esc = True, printed = True):
	"""parse a verse (multiple lines) into ruby annotation"""
	text1 = text.split("\n") # split each line
	res = ""
	for txt in text1:
		textViet, textHan = txt.split("\t") # normal layout
		res += "\t"*tabs + combo(textHan, textViet, esc, False) + "<br />\n"
	res = res[tabs:-7] # trailing line break
	if printed: print(res)
	else: return res

def multiverse(text, tabs, lines, esc = True, printed = True):
	"""parse a multi-lang verse"""
	text1 = text.split("\n") # split each line
	res = '<span lang="zh-Hant" class="in-dam">\n' + "\t"*(tabs +1)
	res += verse("\n".join(text1[:lines]), tabs +1, esc, False) + "\n" + "\t"*tabs + "</span><br />\n" # han viet
	res += "\t"*tabs + '<span lang="vi">\n'
	for i in range(lines, 2*lines-1): # vi text
		res += "\t"*(tabs +1) + text1[i] + "<br />\n"
	res += "\t"*(tabs +1) + text1[2*lines-1] + "\n" + "\t"*tabs + "</span><br />\n"
	if len(text1[2*lines:]) != 4: raise ValueError
	else:
		for i in range(3):
			res += "\t"*tabs + span(langs[i], text1[2*lines+i]) + "<br />\n"
		res += "\t"*tabs + span(langs[3], text1[-1])
		if printed: print(res)
		else: return res

def multiphrase(text, tabs, esc = True, printed = True):
	"""parse a verse (multiple lines) into ruby annotation"""
	text1 = text.split("\n") # split each line
	res = '<span lang="zh-Hant" class="in-dam">' + combo(text1[1], text1[0], esc, False) + "</span><br />\n"
	res += "\t"*tabs + '<span lang="vi">' + text1[2] + "</span><br />\n"
	for i in range(3,6):
		res += "\t"*tabs + span(langs[i-3], text1[i]) + "<br />\n"
	res += "\t"*tabs + span(langs[3], text1[6])
	if printed: print(res)
	else: return res

# %%

def thanChu_seg(text, tabs, esc = True, printed = True):
	"""parse a mantra segment: vi + sa + en"""
	text1 = text.split("\n")
	if len(text1) != 3: raise ValueError
	if esc:
		text1[0] = escapeHTML(text1[0])
	else:
		res = '<span lang="vi" class="in-dam">' + text1[0] + "</span><br />\n"
		res += "\t"*tabs + '<span lang="sa" class="to-vang">' + text1[1] + "</span><br />\n"
		res += "\t"*tabs + '<span lang="en">' + text1[2] + "</span>"
		if printed: print(res)
		else: return res

def thanChu(text, tabs, esc = True, printed = True):
	"""parse a mantra"""
	text1 = text.split("\n")
	len_text = len(text1)
	if len_text % 3 != 0: raise ValueError
	else:
		res = ""
		for i in range(0, len_text, 3):
			res += "\t"*(tabs-1) + '<p class="than-chu-seg">\n' + "\t"*tabs +\
			       thanChu_seg("\n".join(text1[i:i+3]), tabs, esc, False) + "\n" + "\t"*(tabs-1) + "</p>\n"
		if printed: print(res)
		else: return res

# %%

def css(text):
	yolo = 74 - len(text)
	a1, a2 = divmod(yolo, 2)
	if a2: print("/* " + "*"*a1 + text + "*"*(a1+1) + " */")
	else: print("/* " + "*"*a1 + text + "*"*a1 + " */")

def html(text):
	yolo = 71 - len(text)
	a1, a2 = divmod(yolo, 2)
	if a2: print("<!-- " + "-"*a1 + text + "-"*(a1+1) + " -->")
	else: print("<!-- " + "-"*a1 + text + "-"*a1 + " -->")

# %%

with open(r"temp.txt", mode = "w", encoding = "utf-8") as file:
	file.write("\n".join([]))

# %%

textzh = input("zh: ")
textha = input("ha: ")
textvi = input("vi: ")
texten = input("en: ")
textfr = input("fr: ")
textde = input("de: ")
textit = input("it: ")
tabs = int(input("tabs: "))

print('<p class="multi-lang">\n' +\
	"\t"*tabs + '<span lang="zh-Hant" class="to-dam">' + combo(textzh, textha, False) + "</span><br />\n" +\
	"\t"*tabs + '<span lang="vi">' + textvi + "</span><br />\n" +\
	"\t"*tabs + '<span lang="en">' + texten + "</span><br />\n" +\
	"\t"*tabs + '<span lang="fr">' + textfr + "</span><br />\n" +\
	"\t"*tabs + '<span lang="de">' + textde + "</span><br />\n" +\
	"\t"*tabs + '<span lang="it">' + textit + "</span>\n" +\
	"\t"*(tabs-1) + "</p>")

# %% batch escape/unescape HTML & unicode entities

pattern = re.compile(r"(?<=<rb>)[^<]+(?=</rb>)")
basepath = "pathtodir/DataFiles/"
for filename in os.listdir(basepath):
	print(filename)
	if filename.endswith('.html'):
		with open(basepath + filename, mode = "r", encoding = "utf-8") as file:
			tmp = file.readlines()
		with open(basepath + filename, mode = "w", encoding = "utf-8") as file:
			fn = lambda x: escapeHTML(x.group(0)) # escape
			file.writelines([pattern.sub(fn, txt) for txt in tmp])
