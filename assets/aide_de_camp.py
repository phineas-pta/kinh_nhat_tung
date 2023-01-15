# -*- coding: utf-8 -*-

import re, os, html, json, requests as req
from unicodedata import normalize as uni_norm

def escapeHTML(txt: str) -> str:
	"""transform Unicode character -> DEC numerical entity"""
	return txt.encode("ascii", "xmlcharrefreplace").decode()

html.unescape("&#21335;") # to unescape
escapeHTML(uni_norm("NFC","đức")) # composed form
escapeHTML(uni_norm("NFD","đức")) # decomposed form

# %%

def pali(textDeva: str, textLatn: str, esc: bool=True) -> str:
	textLatn_, textDeva_ = textLatn.split(" "), textDeva.split(" ") # split each word
	if esc: textDeva_ = list(map(escapeHTML, textDeva_))
	if len(textDeva_) != len(textLatn_): raise ValueError
	res = ""
	for i in range(len(textDeva_)):
		res += f"<ruby><rb>{textDeva_[i]}</rb><rt>{textLatn_[i]}</rt></ruby>\n"
	return res

headers = {"User-Agent": "kinh_nhat_tung/6.3.2 (https://github.com/phineas-pta/kinh_nhat_tung) Python/3.11"}

# API conversion multiple scripts
aksha_url = "https://aksharamukha-plugin.appspot.com/api/public"
aksha_reqdict = {"source": "IAST", "target": "Siddham"} # "IAST", "IPA", "ISO", "Devanagari"
def toSiddham(textIAST: str, ruby: bool=True, esc: bool=True) -> str:
	"""convert romanized text to Siddham script"""
	# some typo when copied from Digital Sanskrit Buddhist
	textIASTbis = textIAST.replace("|", ".").replace(" .", ".").replace(" ?", "?")
	aksha_reqdict["text"] = textIASTbis
	textSidd = req.get(aksha_url, headers=headers, params=aksha_reqdict).text
	if ruby: # replace after to have special Siddham punctuation
		res = pali(textSidd, textIASTbis.replace("..", "."), esc)
	else:
		if esc: res = escapeHTML(textSidd)
		else: res = textSidd
	return res

while True: print(toSiddham(input("text IAST: ")), "\n")

def stanzas(textIAST: str, esc: bool=True, printed: bool=True):
	"""stanzas of Siddham"""
	textSidd = toSiddham(textIAST, ruby=False)
	textIAST_, textSidd_ = textIAST.split("\n"), textSidd.split("\n")
	res = ""
	for i in range(len(textIAST_)):
		res += pali(textSidd_[i], textIAST_[i], esc) + "<br />\n"
	res = res[:-7]
	if printed: print(res)
	else: return res

# %%

thivien_url = "https://hvdic.thivien.net/transcript-query.json.php"
thivien_headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", **headers}

# i also shared this code at https://gist.github.com/phineas-pta/457b9f546ec20d5d2019d5799847eb01
def convertHanViet(textHan: str, printed: bool=True) -> str:
	payload = f"mode=trans&lang=1&input={textHan}"
	response = requests.request("POST", thivien_url, headers=thivien_headers, data=payload.encode())
	result = json.loads(response.text)["result"]
	res = " ".join([el["o"][0] for el in result])
	if printed: print(res)
	else: return res

Han_punc = list("，、：；．。！？…⋯～／‧•●『』「」（）《》〈〉［］【】〖〗〔〕｛｝")
punc_search = re.compile("(" + "|".join(Han_punc) + ")")

def combo(textHan: str, textViet: str, esc: bool=True, printed: bool=True, debug: bool=False) -> str:
	test0 = textHan.replace(" ", "") # remove spaces
	test1 = punc_search.sub("", test0) # without punc
	test2, test3 = list(test0), list(test1) # split each character: with & without punc
	if debug: print("ckpt1:", test2, test3)

	textViet_ = textViet.split(" ") # split each word
	if debug: print("ckpt2:", textViet_)
	if len(test3) != len(textViet_): raise ValueError("Han-Viet divergence")

	res, i, j = "", 0, 0 # combine punctuation character with a loop (see below)
	while (n := i+j) < len(test2):
		x = test2[n] # to be processed
		if debug: print("ckpt3:", x)
		y = escapeHTML(x) if esc else x
		if x in Han_punc:
			res += f"<ruby><rb>{y}</rb>"
			res += f"<!-- {x} -->" if esc else ""
			res += "<rt></rt></ruby>\n"
			j += 1
		else:
			if debug: print("ckpt4:", test3[i])
			if x != test3[i]: raise ValueError("punctuation error")
			if debug: print("ckpt5:", textViet_[i])
			res += f"<ruby><rb>{y}</rb>"
			res += f"<!-- {x} -->" if esc else ""
			res += f"<rt>{textViet_[i]}</rt></ruby>\n"
			i += 1

	if printed: print(res)
	else: return res

while True: print(combo(input("text Hant: "), input("text Viet: ")), "\n")

def verse_HanViet(textHan: str, textViet: str, esc: bool=True, printed: bool=True) -> str:
	"""combine text (multiple lines) into ruby annotation in HTML"""
	text1, text2 = textHan.split("\n"), textViet.split("\n")
	res = ""
	for i in range(len(text1)):
		res += combo(text1[i], text2[i], esc, False, False) + "<br />\n"
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
	print(combo(textHan, textViet, printed=False))
	print()

# %% batch escape/unescape HTML & unicode entities

test_txt = "<ruby><rb>&#21335;</rb><rt>Nam</rt></ruby><ruby><rb>&#28961;</rb><rt>mô</rt></ruby>"

ruby_base = re.compile(r"(?<=<rb>)[^<]+(?=</rb>)")
" ".join(map( # example
	html.unescape,
	ruby_base.findall(test_txt)
))

esc_fn = lambda x: escapeHTML(x.group(0))
ruby_sub = lambda txt: ruby_base.sub(esc_fn, txt)

han_ruby = re.compile(r"<rb>&#[^7]\d+;</rb>")
def unesc_han_fn(matchobj: re.Match) -> str:
	x = matchobj.group(0)[4:-5] # because len("<rb>") = 4 and len("</rb>") = 5
	y = html.unescape(x)
	return f"<rb>{x}</rb><!-- {y} -->"
han_ruby.sub(unesc_han_fn, test_txt) # example
unesc_han_sub = lambda txt: han_ruby.sub(unesc_han_fn, txt)

basepath = "pathtodir/DataFiles/"
for filename in os.listdir(basepath):
	print(filename)
	if filename.endswith(".html"):
		my_file = basepath + "/" + filename
		with open(my_file, mode="r", encoding="utf-8") as file:
			tmp = file.readlines()
		with open(my_file, mode="w", encoding="utf-8") as file:
			file.writelines(map(unesc_han_sub, tmp)) # doesn't need list object
