# -*- coding: utf-8 -*-

import re, os, html, requests as req
from unicodedata import normalize as uni_norm

def escapeHTML(txt):
	"""transform Unicode character  -> DEC numerical entity"""
	return txt.encode('ascii', 'xmlcharrefreplace').decode()

html.unescape('&#21335;') # to unescape
escapeHTML(uni_norm('NFC','đức')) # composed form
escapeHTML(uni_norm('NFD','đức')) # decomposed form

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

# API conversion multiple scripts
baseurl = "https://aksharamukha-plugin.appspot.com/api/public"
reqdict = dict(source = "IAST", target = "Siddham") # romanization: "IAST", "IPA", "ISO" # "Devanagari"
def toSiddham(textIAST, ruby = True, esc = True):
	"""convert romanized text to Siddham script"""
	# some typo when copied from Digital Sanskrit Buddhist
	textIASTbis = textIAST.replace("|", ".").replace(" .", ".").replace(" ?", "?")
	reqdict["text"] = textIASTbis
	textSidd = req.get(baseurl, params = reqdict).text
	if ruby: return pali(textSidd, textIASTbis.replace("..", "."), esc) # replace after to have special Siddham punctuation
	else:
		if esc: return escapeHTML(textSidd)
		else: return textSidd

while True:
	print(toSiddham(input("text IAST: ")))
	print()

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

Han_punc_left = ["『", "「", "［", "《", '&#12302;', '&#12300;', '&#65339;', '&#12298;']
Han_punc_right = ["，", "：", "；", "、", "。", "！", "？", "』", "」", "］", "》",
'&#65292;', '&#65306;', '&#65307;', '&#12289;', '&#12290;', '&#65281;', '&#65311;', '&#12303;', '&#12301;', '&#65341;', '&#12299;']

def combo(textHan, textViet, esc = True, printed = True):
	"""combine text (1 line) into ruby annotation in HTML"""
	if esc:
		textHan_ = [escapeHTML(x) for x in list(textHan) if x != " "] # split each character + remove spaces
	else:
		textHan_ = [x for x in list(textHan) if x != " "] # split each character + remove spaces
	textHan__, i = [], 0 # combine punctuation character with a loop (see below)
	while i < len(textHan_):
		x = textHan_[i]
		try:
			y = textHan_[i+1]
			if x in Han_punc_left or y in Han_punc_right:
				textHan__.append(x + y)
				i += 2
			else:
				textHan__.append(x)
				i += 1
		except IndexError: # last elem
			if x in Han_punc_right: textHan__[-1] += x
			else: textHan__.append(x)
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

while True:
	textIAST = input("text IAST: ")
	textHan = input("text Han: ")
	textViet = input("text Viet: ")
	print()
	print(toSiddham(textIAST))
	print()
	print(combo(textHan, textViet, printed = False))
	print()

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
