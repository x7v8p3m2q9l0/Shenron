#!/bin/python3

__INFO__ = {
    "Obfuscator": "Shenron",
    "Obfuscator Owner": ["Nguyễn Xuân Trịnh"],
    "VM": "S_VM",
    "Theme": "Dragon Ball",
    "Contact": "https://t.me/CalceIsMe",
    "Obfuscator Code Writing Process": "https://www.youtube.com/watch?v=8yXEvIRFCwc&list=PLS0WF70AJy04pZ-OQwlsjuXiJL_3B9Oc4&index=4",
}

BANNER = """⠀⠀⠀⠀⢨⠊⠀⢀⢀⠀⠀⠀⠈⠺⡵⡱⠀⠀⠀⢠⠃⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡘⢰⡁⠉⠊⠙⢎⣆⠀⠀⠀⠀⢩⢀⠜⠀⠀⠀
⠀⠀⠀⢠⠃⠀⠀⢸⢸⡀⠀⠀⠀⠀⠘⢷⡡⠀⠀⠎⠀⢰⣧⠀⠀⠈⡆⠀⠀⠀⠀⠀⠀⠀⠈⣐⢤⣀⣀⢙⠦⠀⠀⠀⠀⡇⠀⠀⠀⠀
⠀⠀⢀⠃⠀⠀⠀⡌⢸⠃⠀⠀⠀⢀⠀⠀⠑⢧⡸⠀⢀⣿⢻⡀⠀⠀⣻⠀⠀⠀⠀⠀⣠⡴⠛⠉⠀⠀⠀⠑⢝⣦⠀⠀⠀⢰⠠⠁⠀⠀
⠀⠀⠌⠀⠀⠀⡘⣖⣄⢃⠀⠀⠀⠈⢦⡀⠀⡜⡇⠀⣼⠃⠈⢷⣶⢿⠟⠀⠀⠀⢠⠞⠁⠀⣀⠄⠂⣶⣶⣦⠆⠋⠓⠀⢀⣀⡇⠀⠀⠀⠀⠀⠀
⠡⡀⡇⠀⢰⣧⢱⠊⠘⡈⠄⠀⠀⡀⠘⣿⢦⣡⢡⢰⡇⢀⠤⠊⡡⠃⠀⠀⢀⡴⠁⢀⠔⠊⠀⠀⢠⣿⠟⠁⠀⢀⠀⢀⠾⣤⣀⠀⠀⡠
⡀⠱⡇⠀⡆⢃⠀⠀⠀⠃⠀⠀⠀⣧⣀⣹⡄⠙⡾⡏⠀⡌⣠⡾⠁⠀⠀⣠⠊⢠⠔⠁⠀⠀⠀⠀⣸⡏⠀⠀⠀⢨⣪⡄⢻⣥⠫⡳⢊⣴
⠀⠀⢡⢠⠀⢸⡆⠀⣀⠀⠀⠀⠀⠈⣛⢛⣁⣀⠘⣧⣀⢱⡿⠀⠀⢀⡔⢁⢔⠕⠉⠐⣄⣠⠤⠶⠛⠁⢀⣀⠀⠀⠉⠁⠈⠷⣞⠔⡕⣿
⢄⡀⠘⢸⠀⣘⠇⠀⠀⠀⠀⠀⠀⠀⠀⠉⠐⠤⡑⢎⡉⢨⠁⠀⣠⢏⠔⠁⠘⣤⠴⢊⣡⣤⠴⠖⠒⠻⠧⣐⠓⠀⠀⠀⠀⠈⠀⡜⠀⠇
⠤⡈⠑⠇⠡⣻⢠⠊⠉⠉⠉⠑⠒⠤⣀⠀⠀⠀⠈⣾⣄⢘⣫⣜⠮⢿⣆⡴⢊⢥⡪⠛⠉⠀⠀⠀⠀⢀⠄⠂⠁⠀⠀⠀⠀⠀⠀⢧⡀⠈
⠁⠈⠑⠼⣀⣁⣇⠀⣴⡉⠉⠉⠀⠒⡢⠌⣐⡂⠶⣘⢾⡾⠿⢅⠀⣠⣶⡿⠓⠁⢠⠖⣦⡄⠀⠀⠀⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢎⢳
⠀⠀⠀⠀⠉⣇⣿⢜⠙⢷⡄⠀⠀⠀⣄⣠⠼⢶⡛⣡⢴⠀⢀⠛⠱⡀⠀⠀⠀⠀⢀⠎⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡋⠮⡈
⠀⠀⢀⣖⠂⢽⡈⠀⠈⠑⠻⡦⠖⢋⣁⡴⠴⠊⣉⡠⢻⡖⠪⢄⡀⢈⠆⠀⠀⢠⠊⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠤⡵⢤⣃
⠀⠀⠸⢠⡯⣖⢵⡀⠀⠀⣠⣤⠮⠋⠁⠀⠀⠀⠀⠀⠸⣌⢆⢱⡾⠃⢀⠠⠔⠁⣀⢸⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⡸⠚⡸⠈⠁
⠤⢀⣀⢇⢡⠸⡗⢔⡄⠸⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⡩⠔⢉⡠⠔⠂⠉⢀⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢁⠎⢀⡠⠔
⠀⠀⠀⠘⡌⢦⡃⣎⠘⡄⠀⠀⠀⠀⠀⠀⠀⠀⠠⡟⠠⡐⣋⠤⠀⣀⠤⠐⠂⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⢉⠉⠁⠀⠀
⠤⠀⠀⠀⠰⡀⠈⠻⡤⠚⢄⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠈⠂⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⢸⠀⢀⠤⠊
⣀⠀⠀⠀⠀⠘⠢⡑⢽⡬⢽⢆⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⡶⠟⣉⣉⢢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠇⠀⠈⡖⠓⠒⠂
⠀⢈⣑⣒⡤⠄⠀⠈⠑⠥⣈⠙⠧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣁⠔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀⣠⡻⠀⠀⠀⠇⠐⡔⣡
⠉⠉⠁⠀⠒⠒⠒⠒⠀⠤⠤⠍⣒⡗⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⠀⠀⢠⡞⢡⠃⠀⠀⠀⢸⠀⠸⣡
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠈⣶⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠁⣠⡔⠉⠀⡎⠀⠀⠀⠀⢸⠀⠀⠃
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠇⣀⢼⠀⠀⠀⢉⡄⠈⠐⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⡜⡡⣾⠃⠀⠀⠸⠀⠀⠀⠀⠀⠀⡧⢄⡈
⠀⠀⠀⠀⠀⠀⠀⣀⠤⠚⠉⠀⡆⠀⠀⠀⠈⡵⢄⡀⠀⠀⠙⠂⠄⣀⡀⠤⠊⠉⢀⣀⣠⡴⢿⣟⠞⠀⠀⢀⠇⠀⠀⠀⠀⠀⠀⡗⠢⢌
⠀⠀⠀⠀⡠⠔⠉⠀⠀⢀⡠⡤⠇⠀⠀⢀⠀⠰⣣⠈⠐⠤⡀⠀⡀⠈⠙⢍⠉⣉⠤⠒⠉⣠⣟⢮⠂⡄⠀⣼⠁⠀⡆⠀⠀⠀⠀⢡⣀⠀
⣿⡷⠖⠉⠀⠀⡠⠔⣪⣿⠟⣫⠀⠀⠀⢸⠀⠀⢩⢆⠀⠀⠈⠑⢳⠤⠄⠠⠭⠤⠐⠂⢉⣾⢮⠃⢠⠃⢰⡹⠀⢰⠀⠀⠀⠀⠀⢸⡉⣳
⠉⠀⢀⡠⠒⠉⣠⠾⠋⢁⠔⠹⠀⠀⠀⡈⡇⠀⠀⢫⣆⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⣘⢾⠃⢀⠏⣠⡳⠁⠀⣾⠀⠀⠀⠀⠀⠀⠈⠉"""

