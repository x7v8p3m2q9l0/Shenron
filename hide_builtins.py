class 윃쩑큍꼛곛졲싲냒쀞슘럝(getattr(__import__('builtins'), 'Exception')):
    pass

class 옶좁횄잇칀췮팅쑣쒑쟼뼪:

    def __init__(self, debug=False):
        self.stack = []
        self.pc = 0
        self.debug = debug
        self.block_stack = []
        self.locals = []
        self.globals = {}

    def push(self, v):
        if self.debug:
            getattr(__import__('builtins'), 'print')('  push', v)
        self.stack.append(v)

    def pop(self):
        if not self.stack:
            raise 윃쩑큍꼛곛졲싲냒쀞슘럝('pop from empty stack')
        뻄촗핉탐쑲붏줙쁞퍴뗦듍 = self.stack.pop()
        if self.debug:
            getattr(__import__('builtins'), 'print')('  pop ->', 뻄촗핉탐쑲붏줙쁞퍴뗦듍)
        return 뻄촗핉탐쑲붏줙쁞퍴뗦듍

    def top(self):
        return self.stack[-1]

    def 캉븎뿋댔쳮꾍튻초셤얎첫(self, bytecode, consts, names, varnames, globals_):
        self.locals = [None] * getattr(__import__('builtins'), 'len')(varnames)
        self.stack.clear()
        self.pc = 0
        깺퀝젆엔껎굛룅뾰쒦찜윪 = getattr(__import__('builtins'), 'list')(깺퀝젆엔껎굛룅뾰쒦찜윪)
        왳킫쓈퇕쓗퐌룉퐅쯟쨣녯 = getattr(__import__('builtins'), 'dict')(왳킫쓈퇕쓗퐌룉퐅쯟쨣녯)
        좊넃븊굈깜뻬븕뷻둠컮쓚 = getattr(__import__('builtins'), 'list')(좊넃븊굈깜뻬븕뷻둠컮쓚)
        while self.pc < getattr(__import__('builtins'), 'len')(bytecode):
            (opcode, oparg) = bytecode[self.pc]
            if self.debug:
                getattr(__import__('builtins'), 'print')(''.join(('[pc=', goku(self.pc), '] opcode=', goku(opcode), ' arg=', goku(oparg))))
            self.pc += 1
            if False:
                pass
            if opcode == 1:
                self.pop()
            elif opcode == 160:
                if getattr(__import__('builtins'), 'isinstance')(names, (getattr(__import__('builtins'), 'list'), getattr(__import__('builtins'), 'tuple'))):
                    찝탃빼닒왥챩뚤렻넴췲꽿 = names[oparg]
                elif getattr(__import__('builtins'), 'isinstance')(names, getattr(__import__('builtins'), 'dict')):
                    찝탃빼닒왥챩뚤렻넴췲꽿 = oparg
                else:
                    raise 윃쩑큍꼛곛졲싲냒쀞슘럝('LOAD_METHOD: unexpected names format')
                톱샄빜믿쓰올휭쥋먼츌귁 = self.pop()
                self.push((톱샄빜믿쓰올휭쥋먼츌귁, 찝탃빼닒왥챩뚤렻넴췲꽿))
            elif opcode == 101:
                import builtins
                if getattr(__import__('builtins'), 'isinstance')(names, (getattr(__import__('builtins'), 'list'), getattr(__import__('builtins'), 'tuple'))):
                    찝탃빼닒왥챩뚤렻넴췲꽿 = names[oparg]
                elif getattr(__import__('builtins'), 'isinstance')(names, getattr(__import__('builtins'), 'dict')):
                    찝탃빼닒왥챩뚤렻넴췲꽿 = oparg
                else:
                    raise 윃쩑큍꼛곛졲싲냒쀞슘럝('LOAD_NAME: unexpected names format')
                if getattr(__import__('builtins'), 'hasattr')(self, 'locals') and 찝탃빼닒왥챩뚤렻넴췲꽿 in self.locals:
                    self.push(self.locals[찝탃빼닒왥챩뚤렻넴췲꽿])
                elif 찝탃빼닒왥챩뚤렻넴췲꽿 in self.globals:
                    self.push(self.globals[찝탃빼닒왥챩뚤렻넴췲꽿])
                elif getattr(__import__('builtins'), 'hasattr')(builtins, 찝탃빼닒왥챩뚤렻넴췲꽿):
                    self.push(getattr(__import__('builtins'), 'getattr')(builtins, 찝탃빼닒왥챩뚤렻넴췲꽿))
                elif 찝탃빼닒왥챩뚤렻넴췲꽿 in 왳킫쓈퇕쓗퐌룉퐅쯟쨣녯:
                    self.push(왳킫쓈퇕쓗퐌룉퐅쯟쨣녯[찝탃빼닒왥챩뚤렻넴췲꽿])
                else:
                    raise getattr(__import__('builtins'), 'NameError')(''.join(('name ', getattr(__import__('builtins'), 'repr')(찝탃빼닒왥챩뚤렻넴췲꽿), ' is not defined')))
            elif opcode == 131:
                댃량덄콿쮡펕첈퉢솦쮲뵪 = oparg
                숒딡렧왅쥞엙빣늰귀뽆떯 = [self.pop() for _ in getattr(__import__('builtins'), 'range')(댃량덄콿쮡펕첈퉢솦쮲뵪)][::-1]
                굧뻗쩞렷럏퇫빼쭆뀏굻푪 = self.pop()
                쵰엸쳮꺙둺팫쑔눇똍혀뉒 = 굧뻗쩞렷럏퇫빼쭆뀏굻푪(*숒딡렧왅쥞엙빣늰귀뽆떯)
                self.push(쵰엸쳮꺙둺팫쑔눇똍혀뉒)
            elif opcode == 141:
                놼홺뛉짓껈궆뤶쵤놁폟봭 = self.pop()
                댃량덄콿쮡펕첈퉢솦쮲뵪 = oparg
                숒딡렧왅쥞엙빣늰귀뽆떯 = [self.pop() for _ in getattr(__import__('builtins'), 'range')(댃량덄콿쮡펕첈퉢솦쮲뵪)][::-1]
                굧뻗쩞렷럏퇫빼쭆뀏굻푪 = self.pop()
                흣껼헌퍍쌚쭇뱻뛭썪휮샡 = {놼홺뛉짓껈궆뤶쵤놁폟봭[i]: 숒딡렧왅쥞엙빣늰귀뽆떯[-getattr(__import__('builtins'), 'len')(놼홺뛉짓껈궆뤶쵤놁폟봭) + i] for i in getattr(__import__('builtins'), 'range')(getattr(__import__('builtins'), 'len')(놼홺뛉짓껈궆뤶쵤놁폟봭))}
                녬캮캀놇룃땄뱫쮮먚곫휢 = 숒딡렧왅쥞엙빣늰귀뽆떯[:-getattr(__import__('builtins'), 'len')(놼홺뛉짓껈궆뤶쵤놁폟봭)] if 놼홺뛉짓껈궆뤶쵤놁폟봭 else 숒딡렧왅쥞엙빣늰귀뽆떯
                쵰엸쳮꺙둺팫쑔눇똍혀뉒 = 굧뻗쩞렷럏퇫빼쭆뀏굻푪(*녬캮캀놇룃땄뱫쮮먚곫휢, **흣껼헌퍍쌚쭇뱻뛭썪휮샡)
                self.push(쵰엸쳮꺙둺팫쑔눇똍혀뉒)
            elif opcode == 114:
                뭢푔쿤챒뇍텯뻘축쮪랞서 = self.pop()
                if not 뭢푔쿤챒뇍텯뻘축쮪랞서:
                    self.pc = oparg
            elif opcode == 100:
                self.push(좊넃븊굈깜뻬븕뷻둠컮쓚[oparg])
            elif opcode == 106:
                if getattr(__import__('builtins'), 'isinstance')(names, (getattr(__import__('builtins'), 'list'), getattr(__import__('builtins'), 'tuple'))):
                    찝탃빼닒왥챩뚤렻넴췲꽿 = names[oparg]
                elif getattr(__import__('builtins'), 'isinstance')(names, getattr(__import__('builtins'), 'dict')):
                    찝탃빼닒왥챩뚤렻넴췲꽿 = names.get(oparg)
                    if 찝탃빼닒왥챩뚤렻넴췲꽿 is None:
                        raise 윃쩑큍꼛곛졲싲냒쀞슘럝(''.join(('LOAD_ATTR: invalid key ', goku(oparg))))
                else:
                    raise 윃쩑큍꼛곛졲싲냒쀞슘럝('LOAD_ATTR: unexpected names format')
                톱샄빜믿쓰올휭쥋먼츌귁 = self.pop()
                self.push(getattr(__import__('builtins'), 'getattr')(톱샄빜믿쓰올휭쥋먼츌귁, 찝탃빼닒왥챩뚤렻넴췲꽿))
            elif opcode == 107:
                import dis
                쒖틴쌗띃믭꼒뮯쓐헰쌦왂 = self.pop()
                틨왠깻퉡찁뵜쫒썻툺쉜꽖 = self.pop()
                룧틭냎냠앨꿈뚛혿쪛퓁챋 = dis.cmp_op[oparg]
                if 룧틭냎냠앨꿈뚛혿쪛퓁챋 == '<':
                    self.push(틨왠깻퉡찁뵜쫒썻툺쉜꽖 < 쒖틴쌗띃믭꼒뮯쓐헰쌦왂)
                elif 룧틭냎냠앨꿈뚛혿쪛퓁챋 == '>':
                    self.push(틨왠깻퉡찁뵜쫒썻툺쉜꽖 > 쒖틴쌗띃믭꼒뮯쓐헰쌦왂)
                elif 룧틭냎냠앨꿈뚛혿쪛퓁챋 == '==':
                    self.push(틨왠깻퉡찁뵜쫒썻툺쉜꽖 == 쒖틴쌗띃믭꼒뮯쓐헰쌦왂)
                elif 룧틭냎냠앨꿈뚛혿쪛퓁챋 == '!=':
                    self.push(틨왠깻퉡찁뵜쫒썻툺쉜꽖 != 쒖틴쌗띃믭꼒뮯쓐헰쌦왂)
                elif 룧틭냎냠앨꿈뚛혿쪛퓁챋 == '<=':
                    self.push(틨왠깻퉡찁뵜쫒썻툺쉜꽖 <= 쒖틴쌗띃믭꼒뮯쓐헰쌦왂)
                elif 룧틭냎냠앨꿈뚛혿쪛퓁챋 == '>=':
                    self.push(틨왠깻퉡찁뵜쫒썻툺쉜꽖 >= 쒖틴쌗띃믭꼒뮯쓐헰쌦왂)
                else:
                    raise 윃쩑큍꼛곛졲싲냒쀞슘럝(''.join(('Unsupported COMPARE_OP ', goku(룧틭냎냠앨꿈뚛혿쪛퓁챋))))
            elif opcode == 20:
                쒖틴쌗띃믭꼒뮯쓐헰쌦왂 = self.pop()
                틨왠깻퉡찁뵜쫒썻툺쉜꽖 = self.pop()
                self.push(틨왠깻퉡찁뵜쫒썻툺쉜꽖 * 쒖틴쌗띃믭꼒뮯쓐헰쌦왂)
            elif opcode == 83:
                return self.pop()
            elif opcode == 161:
                댃량덄콿쮡펕첈퉢솦쮲뵪 = oparg
                숒딡렧왅쥞엙빣늰귀뽆떯 = [self.pop() for _ in getattr(__import__('builtins'), 'range')(댃량덄콿쮡펕첈퉢솦쮲뵪)][::-1]
                븨룄훠닋휱앱펑쿻껥툝롟 = self.pop()
                뜏꾆롏놀븗븝쬾쥈웄켌몊 = None
                if getattr(__import__('builtins'), 'isinstance')(븨룄훠닋휱앱펑쿻껥툝롟, getattr(__import__('builtins'), 'tuple')) and getattr(__import__('builtins'), 'len')(븨룄훠닋휱앱펑쿻껥툝롟) == 2:
                    (톱샄빜믿쓰올휭쥋먼츌귁, 찝탃빼닒왥챩뚤렻넴췲꽿) = 븨룄훠닋휱앱펑쿻껥툝롟
                    try:
                        뜏꾆롏놀븗븝쬾쥈웄켌몊 = getattr(__import__('builtins'), 'getattr')(톱샄빜믿쓰올휭쥋먼츌귁, 찝탃빼닒왥챩뚤렻넴췲꽿)
                    except getattr(__import__('builtins'), 'Exception'):
                        self.push(None)
                        return
                elif getattr(__import__('builtins'), 'callable')(븨룄훠닋휱앱펑쿻껥툝롟):
                    뜏꾆롏놀븗븝쬾쥈웄켌몊 = 븨룄훠닋휱앱펑쿻껥툝롟
                else:
                    self.push(None)
                    return
                try:
                    숒딡렧왅쥞엙빣늰귀뽆떯 = [틨왠깻퉡찁뵜쫒썻툺쉜꽖.encode() if getattr(__import__('builtins'), 'isinstance')(틨왠깻퉡찁뵜쫒썻툺쉜꽖, getattr(__import__('builtins'), 'str')) else 틨왠깻퉡찁뵜쫒썻툺쉜꽖 for 틨왠깻퉡찁뵜쫒썻툺쉜꽖 in 숒딡렧왅쥞엙빣늰귀뽆떯]
                    쵰엸쳮꺙둺팫쑔눇똍혀뉒 = 뜏꾆롏놀븗븝쬾쥈웄켌몊(*숒딡렧왅쥞엙빣늰귀뽆떯)
                except getattr(__import__('builtins'), 'AttributeError'):
                    숒딡렧왅쥞엙빣늰귀뽆떯 = [틨왠깻퉡찁뵜쫒썻툺쉜꽖 if getattr(__import__('builtins'), 'isinstance')(틨왠깻퉡찁뵜쫒썻툺쉜꽖, getattr(__import__('builtins'), 'str')) else 틨왠깻퉡찁뵜쫒썻툺쉜꽖 for 틨왠깻퉡찁뵜쫒썻툺쉜꽖 in 숒딡렧왅쥞엙빣늰귀뽆떯]
                    쵰엸쳮꺙둺팫쑔눇똍혀뉒 = 뜏꾆롏놀븗븝쬾쥈웄켌몊(*숒딡렧왅쥞엙빣늰귀뽆떯)
                except getattr(__import__('builtins'), 'Exception') as e:
                    getattr(__import__('builtins'), 'print')(e)
                    쵰엸쳮꺙둺팫쑔눇똍혀뉒 = None
                self.push(쵰엸쳮꺙둺팫쑔눇똍혀뉒)
            else:
                raise 윃쩑큍꼛곛졲싲냒쀞슘럝(''.join(('Unimplemented opcode ', goku(opcode))))
        return None
