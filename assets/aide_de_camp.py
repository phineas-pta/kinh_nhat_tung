# -*- coding: utf-8 -*-

import re, os, html, requests as req
from unicodedata import normalize as uni_norm

def escapeHTML(txt):
	"""transform Unicode character -> DEC numerical entity"""
	return txt.encode("ascii", "xmlcharrefreplace").decode()

html.unescape("&#21335;") # to unescape
escapeHTML(uni_norm("NFC","đức")) # composed form
escapeHTML(uni_norm("NFD","đức")) # decomposed form

# %%

def pali(textDeva, textLatn, esc = True):
	textLatn_, textDeva_ = textLatn.split(" "), textDeva.split(" ") # split each word
	if esc: textDeva_ = list(map(escapeHTML, textDeva_))
	if len(textDeva_) != len(textLatn_): raise ValueError
	res = "<ruby>"
	for i in range(len(textDeva_)):
		res += f"<rb>{textDeva_[i]}</rb><rt>{textLatn_[i]}</rt>"
	return res + "</ruby>"

# API conversion multiple scripts
baseurl = "https://aksharamukha-plugin.appspot.com/api/public"
reqdict = dict(source = "IAST", target = "Siddham") # "IAST", "IPA", "ISO", "Devanagari"
def toSiddham(textIAST, ruby = True, esc = True):
	"""convert romanized text to Siddham script"""
	# some typo when copied from Digital Sanskrit Buddhist
	textIASTbis = textIAST.replace("|", ".").replace(" .", ".").replace(" ?", "?")
	reqdict["text"] = textIASTbis
	textSidd = req.get(baseurl, params = reqdict).text
	if ruby: # replace after to have special Siddham punctuation
		res = pali(textSidd, textIASTbis.replace("..", "."), esc)
	else:
		if esc: res = escapeHTML(textSidd)
		else: res = textSidd
	return res

while True: print(toSiddham(input("text IAST: ")), "\n")

def stanzas(textIAST, tabs, esc = True, printed = True):
	"""stanzas of Siddham"""
	textSidd = toSiddham(textIAST, ruby = False)
	textIAST_, textSidd_ = textIAST.split("\n"), textSidd.split("\n")
	res = ""
	for i in range(len(textIAST_)):
		res += "\t"*tabs + pali(textSidd_[i], textIAST_[i], esc) + "<br />\n"
	res = res[:-7]
	if printed: print(res)
	else: return res

# %%

Han_punc = list("，、：；．。！？…～／‧•●『』「」（）《》〈〉［］【】〖〗〔〕｛｝")
punc_search = re.compile("(" + "|".join(Han_punc) + ")")

def combo(textHan, textViet, esc = True, printed = True, debug = False):
	test0 = textHan.replace(" ", "") # remove spaces
	test1 = punc_search.sub("", test0) # without punc
	test2, test3 = list(test0), list(test1) # split each character: with & without punc
	if debug: print("ckpt1:", test2, test3)

	textViet_ = textViet.split(" ") # split each word
	if debug: print("ckpt2:", textViet_)
	if len(test3) != len(textViet_): raise ValueError("Han-Viet divergence")

	res, i, j = "<ruby>", 0, 0 # combine punctuation character with a loop (see below)
	while (n := i+j) < len(test2):
		x = test2[n] # to be processed
		if debug: print("ckpt3:", x)
		y = escapeHTML(x) if esc else x
		if x in Han_punc:
			res += f"<rb>{y}</rb><rt></rt>"
			j += 1
		else:
			if debug: print("ckpt4:", test3[i])
			if x != test3[i]: raise ValueError("punctuation error")
			if debug: print("ckpt5:", textViet_[i])
			res += f"<rb>{y}</rb><rt>{textViet_[i]}</rt>"
			i += 1

	res += "</ruby>"
	if printed: print(res)
	else: return res

while True: print(combo(input("text Hant: "), input("text Viet: ")), "\n")

def verse_HanViet(textHan, textViet, tabs, esc = True, printed = True):
	"""combine text (multiple lines) into ruby annotation in HTML"""
	text1, text2 = textHan.split("\n"), textViet.split("\n")
	res = ""
	for i in range(len(text1)):
		res += "\t"*tabs + combo(text1[i], text2[i], esc, False, False) + "<br />\n"
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

ruby_base = re.compile(r"(?<=<rb>)[^<]+(?=</rb>)")
"".join(map(
	html.unescape,
	ruby_base.findall("<ruby><rb>&#21335;</rb><rt>Nam </rt><rb>&#28961;</rb><rt>mô</rt></ruby>")
))

basepath = "pathtodir/DataFiles/"
esc_fn = lambda x: escapeHTML(x.group(0))
ruby_sub = lambda txt: ruby_base.sub(esc_fn, txt)
for filename in os.listdir(basepath):
	print(filename)
	if filename.endswith(".html"):
		with open(basepath + filename, mode = "r", encoding = "utf-8") as file:
			tmp = file.readlines()
		with open(basepath + filename, mode = "w", encoding = "utf-8") as file:
			file.writelines(map(ruby_sub, tmp)) # doesn't need list object