import ast, marshal, base64, bz2, zlib, lzma, time, sys
from ast import *
from utils.minifier import minify_source
from utils.constant_renamer import var_con_cak
from vm.vm import main, remove_comments

sys.setrecursionlimit(99999999)

ver = str(sys.version_info.major) + "." + str(sys.version_info.minor)

try:
    from pystyle import *
except ModuleNotFoundError:
    print(">> Installing Module")
    __import__("os").system(f"pip{ver} install pystyle")
    from pystyle import *

System.Clear()

listofshit = {
    "A": "🐉",
    "B": "🐲",
    "C": "⭐",
    "D": "✦",
    "E": "✧",
    "F": "✨",
    "G": "💫",
    "H": "🌠",
    "I": "⚡",
    "J": "🔥",
    "K": "💥",
    "L": "☄",
    "M": "️",
    "N": "🌪",
    "O": "❄",
    "P": "️",
    "Q": "🌀",
    "R": "🥋",
    "S": "🥊",
    "T": "⚔",
    "U": "️",
    "V": "👊",
    "W": "🙌",
    "X": "👐",
    "Y": "🟠",
    "Z": "🔴",
    "a": "🟡",
    "b": "🟢",
    "c": "🔵",
    "d": "🟣",
    "e": "⚫",
    "f": "⚪",
    "g": "👽",
    "h": "🤖",
    "i": "👺",
    "j": "🐢",
    "k": "🐒",
    "l": "🦍",
    "m": "👑",
    "n": "💎",
    "o": "🔮",
    "p": "🍑",
    "q": "🍗",
    "r": "🍚",
    "s": "🍶",
    "t": "🏯",
    "u": "⛩",
    "v": "⛰",
    "w": "🛡",
    "x": "👑",
    "y": "🧙",
    "z": "\u200d",
    "0": "♂",
    "1": "️",
    "2": "🤜",
    "3": "🤛",
    "4": "😡",
    "5": "😤",
    "6": "🥵",
    "7": "🤯",
    "8": "🌌",
    "9": "🌍",
    "+": "🌑",
    "/": "☀",
}
d = {v: k for k, v in listofshit.items()}


