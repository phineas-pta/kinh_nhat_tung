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

Han_punc = ["『", "「", "（", "［", "【", "《", "〈", "，", "：", "；", "、", "。", "！", "？", "』", "」", "）", "］", "】", "》", "〉", "‧"]
punc_search = re.compile("(" + "|".join(Han_punc) + ")")

def combo(textHan, textViet, esc = True, printed = True):
	test0 = textHan.replace(" ", "") # remove spaces
	test1 = punc_search.sub("", test0) # without punc

	test2, test3 = list(test0), list(test1)
	test4 = list(map(escapeHTML, test2)) if esc else test2 # split each character
	test5 = list(map(escapeHTML, test3)) if esc else test3 # without punc

	textViet_ = textViet.split(" ") # split each word
	if len(test5) != len(textViet_): raise ValueError("Han-Viet divergence")

	res, i, j = "<ruby>", 0, 0 # combine punctuation character with a loop (see below)
	while (n := i+j) < len(test4):
		x = test4[n]
		if x in Han_punc:
			res += "<rb>" + x + "</rb><rt></rt>"
			j += 1
		else:
			if x != test5[i]: raise ValueError("punctuation error")
			res += "<rb>" + x + "</rb><rt>" + textViet_[i] + " </rt>"
			i += 1

	if res[:-6] == " </rt>": res = res[:-6] + "</rt></ruby>" # remove trailing space
	else: res += "</ruby>"
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