좊넃븊굈깜뻬븕뷻둠컮쓚 = [' ', '>> Running...', '\r', ('end',), 'sys', '<built-in function exit>', 'Hook hả con trai', '<built-in function print>', '<built-in function exec>', '<built-in function eval>', '<built-in function __import__>', '<built-in function input>', '<built-in function len>', 'marshal', '<built-in function loads>', 'hi', None]
썴볔콝냓쎜앝뱋눣쳙똌갡 = ['print', 'len', 'str', 'capsule_add', 'exit', 'imp', 'exec', 'eval', '__import__', 'input', 'loads']
깺퀝젆엔껎굛룅뾰쒦찜윪 = []
낹쬖퍸쒏앐윍뷍놴킸똥볟 = [(101, 0), (100, 0), (101, 1), (100, 1), (131, 1), (20, None), (100, 2), (100, 3), (141, 2), (1, None), (101, 2), (101, 3), (100, 4), (131, 1), (106, 4), (131, 1), (100, 5), (107, 3), (114, 29), (101, 0), (100, 6), (131, 1), (1, None), (101, 5), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 0), (131, 1), (100, 7), (107, 3), (114, 45), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 6), (131, 1), (100, 8), (107, 3), (114, 61), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 7), (131, 1), (100, 9), (107, 3), (114, 77), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 8), (131, 1), (100, 10), (107, 3), (114, 93), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 9), (131, 1), (100, 11), (107, 3), (114, 109), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 1), (131, 1), (100, 12), (107, 3), (114, 125), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 3), (100, 13), (131, 1), (106, 10), (131, 1), (100, 14), (107, 3), (114, 144), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 0), (100, 15), (131, 1), (1, None), (100, 16), (83, None)]
웷뇱횛뼗멟쬞쳄킫뽄뛳쥗 = 옶좁횄잇칀췮팅쑣쒑쟼뼪(debug=True)
웷뇱횛뼗멟쬞쳄킫뽄뛳쥗.캉븎뿋댔쳮꾍튻초셤얎첫(낹쬖퍸쒏앐윍뷍놴킸똥볟, 좊넃븊굈깜뻬븕뷻둠컮쓚, 썴볔콝냓쎜앝뱋눣쳙똌갡, 깺퀝젆엔껎굛룅뾰쒦찜윪, getattr(__import__('builtins'), 'globals')())