def enc(s: str) -> str:
    noisy = s.encode().hex()
    mapped = "".join(listofshit.get(c, c) for c in noisy)
    return f'shenron("{mapped}")'


buitlins = [
    "__import__",
    "abs",
    "all",
    "any",
    "ascii",
    "bin",
    "breakpoint",
    "callable",
    "chr",
    "compile",
    "delattr",
    "dir",
    "divmod",
    "eval",
    "exec",
    "format",
    "getattr",
    "globals",
    "hasattr",
    "hash",
    "hex",
    "id",
    "input",
    "isinstance",
    "issubclass",
    "iter",
    "aiter",
    "len",
    "locals",
    "max",
    "min",
    "next",
    "anext",
    "oct",
    "ord",
    "pow",
    "print",
    "repr",
    "round",
    "setattr",
    "sorted",
    "sum",
    "vars",
    "None",
    "Ellipsis",
    "NotImplemented",
    "False",
    "True",
    "bool",
    "memoryview",
    "bytearray",
    "bytes",
    "classmethod",
    "complex",
    "dict",
    "enumerate",
    "filter",
    "float",
    "frozenset",
    "property",
    "int",
    "list",
    "map",
    "object",
    "range",
    "reversed",
    "set",
    "slice",
    "staticmethod",
    "str",
    "super",
    "tuple",
    "type",
    "zip",
]
anti = """
if str(capsule_add('sys').exit) != '<built-in function exit>':
    logging.debug(str(capsule_add('sys').exit))
    capsule_add('sys').exit()

if str(exec) != '<built-in function exec>':
    logging.debug(str(exec))
    capsule_add('sys').exit()

if str(eval) != '<built-in function eval>':
    logging.debug(str(eval))
    capsule_add('sys').exit()

if str(__import__) != '<built-in function __import__>':
    logging.debug(str(__import__))
    capsule_add('sys').exit()

if str(capsule_add('marshal').loads) != '<built-in function loads>':
    logging.debug(str(capsule_add('marshal').loads))
    capsule_add('sys').exit()
"""

