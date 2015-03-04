import copy

class Language(object):
    
    class Rule(object):
        def __init__(self, string=None):
            if string is not None:
                self.__init_from_string(string)

        def __init_from_string(self, string):
            parts = string.split(' ')
            self._from = parts[0]
            self._to = []
            for i in parts[1:]:
                self._to.append(i)


        def is_lamda_rule(self):
            return len(self._to) == 0

        
        def get_splitted_copy(self, terminals_to_replace):
            new_rule = copy.deepcopy(self)
            for i in range(0, len(new_rule._to)):
                if new_rule._to[i] in terminals_to_replace:
                    new_rule._to[i] = new_rule._to[i] + '\''
            return new_rule


        def _get_right_part_str(self):
            if self.is_lamda_rule():
                return chr(955)
            else:
                return ' '.join(self._to)
        
        
        def __str__(self):
            return '%s -> %s' % (self._from, self._get_right_part_str())

        
        def __repr__(self):
            return '%s -> %s' % (self._from, self._get_right_part_str())


    def __init_from_file(self, filename):
        with open(filename, 'r') as f:
            nonterminals_num = int(f.readline())
            self._nonterminals = []
            for _ in range(0, nonterminals_num):
                self._nonterminals.append(f.readline().strip(' \n\t'))
            
            terminals_num = int(f.readline().strip(' \n\t'))
            self._terminals = []
            for _ in range(0, terminals_num):
                self._terminals.append(f.readline().strip(' \n\t'))

            rules_num = int(f.readline())
            self._rules = []
            for _ in range(0, rules_num):
                rule = Language.Rule(string=f.readline().strip(' \n\t'))
                self._rules.append(rule)
            
            self._start_symbol = f.readline().strip(' \n\t')
    
    def __init_from_data(self, terminals, non_terminals, rules, start):
        self._nonterminals = non_terminals[:]
        self._terminals = terminals[:]
        self._start_symbol = start
        self._rules = copy.deepcopy(rules)

    
    def __init__(self, filename=None, terminals=None, non_terminals=None, rules=None, start=None):
        if filename is not None:
            self.__init_from_file(filename)
        elif terminals is not None:
            self.__init_from_data(terminals, non_terminals, rules, start)

    def split_grammer(self, nonterminals_to_replace):
        new_grammers = []
        new_rules = []
        for rule in self._rules:
            new_rules.append(rule.get_splitted_copy(nonterminals_to_replace))

        for nonterminal_to_replace in nonterminals_to_replace:
            new_nonterminals = list(set(self._nonterminals) - (set(nonterminals_to_replace).union(set([nonterminal_to_replace]))))
            new_terminals = list(set(self._terminals).union(set([i + '\'' for i in nonterminals_to_replace])))
            new_grammers.append(Language(terminals=new_terminals, non_terminals=new_nonterminals, rules=new_rules, start=nonterminal_to_replace))
        
        return new_grammers

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "Terminals: %s\nNon-terminals: %s\nRules: %s\nStart symbol: %s" % (self._terminals, self._nonterminals, self._rules, self._start_symbol)

    
language = Language(filename='grammer728.txt')
print('Original grammer:')
print(language)
print('')
print('')
print('Grammers after split without reduction')
new_grammers = language.split_grammer(('E', 'T'))
for new_grammer in new_grammers:
    print(new_grammer)
    print('')
#print(language.split_grammer(('E', 'T')))
