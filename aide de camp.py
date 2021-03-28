# -*- coding: utf-8 -*-

import re, os, html, requests as req

def escapeHTML(txt): # to unescape: html.unescape
	"""transform Unicode character  -> DEC numerical entity"""
	return txt.encode('ascii', 'xmlcharrefreplace').decode()

# API conversion multiple scripts
baseurl = "https://aksharamukha-plugin.appspot.com/api/public"
reqdict = dict(source = "Devanagari", target = "Siddham") # romanization: "IAST", "IPA", "ISO"
reqdict["text"] = "बुद्ध"
escapeHTML(req.get(baseurl, params = reqdict).text)

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

reqdict = dict(source = "IAST", target = "Siddham")
def toSiddham(textIAST, ruby = True, esc = True):
	"""convert romanized text to Siddham script"""
	reqdict["text"] = textIAST
	textSidd = req.get(baseurl, params = reqdict).text
	if ruby: return pali(textSidd, textIAST, esc)
	else: return textSidd

def stanzas(textIAST, tabs, esc = True, printed = True):
	"""stanzas of Siddham"""
	textSidd = toSiddham(textIAST, ruby = False)
	_textIAST, _textSidd = textIAST.split("\n"), textSidd.split("\n")
	res = ""
	for i in range(len(_textIAST)):
		res += "\t"*tabs + pali(_textSidd[i], _textIAST[i], esc) + "<br />\n"
	res = res[:-7]
	if printed: print(res)
	else: return res

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

def verse_HanViet(textHan, textViet, tabs, esc = True, printed = True):
	"""combine text (multiple lines) into ruby annotation in HTML"""
	text1, text2 = textHan.split("\n"), textViet.split("\n")
	res = ""
	for i in range(len(text1)):
		res += "\t"*tabs + combo(text1[i], text2[i], esc, False) + "<br />\n"
	res = res[:-7]
	if printed: print(res)
	else: return res

prompt = ""
while prompt != "stop":
	textIAST = input("text IAST: ")
	textHan = input("text Han: ")
	textViet = input("text Viet: ")
	print()
	print(toSiddham(textIAST))
	print()
	print(combo(textHan, textViet, printed = False))
	print()
	prompt = input("continue? ")

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