"""
thecodething=open(__file__, 'rb').read()
if thecodething.count(b'print')>3:
    print(">> Don't Edit This File")
    capsule_add('sys').exit()

"""
v = var_con_cak()
args = var_con_cak()
kwds = var_con_cak()
d = var_con_cak()
k = var_con_cak()
c = var_con_cak()
arg_ = var_con_cak()
s = var_con_cak()

SANH = f"""
#!/bin/python{ver}
# -*- coding: utf-8 -*-

INFOTAGGE=123

class CapsuleCorp(object):

    def __init__(self):
        if str(__import__("sys").version_info.major)+"."+str(__import__("sys").version_info.minor) != "{ver}":
            print(f'>> Your Python Version Is {{str(__import__("sys").version_info.major)+"."+str(__import__("sys").version_info.minor)}}.\\n>> Please Install Python {ver} To Run This File!')
            __import__('sys').exit()

    def __call__(self, *{args}, **{kwds}):
        global yamcha, bulma, capsule, radar, shenron, frieza, goku, vegeta, gohan, trunks, capsule, kamehameha, capsule_add
        globals()['frieza'] = eval('lave'[::-1])
        globals()['goku'] = frieza('rts'[::-1])
        globals()['vegeta'] = frieza('setyb'[::-1])
        globals()['gohan'] = frieza(('tcid')[::-1])
        globals()['bulma'] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        globals()['capsule'] = "🐉🐲⭐✦✧✨💫🌠⚡🔥💥☄️🌪❄️🌀🥋🥊⚔️👊🙌👐🟠🔴🟡🟢🔵🟣⚫⚪👽🤖👺🐢🐒🦍👑💎🔮🍑🍗🍚🍶🏯⛩⛰🛡👑🧙‍♂️🤜🤛😡😤🥵🤯🌌🌍🌑☀️🌠"
        globals()['trunks'] = frieza('piz'[::-1])
        globals()['radar'] = gohan(trunks(bulma, capsule))
        {d} = {{{v}: {k} for {k}, {v} in radar.items()}}
        globals()['shenron'] = lambda {s}: getattr(vegeta, "fromhex")(goku().join(({d}.get({c}, {c}) for {c} in {s}))).decode()
        globals()['capsule_add'] = frieza({enc('__tropmi__')}[::-1])
        globals()['kamehameha'] = frieza({enc('cexe')}[::-1])
        globals()['yamcha'] = frieza({enc('tni')}[::-1])
        
CapsuleCorp()()

class DragonRadar(object):

    def __init__(self, *{args}):
        setattr(self, "dragonball1", {enc('base64')})
        setattr(self, "dragonball2", {enc('bz2')})
        setattr(self, "dragonball3", {enc('zlib')})
        setattr(self, "dragonball4", {enc('lzma')})
        setattr(self, "{arg_}", {args}[0])

    def scan(self):
        return getattr(capsule_add(getattr(self, "dragonball4")), {enc("decompress")})(
            getattr(capsule_add(getattr(self, "dragonball3")), {enc("decompress")})(
                getattr(capsule_add(getattr(self, "dragonball2")), {enc("decompress")})(
                    getattr(capsule_add(getattr(self, "dragonball1")), {enc("a85decode")})(getattr(self, "{arg_}"))
                )
            )
        )


class ShenronSummoner(object):

    def __init__(self):
        setattr(self, "dragonball5", {enc('marshal')})
        setattr(self, "dragonball6", radar)
        setattr(self, "dragonball7", kamehameha)

    def wish(self, {arg_}):
        getattr(self, "dragonball7")(
            getattr(capsule_add(getattr(self, "dragonball5")), {enc("loads")})({arg_}),
            globals()
        )

    def __call__(self, *{args}, **{kwds}):
        Shenron = DragonRadar({args}[0]).scan()
        self.wish(Shenron)

try:
    ShenronSummoner()(BYTECODE)
except Exception as e:
    print(e)
except KeyboardInterrupt:
    exit('Exiting...')"""


def _args(name):
    return ast.arguments(
        posonlyargs=[],
        args=[ast.arg(arg=name)],
        vararg=None,
        kwonlyargs=[],
        kw_defaults=[],
        kwarg=None,
        defaults=[],
    )


def obfstr(s):
    lst = [ord(i) for i in s]
    v = var_con_cak()
    lam3 = ast.Lambda(
        args=_args(var_con_cak()),
        body=ast.Call(
            func=ast.Attribute(
                value=ast.Call(ast.Name("goku", ast.Load()), [], []),
                attr="join",
                ctx=ast.Load(),
            ),
            args=[
                ast.GeneratorExp(
                    elt=ast.Call(
                        ast.Name("chr", ast.Load()), [ast.Name(v, ast.Load())], []
                    ),
                    generators=[
                        ast.comprehension(
                            target=ast.Name(v, ast.Store()),
                            iter=ast.List([ast.Constant(x) for x in lst], ast.Load()),
                            ifs=[],
                            is_async=0,
                        )
                    ],
                )
            ],
            keywords=[],
        ),
    )
    lam2 = ast.Lambda(
        _args(var_con_cak()), ast.Call(lam3, [ast.Constant("Trinh Dep Trai")], [])
    )
    lam1 = ast.Lambda(
        _args(var_con_cak()), ast.Call(lam2, [ast.Constant("Trinh Dep Trai")], [])
    )
    return ast.Call(lam1, [ast.Constant("Trinh Dep Trai")], [])


def obfint(i):
    haha = 2010 - i
    lam3 = ast.Lambda(
        _args(var_con_cak()),
        ast.Call(
            ast.Name("yamcha", ast.Load()),
            [ast.BinOp(ast.Constant(2010), ast.Sub(), ast.Constant(haha))],
            [],
        ),
    )
    lam2 = ast.Lambda(
        _args(var_con_cak()), ast.Call(lam3, [ast.Constant("Trinh Dep Trai")], [])
    )
    lam1 = ast.Lambda(
        _args(var_con_cak()), ast.Call(lam2, [ast.Constant("Trinh Dep Trai")], [])
    )
    return ast.Call(lam1, [ast.Constant("Trinh Dep Trai")], [])


def joinstr(f):
    if not isinstance(f, ast.JoinedStr):
        return f
    vl = []
    for i in f.values:
        if isinstance(i, ast.Constant):
            vl.append(i)
        elif isinstance(i, ast.FormattedValue):
            value_expr = i.value
            if i.conversion == 115:
                value_expr = Call(
                    func=Name(id="goku", ctx=Load()), args=[value_expr], keywords=[]
                )
            elif i.conversion == 114:
                value_expr = Call(
                    func=Name(id="repr", ctx=Load()), args=[value_expr], keywords=[]
                )
            elif i.conversion == 97:
                value_expr = Call(
                    func=Name(id="ascii", ctx=Load()), args=[value_expr], keywords=[]
                )
            if i.format_spec:
                if isinstance(i.format_spec, ast.JoinedStr):
                    spec_expr = joinstr(i.format_spec)
                elif isinstance(i.format_spec, ast.Constant):
                    spec_expr = i.format_spec
                elif isinstance(i.format_spec, ast.FormattedValue):
                    spec_parts = []
                    spec_value = i.format_spec.value
                    if i.format_spec.conversion == 115:
                        spec_value = Call(
                            func=Name(id="goku", ctx=Load()),
                            args=[spec_value],
                            keywords=[],
                        )
                    elif i.format_spec.conversion == 114:
                        spec_value = Call(
                            func=Name(id="repr", ctx=Load()),
                            args=[spec_value],
                            keywords=[],
                        )
                    elif i.format_spec.conversion == 97:
                        spec_value = Call(
                            func=Name(id="ascii", ctx=Load()),
                            args=[spec_value],
                            keywords=[],
                        )
                    spec_expr = spec_value
                else:
                    spec_expr = i.format_spec
                value_expr = Call(
                    func=Name(id="format", ctx=Load()),
                    args=[value_expr, spec_expr],
                    keywords=[],
                )
            elif i.conversion == -1:
                value_expr = Call(
                    func=Name(id="goku", ctx=Load()), args=[value_expr], keywords=[]
                )
            vl.append(value_expr)
        elif hasattr(i, "values") and isinstance(i, ast.JoinedStr):
            vl.append(joinstr(i))
        else:
            vl.append(Call(func=Name(id="goku", ctx=Load()), args=[i], keywords=[]))
    if not vl:
        return Constant(value="")
    if len(vl) == 1 and isinstance(vl[0], ast.Constant):
        return vl[0]
    return Call(
        func=Attribute(value=Constant(value=""), attr="join", ctx=Load()),
        args=[Tuple(elts=vl, ctx=Load())],
        keywords=[],
    )


class cv(ast.NodeTransformer):

    def visit_JoinedStr(self, node):
        node = joinstr(node)
        return node


class hb(ast.NodeTransformer):
    def visit_Name(self, node: ast.Name):
        if node.id in set(dir(__builtins__)):
            return ast.Call(
                func=ast.Name(id="getattr", ctx=ast.Load()),
                args=[
                    ast.Call(
                        func=ast.Name(id="__import__", ctx=ast.Load()),
                        args=[ast.Constant(value="builtins")],
                        keywords=[],
                    ),
                    ast.Constant(value=node.id),
                ],
                keywords=[],
            )
        return node


class obf(ast.NodeTransformer):

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            node = obfstr(node.value)
        elif isinstance(node.value, int):
            node = obfint(node.value)
        return node


def gen_jcode(code):
    men = var_con_cak()
    trinhdeptrai = var_con_cak()
    quadeptrai = var_con_cak()
    return [
        Assign(
            targets=[Name(id=trinhdeptrai, ctx=Store())],
            value=Constant(value=men),
            lineno=0,
        ),
        Assign(
            targets=[Name(id=quadeptrai, ctx=Store())],
            value=Constant(value=True),
            lineno=0,
        ),
        If(
            test=BoolOp(
                op=And(),
                values=[
                    Compare(
                        left=Name(id=trinhdeptrai, ctx=Load()),
                        ops=[Eq()],
                        comparators=[Constant(value=men)],
                    ),
                    Compare(
                        left=Name(id=quadeptrai, ctx=Load()),
                        ops=[NotEq()],
                        comparators=[Constant(value=True)],
                    ),
                ],
            ),
            body=[
                Expr(
                    value=Lambda(
                        args=arguments(
                            posonlyargs=[],
                            args=[],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[],
                        ),
                        body=Constant(value="dit me may"),
                    )
                )
            ],
            orelse=[
                If(
                    test=BoolOp(
                        op=And(),
                        values=[
                            Compare(
                                left=Name(id=trinhdeptrai, ctx=Load()),
                                ops=[Eq()],
                                comparators=[Constant(value=men)],
                            ),
                            Compare(
                                left=Name(id=quadeptrai, ctx=Load()),
                                ops=[NotEq()],
                                comparators=[Constant(value=False)],
                            ),
                        ],
                    ),
                    body=[
                        Try(
                            body=[
                                Expr(
                                    value=Tuple(
                                        elts=[
                                            BinOp(
                                                left=Constant(value=1),
                                                op=Div(),
                                                right=Constant(value=0),
                                            ),
                                            BinOp(
                                                left=Constant(value=123),
                                                op=Div(),
                                                right=Constant(value=0),
                                            ),
                                            BinOp(
                                                left=Constant(value=12312321312),
                                                op=Div(),
                                                right=Constant(value=0),
                                            ),
                                        ],
                                        ctx=Load(),
                                    )
                                )
                            ],
                            handlers=[ExceptHandler(body=[code])],
                            orelse=[],
                            finalbody=[],
                        )
                    ],
                    orelse=[
                        If(
                            test=BoolOp(
                                op=Or(),
                                values=[
                                    Compare(
                                        left=Name(id=trinhdeptrai, ctx=Load()),
                                        ops=[Eq()],
                                        comparators=[Constant(value="gay")],
                                    ),
                                    Compare(
                                        left=Name(id=quadeptrai, ctx=Load()),
                                        ops=[Eq()],
                                        comparators=[Constant(value=False)],
                                    ),
                                ],
                            ),
                            body=[
                                Expr(
                                    value=Call(
                                        func=Lambda(
                                            args=arguments(
                                                posonlyargs=[],
                                                args=[],
                                                kwonlyargs=[],
                                                kw_defaults=[],
                                                defaults=[],
                                            ),
                                            body=Call(
                                                func=Name(id="print", ctx=Load()),
                                                args=[
                                                    Constant(
                                                        value="cai lon cha nha may"
                                                    )
                                                ],
                                                keywords=[],
                                            ),
                                        ),
                                        args=[],
                                        keywords=[],
                                    )
                                )
                            ],
                            orelse=[
                                While(
                                    test=Constant(value=True), body=[Pass()], orelse=[]
                                ),
                                Expr(
                                    value=Call(
                                        func=Name(id="print", ctx=Load()),
                                        args=[Constant(value="cai dit thang cha may")],
                                        keywords=[],
                                    )
                                ),
                            ],
                        )
                    ],
                )
            ],
        ),
    ]


class junk(ast.NodeTransformer):

    def visit_Module(self, node):
        new_body = []
        for stmt in node.body:
            if isinstance(stmt, (ast.FunctionDef, ast.ClassDef)):
                stmt = self.visit(stmt)
            new_body.extend(gen_jcode(stmt))
        node.body = new_body
        return node

    def visit_FunctionDef(self, node):
        new_body = []
        for stmt in node.body:
            new_body.extend(gen_jcode(stmt))
        node.body = new_body
        return node

    def visit_ClassDef(self, node):
        new_body = []
        for stmt in node.body:
            new_body.extend(gen_jcode(stmt))
        node.body = new_body
        return node


print(Colorate.Diagonal(Colors.DynamicMIX((Col.orange, Col.red)), BANNER))
print(
    Colorate.Diagonal(
        Colors.DynamicMIX((Col.red, Col.orange)), " " * 19 + "Obfuscator: Shenron"
    )
)
print(
    Colorate.Diagonal(
        Colors.DynamicMIX((Col.red, Col.orange)), " " * 19 + "Author: NguyenXuanTrinh"
    )
)
print(
    Colorate.Diagonal(
        Colors.DynamicMIX((Col.orange, Col.red)), " " * 19 + "Telegram: @CalceIsMe"
    )
)
print(
    Colorate.Diagonal(
        Colors.DynamicMIX((Col.red, Col.orange)),
        " " * 19 + "Github: @nguyenxuantrinhdznotpd",
    )
)
print()
cyyy = Colors.StaticMIX((Col.light_blue, Col.light_gray, Col.light_red))

while True:
    file_name = input(
        Colorate.Diagonal(
            Colors.DynamicMIX((Col.red, cyyy)), ">> Enter Your File Name: "
        )
    )
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            # z=anti + f.read()
            code = ast.parse(remove_comments(f.read()))
        break
    except FileNotFoundError:
        print(Colorate.Horizontal(Colors.red_to_white, "File Not Found.\n"))
# HI. It will generate it in around 40 secs
vm_debug = (
    True
    if input(
        Colorate.Diagonal(
            Colors.DynamicMIX((Col.red, cyyy)),
            ">> Do You Want To Enable VM Debug Mode (Y/n): ",
        )
    )
    != "n"
    else False
)
hide_builtins = (
    True
    if input(
        Colorate.Diagonal(
            Colors.DynamicMIX((Col.red, cyyy)),
            ">> Do You Want To Hide Builtins (Y/n): ",
        )
    )
    != "n"
    else False
)
use_vm = (
    True
    if input(
        Colorate.Diagonal(
            Colors.DynamicMIX((Col.red, cyyy)), ">> Do You Want To Use VM (Y/n): "
        )
    )
    != "n"
    else False
)
junk_code = (
    True
    if input(
        Colorate.Diagonal(
            Colors.DynamicMIX((Col.red, cyyy)),
            ">> Do You Want To Add Junk Code (Recommend Yes) (Y/n): ",
        )
    )
    != "n"
    else False
)

print(Colorate.Diagonal(Colors.DynamicMIX((Col.red, cyyy)), "[...] Starting..."))
st = time.perf_counter()
if use_vm:
    print(Colorate.Diagonal(Colors.DynamicMIX((Col.red, cyyy)), "[...] Adding VM..."))
    # from utils.constant_renamer import renamethings
    code = minify_source(code)
    import types

    func = types.FunctionType(compile(code, "<SVM>", "exec"), {})
    code = remove_comments(
        main(func, random_opcodes=not vm_debug, random_opcodes_count=12, debug=vm_debug)
    )
    if vm_debug:
        with open("vm_code.py", "w", encoding="utf-8") as f:
            f.write(code)
    code = ast.parse(code)
    # TODO: Fix this shit or fully remove it.
    # code=renamethings(code)
print(
    Colorate.Diagonal(
        Colors.DynamicMIX((Col.red, cyyy)),
        "[...] Converting F-String To Join String...",
    )
)
cv().visit(code)

if hide_builtins:
    print(
        Colorate.Diagonal(
            Colors.DynamicMIX((Col.red, cyyy)), "[...] Hiding Builtins..."
        )
    )
    hb().visit(code)
    if vm_debug:
        with open("hide_builtins.py", "w", encoding="utf-8") as f:
            f.write(ast.unparse(code))
print(
    Colorate.Diagonal(
        Colors.DynamicMIX((Col.red, cyyy)), "[...] Obfuscating Content..."
    )
)
obf().visit(code)

if junk_code:
    print(
        Colorate.Diagonal(
            Colors.DynamicMIX((Col.red, cyyy)), "[...] Adding Junk Code..."
        )
    )
    junk().visit(code)
    code = ast.unparse(code)
    if vm_debug:
        with open("junk_code.py", "w", encoding="utf-8") as f:
            f.write(code)
else:
    code = ast.unparse(code)
print(Colorate.Diagonal(Colors.DynamicMIX((Col.red, cyyy)), "[...] Compiling..."))
code = (
    code
    + """
if __INFO__ != {
    'Obfuscator': 'Shenron',
    'Obfuscator Owner': ['Nguyễn Xuân Trịnh'],
    'VM': 'S_VM',
    'Theme': 'Dragon Ball',
    'Contact': 'https://t.me/CalceIsMe',
    'Obfuscator Code Writing Process': 'https://www.youtube.com/watch?v=8yXEvIRFCwc&list=PLS0WF70AJy04pZ-OQwlsjuXiJL_3B9Oc4&index=4'
}:
    print(">> Don't Edit __INFO__")
    open('diffinfo.txt','r')
    capsule_add('sys').exit()"""
)
code = marshal.dumps(compile(code, "<Shenron>", "exec"))

print(Colorate.Diagonal(Colors.DynamicMIX((Col.red, cyyy)), "[...] Compressing..."))
code = base64.a85encode(bz2.compress(zlib.compress(lzma.compress(code))))
# code = minify_source(code.decode(),skip_format=True)

open("obf-" + file_name, "wb").write(
    minify_source(SANH.replace("BYTECODE", str(code)))
    .replace(
        "INFOTAGGE = 123",
        """
__INFO__ = {
    'Obfuscator': 'Shenron',
    'Obfuscator Owner': ['Nguyễn Xuân Trịnh'],
    'VM': 'S_VM',
    'Theme': 'Dragon Ball',
    'Contact': 'https://t.me/CalceIsMe',
    'Obfuscator Code Writing Process': 'https://www.youtube.com/watch?v=8yXEvIRFCwc&list=PLS0WF70AJy04pZ-OQwlsjuXiJL_3B9Oc4&index=4'
}""",
    )
    .encode()
)
print(
    Colorate.Diagonal(
        Colors.DynamicMIX((Col.red, cyyy)), f'>> Saved in {"obf-"+file_name}'
    )
)
timse = time.perf_counter() - st
print(
    Colorate.Diagonal(
        Colors.DynamicMIX((Col.red, cyyy)), f">> Done in {round(timse,3)}s"
    )
)
