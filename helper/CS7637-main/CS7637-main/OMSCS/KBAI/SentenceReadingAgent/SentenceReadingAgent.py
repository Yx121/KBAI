# import spacy
import string
import time


class SentenceReadingAgent:
    def __init__(self):
        # If you want to do any initial processing, add it here.
        pass

    def solve(self, sentence, question):
        # Add your code here! Your solve method should receive
        # two strings as input: sentence and question. It should
        # return a string representing the answer to the question.
        
        o = Ontology()
        d = o.load()
        initial_sentence = sentence.split()
        for c in string.punctuation:
            sentence = sentence.replace(c, "")

        for c in string.punctuation:
            question = question.replace(c, "")

        words_sentence = sentence.split()
        words_sentence = [x.lower() for x in words_sentence]
        words_question = question.split()
        words_question = [x.lower() for x in words_question]

        words_s = {}
        words_q = {}

        for i in words_sentence:
            if d.get(i) in words_s:
                words_s[d.get(i)].append(i)
            else:
                words_s[d.get(i)] = [i]

        for i in words_question:
            if d.get(i) in words_q:
                words_q[d.get(i)].append(i)
            else:
                words_q[d.get(i)] = [i]

        # Heuristics that is based on the knowledge from the test examples.
        # Safe
        if "time" in words_question:
            for i in initial_sentence:
                if ":" in i:
                    return i

        # Safe
        if "when" in words_question:

            when = ["day", "night", "morning", "yesterday", "today"]
            for i in words_sentence:
                if i in when:
                    return i

            sentence_adv = words_s.get('ADV')
            if sentence_adv is not None:
                return sentence_adv[0]
        # Safe
        if "who" in words_question:
            # When there are no PROPN in the question, get the first PROPN.

            propn_list_s = words_s.get('PROPN')
            propn_list_q = words_q.get('PROPN')
            noun_list_s = words_s.get('PRON')
            noun_list_q = words_q.get('PRON')

            if propn_list_q is None and propn_list_s is not None:
                return propn_list_s[0].capitalize()
            elif propn_list_q is not None and len(propn_list_q) == 1:
                if propn_list_q[0] in propn_list_s:
                    propn_list_s.remove(propn_list_q[0])
                    return propn_list_s[0].capitalize()
            elif propn_list_s is not None:
                return propn_list_s[0].capitalize()
            else:
                return noun_list_s[0]

        if "what" in words_question:

            s_list_noun = words_s.get('NOUN')
            s_list_verb = words_s.get('VERB')
            s_list_adj = words_s.get('ADJ')
            s_list_det = words_s.get('DET')
            q_list_noun = words_q.get('NOUN')
            q_list_verb = words_q.get('VERB')
            s_list_pnoun = words_s.get('PNOUN')
            q_list_pnoun = words_s.get('PNOUN')

            if 'name' in words_question:
                for i in initial_sentence[1:]:
                    if i[0].isupper():
                        return i

            if 'do' in words_question:
                return s_list_verb[0]

            if 'color' in words_question:
                color = words_s.get('ADJ')
                subject = words_q.get('NOUN')
                if len(color) == 1:
                    return color[0]

                if subject is not None:
                    subject2 = subject[1]
                    index = initial_sentence.index(subject2)
                    index2 = index - 1
                    return initial_sentence[index2]
                return color[0]

            if q_list_noun is not None:
                if s_list_noun is not None:
                    # remove all the similar words in both lists.
                    res = set(q_list_noun).intersection(set(s_list_noun))
                    res2 = list(res ^ set(s_list_noun))
                    return res2[0]

            if s_list_noun is not None:
                return s_list_noun[0]
            elif s_list_adj is not Noneclear:
                return s_list_adj[0]
            elif s_list_verb is not None:
                return s_list_verb[0]
            else:
                pass

        if "how" in words_question:

            describer = words_question[1]  # long, Far, Do
            x = d.get(describer)
            if "many" in words_question:
                s_list_num = words_s.get('NUM')
                if len(s_list_num) == 1:
                    return s_list_num[0]
                else:
                    x = s_list_num[0] + " " + s_list_num[1]
                    return x
            if "much" in words_question:
                propn_list_s = words_s.get('DET')
                if propn_list_s is not None:
                    return propn_list_s[0]

            if x == 'ADJ':  # Long and Far are adjectives
                s_list_adj = words_s.get('ADJ')
                s_list_adv = words_s.get('ADV')
                if s_list_adj is None:
                    s_list_noun = words_s.get('NOUN')
                    if s_list_noun is not None:
                        return s_list_noun[0]
                if s_list_adv is not None:
                    location_index = words_sentence.index(s_list_adv[0]) + 1
                    return words_sentence[location_index]
                return s_list_adj[0]
            if x == 'VERB':
                s_list_verb = words_s.get('VERB')
                if s_list_verb is not None:
                    return s_list_verb[0]

        if "where" in words_question:
            s_list_noun = words_s.get('NOUN')
            q_list_noun = words_q.get('NOUN')
            if "go" in words_sentence:
                location_index = words_sentence.index('go') + 2
                return words_sentence[location_index]

            if "in" in words_sentence:
                location_index = words_sentence.index('in') + 2
                return words_sentence[location_index]

            if q_list_noun is not None:
                s_list_noun.remove(q_list_noun[0])
                return s_list_noun[0]
            else:
                return s_list_noun[0]


class Ontology:
    def __init__(self):
        # If you want to do any initial processing, add it here.
        pass

    def load(self):
        '''
        Pre-processing class to return an ontology of the word space.

        words = ["Serena",
                 "Andrew",
                 "Bobbie",
                 "Cason",
                 "David",
                 "Farzana",
                 "Frank",
                 "Hannah",
                 "Ida",
                 "Irene",
                 "Jim",
                 "Jose",
                 "Keith",
                 "Laura",
                 "Lucy",
                 "Meredith",
                 "Nick",
                 "Ada",
                 "Yeeling",
                 "Yan",
                 "the",
                 "of",
                 "to",
                 "and",
                 "a",
                 "in",
                 "is",
                 "it",
                 "you",
                 "that",
                 "he",
                 "was",
                 "for",
                 "on",
                 "are",
                 "with",
                 "as",
                 "I",
                 "his",
                 "they",
                 "be",
                 "at",
                 "one",
                 "have",
                 "this",
                 "from",
                 "or",
                 "had",
                 "by",
                 "hot",
                 "but",
                 "some",
                 "what",
                 "there",
                 "we",
                 "can",
                 "out",
                 "other",
                 "were",
                 "all",
                 "your",
                 "when",
                 "up",
                 "use",
                 "word",
                 "how",
                 "said",
                 "an",
                 "each",
                 "she",
                 "which",
                 "do",
                 "their",
                 "time",
                 "if",
                 "will",
                 "way",
                 "about",
                 "many",
                 "then",
                 "them",
                 "would",
                 "write",
                 "like",
                 "so",
                 "these",
                 "her",
                 "long",
                 "make",
                 "thing",
                 "see",
                 "him",
                 "two",
                 "has",
                 "look",
                 "more",
                 "day",
                 "could",
                 "go",
                 "come",
                 "did",
                 "my",
                 "sound",
                 "no",
                 "most",
                 "number",
                 "who",
                 "over",
                 "know",
                 "water",
                 "than",
                 "call",
                 "first",
                 "people",
                 "may",
                 "down",
                 "side",
                 "been",
                 "now",
                 "find",
                 "any",
                 "new",
                 "work",
                 "part",
                 "take",
                 "get",
                 "place",
                 "made",
                 "live",
                 "where",
                 "after",
                 "back",
                 "little",
                 "only",
                 "round",
                 "man",
                 "year",
                 "came",
                 "show",
                 "every",
                 "good",
                 "me",
                 "give",
                 "our",
                 "under",
                 "name",
                 "very",
                 "through",
                 "just",
                 "form",
                 "much",
                 "great",
                 "think",
                 "say",
                 "help",
                 "low",
                 "line",
                 "before",
                 "turn",
                 "cause",
                 "same",
                 "mean",
                 "differ",
                 "move",
                 "right",
                 "boy",
                 "old",
                 "too",
                 "does",
                 "tell",
                 "sentence",
                 "set",
                 "three",
                 "want",
                 "air",
                 "well",
                 "also",
                 "play",
                 "small",
                 "end",
                 "put",
                 "home",
                 "read",
                 "hand",
                 "port",
                 "large",
                 "spell",
                 "add",
                 "even",
                 "land",
                 "here",
                 "must",
                 "big",
                 "high",
                 "such",
                 "follow",
                 "act",
                 "why",
                 "ask",
                 "men",
                 "change",
                 "went",
                 "light",
                 "kind",
                 "off",
                 "need",
                 "house",
                 "picture",
                 "try",
                 "us",
                 "again",
                 "animal",
                 "point",
                 "mother",
                 "world",
                 "near",
                 "build",
                 "self",
                 "earth",
                 "father",
                 "head",
                 "stand",
                 "own",
                 "page",
                 "should",
                 "country",
                 "found",
                 "answer",
                 "school",
                 "grow",
                 "study",
                 "still",
                 "learn",
                 "plant",
                 "cover",
                 "food",
                 "sun",
                 "four",
                 "thought",
                 "let",
                 "keep",
                 "eye",
                 "never",
                 "last",
                 "door",
                 "between",
                 "city",
                 "tree",
                 "cross",
                 "since",
                 "hard",
                 "start",
                 "might",
                 "story",
                 "saw",
                 "far",
                 "sea",
                 "draw",
                 "left",
                 "late",
                 "run",
                 "donít",
                 "while",
                 "press",
                 "close",
                 "night",
                 "real",
                 "life",
                 "few",
                 "stop",
                 "open",
                 "seem",
                 "together",
                 "next",
                 "white",
                 "children",
                 "begin",
                 "got",
                 "walk",
                 "example",
                 "ease",
                 "paper",
                 "often",
                 "always",
                 "music",
                 "those",
                 "both",
                 "mark",
                 "book",
                 "letter",
                 "until",
                 "mile",
                 "river",
                 "car",
                 "feet",
                 "care",
                 "second",
                 "group",
                 "carry",
                 "took",
                 "rain",
                 "eat",
                 "room",
                 "friend",
                 "began",
                 "idea",
                 "fish",
                 "mountain",
                 "north",
                 "once",
                 "base",
                 "hear",
                 "horse",
                 "cut",
                 "sure",
                 "watch",
                 "color",
                 "face",
                 "wood",
                 "main",
                 "enough",
                 "plain",
                 "girl",
                 "usual",
                 "young",
                 "ready",
                 "above",
                 "ever",
                 "red",
                 "list",
                 "though",
                 "feel",
                 "talk",
                 "bird",
                 "soon",
                 "body",
                 "dog",
                 "family",
                 "direct",
                 "pose",
                 "leave",
                 "song",
                 "measure",
                 "state",
                 "product",
                 "black",
                 "short",
                 "numeral",
                 "class",
                 "wind",
                 "question",
                 "happen",
                 "complete",
                 "ship",
                 "area",
                 "half",
                 "rock",
                 "order",
                 "fire",
                 "south",
                 "problem",
                 "piece",
                 "told",
                 "knew",
                 "pass",
                 "farm",
                 "top",
                 "whole",
                 "king",
                 "size",
                 "heard",
                 "best",
                 "hour",
                 "better",
                 "TRUE",
                 "during",
                 "hundred",
                 "am",
                 "remember",
                 "step",
                 "early",
                 "hold",
                 "west",
                 "ground",
                 "interest",
                 "reach",
                 "fast",
                 "five",
                 "sing",
                 "listen",
                 "six",
                 "table",
                 "travel",
                 "less",
                 "morning",
                 "ten",
                 "simple",
                 "several",
                 "vowel",
                 "toward",
                 "war",
                 "lay",
                 "against",
                 "pattern",
                 "slow",
                 "center",
                 "love",
                 "person",
                 "money",
                 "serve",
                 "appear",
                 "road",
                 "map",
                 "science",
                 "rule",
                 "govern",
                 "pull",
                 "cold",
                 "notice",
                 "voice",
                 "fall",
                 "power",
                 "town",
                 "fine",
                 "certain",
                 "fly",
                 "unit",
                 "lead",
                 "cry",
                 "dark",
                 "machine",
                 "note",
                 "wait",
                 "plan",
                 "figure",
                 "star",
                 "box",
                 "noun",
                 "field",
                 "rest",
                 "correct",
                 "able",
                 "pound",
                 "done",
                 "beauty",
                 "drive",
                 "stood",
                 "contain",
                 "front",
                 "teach",
                 "week",
                 "final",
                 "gave",
                 "green",
                 "oh",
                 "quick",
                 "develop",
                 "sleep",
                 "warm",
                 "free",
                 "minute",
                 "strong",
                 "special",
                 "mind",
                 "behind",
                 "clear",
                 "tail",
                 "produce",
                 "fact",
                 "street",
                 "inch",
                 "lot",
                 "nothing",
                 "course",
                 "stay",
                 "wheel",
                 "full",
                 "force",
                 "blue",
                 "object",
                 "decide",
                 "surface",
                 "deep",
                 "moon",
                 "island",
                 "foot",
                 "yet",
                 "busy",
                 "test",
                 "record",
                 "boat",
                 "common",
                 "gold",
                 "possible",
                 "plane",
                 "age",
                 "dry",
                 "wonder",
                 "laugh",
                 "thousand",
                 "ago",
                 "ran",
                 "check",
                 "game",
                 "shape",
                 "yes",
                 "cool",
                 "miss",
                 "brought",
                 "heat",
                 "snow",
                 "bed",
                 "bring",
                 "sit",
                 "perhaps",
                 "fill",
                 "east",
                 "weight",
                 "language",
                 "among"
                 ]
        words = " ".join(words)

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(words)
        word_dict = {}

        for token in doc:
            # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            # token.shape_, token.is_alpha, token.is_stop)
            word_dict[token.text] = token.pos_
        '''
        word_dict = {'Serena': 'PROPN', 'Andrew': 'PROPN', 'Bobbie': 'PROPN', 'Cason': 'PROPN', 'David': 'PROPN', 'Farzana': 'PROPN', 'Frank': 'PROPN', 'Hannah': 'PROPN', 'Ida': 'PROPN', 'Irene': 'PROPN', 'Jim': 'PROPN', 'Jose': 'PROPN', 'Keith': 'PROPN', 'Laura': 'PROPN', 'Lucy': 'PROPN', 'Meredith': 'PROPN', 'Nick': 'PROPN', 'Ada': 'PROPN', 'Yeeling': 'PROPN', 'Yan': 'PROPN', 'the': 'DET', 'of': 'ADP', 'to': 'ADP', 'and': 'CCONJ', 'a': 'DET', 'in': 'NOUN', 'is': 'AUX', 'it': 'PRON', 'you': 'PRON', 'that': 'SCONJ', 'he': 'PRON', 'was': 'AUX', 'for': 'ADP', 'on': 'ADV', 'are': 'AUX', 'with': 'ADP', 'as': 'ADP', 'I': 'PRON', 'his': 'PRON', 'they': 'PRON', 'be': 'VERB', 'at': 'ADP', 'one': 'NUM', 'have': 'VERB', 'this': 'DET', 'from': 'ADP', ' or ': 'CCONJ', 'had': 'VERB', 'by': 'ADP', 'hot': 'ADJ', 'but': 'CCONJ', 'some': 'DET', 'what': 'PRON', 'there': 'ADV', 'we': 'PRON', 'can': 'AUX', 'out': 'ADV', 'other': 'ADJ', 'were': 'AUX', 'all': 'DET', 'your': 'PRON', 'when': 'ADV', 'up': 'ADP', 'use': 'VERB', 'word': 'NOUN', 'how': 'ADV', 'said': 'VERB', 'an': 'DET', 'each': 'DET', 'she': 'PRON', 'which': 'DET', 'do': 'VERB', 'their': 'PRON', 'time': 'NOUN', 'if': 'SCONJ', 'will': 'AUX', 'way': 'VERB', 'about': 'ADV', 'many': 'ADJ', 'then': 'ADV', 'them': 'PRON', 'would': 'AUX', 'write': 'VERB', 'like': 'ADP', 'so': 'ADV', 'these': 'DET', 'her': 'PRON', 'long': 'ADJ', 'make': 'NOUN', 'thing': 'NOUN', 'see': 'VERB', 'him': 'PRON', 'two': 'NUM', 'has': 'AUX', 'look': 'VERB', 'more': 'ADJ', 'day': 'NOUN', 'could': 'AUX', 'go': 'VERB', 'come': 'VERB', 'did': 'VERB', 'my': 'PRON', 'sound': 'NOUN', 'no': 'DET', 'most': 'ADJ', 'number': 'NOUN', 'who': 'PRON', 'over': 'ADP', 'know': 'VERB', 'water': 'NOUN', 'than': 'SCONJ', 'call': 'VERB', 'first': 'ADJ', 'people': 'NOUN', 'may': 'AUX', 'down': 'ADV', 'side': 'NOUN', 'been': 'AUX', 'now': 'ADV', 'find': 'VERB', 'any': 'DET', 'new': 'ADJ', 'work': 'NOUN', 'part': 'NOUN', 'take': 'VERB', 'get': 'VERB', 'place': 'NOUN', 'made': 'VERB', 'live': 'ADJ', 'where': 'ADV', 'after': 'ADP', 'back': 'ADV', 'little': 'ADJ', 'only': 'ADJ', 'round': 'ADJ', 'man': 'NOUN', 'year': 'TIME', 'came': 'VERB', 'show': 'VERB', 'every': 'DET', 'good': 'ADJ', 'me': 'PRON', 'give': 'VERB', 'our': 'PRON', 'under': 'ADP', 'name': 'NOUN', 'very': 'ADV', 'through': 'ADP', 'just': 'ADV', 'form': 'VERB', 'much': 'ADV', 'great': 'ADJ', 'think': 'NOUN', 'say': 'VERB', 'help': 'VERB', 'low': 'ADJ', 'line': 'NOUN', 'before': 'ADP', 'turn': 'NOUN', 'cause': 'VERB', 'same': 'ADJ', 'mean': 'NOUN', 'differ': 'VERB', 'move': 'NOUN', 'right': 'ADJ', 'boy': 'INTJ', 'old': 'ADJ', 'too': 'ADV', 'does': 'AUX', 'tell': 'VERB', 'sentence': 'NOUN', 'set': 'NOUN', 'three': 'NUM', 'want': 'ADJ', 'air': 'NOUN', 'well': 'ADV', 'also': 'ADV', 'play': 'VERB', 'small': 'ADJ', 'end': 'NOUN', 'put': 'VERB', 'home': 'ADV', 'read': 'VERB', 'hand': 'NOUN', 'port': 'NOUN', 'large': 'ADJ', 'spell': 'NOUN', 'add': 'VERB', 'even': 'ADV', 'land': 'NOUN', 'here': 'ADV', 'must': 'AUX', 'big': 'ADJ', 'high': 'ADJ', 'such': 'ADJ', 'follow': 'NOUN', 'act': 'NOUN', 'why': 'ADV', 'ask': 'VERB', 'men': 'NOUN', 'change': 'VERB', 'went': 'VERB', 'light': 'ADJ', 'kind': 'NOUN', 'off': 'ADV', 'need': 'VERB', 'house': 'NOUN', 'picture': 'NOUN', 'try': 'VERB', 'us': 'PRON', 'again': 'ADV', 'animal': 'NOUN', 'point': 'NOUN', 'mother': 'NOUN', 'world': 'NOUN', 'near': 'SCONJ', 'build': 'VERB', 'self': 'NOUN', 'earth': 'NOUN', 'father': 'NOUN', 'head': 'NOUN', 'stand': 'VERB', 'own': 'ADJ', 'page': 'NOUN', 'should': 'AUX', 'country': 'NOUN', 'found': 'VERB', 'answer': 'NOUN', 'school': 'NOUN', 'grow': 'NOUN', 'study': 'NOUN', 'still': 'ADV', 'learn': 'VERB', 'plant': 'NOUN', 'cover': 'VERB', 'food': 'NOUN', 'sun': 'NOUN', 'four': 'NUM', 'thought': 'VERB', 'let': 'VERB', 'keep': 'VERB', 'eye': 'NOUN', 'never': 'ADV', 'last': 'ADJ', 'door': 'NOUN', 'between': 'ADP', 'city': 'NOUN', 'tree': 'NOUN', 'cross': 'NOUN', 'since': 'SCONJ', 'hard': 'ADJ', 'start': 'NOUN', 'might': 'AUX', 'story': 'NOUN', 'saw': 'VERB', 'far': 'ADJ', 'sea': 'NOUN', 'draw': 'NOUN', 'left': 'VERB', 'late': 'ADJ', 'run': 'NOUN', 'donít': 'NOUN', 'while': 'SCONJ', 'press': 'NOUN', 'close': 'ADJ',
                     'night': 'NOUN', 'real': 'ADJ', 'life': 'NOUN', 'few': 'ADJ', 'stop': 'VERB', 'open': 'ADJ', 'seem': 'VERB', 'together': 'ADV', 'next': 'ADP', 'white': 'ADJ', 'children': 'NOUN', 'begin': 'VERB', 'got': 'VERB', 'walk': 'VERB', 'example': 'NOUN', 'ease': 'NOUN', 'paper': 'NOUN', 'often': 'ADV', 'always': 'ADV', 'music': 'VERB', 'those': 'DET', 'both': 'DET', 'mark': 'NOUN', 'book': 'NOUN', 'letter': 'NOUN', 'until': 'ADP', 'mile': 'NOUN', 'river': 'NOUN', 'car': 'NOUN', 'feet': 'NOUN', 'care': 'VERB', 'second': 'ADJ', 'group': 'NOUN', 'carry': 'NOUN', 'took': 'VERB', 'rain': 'NOUN', 'eat': 'NOUN', 'room': 'NOUN', 'friend': 'NOUN', 'began': 'VERB', 'idea': 'NOUN', 'fish': 'NOUN', 'mountain': 'NOUN', 'north': 'NOUN', 'once': 'ADV', 'base': 'NOUN', 'hear': 'VERB', 'horse': 'NOUN', 'cut': 'VERB', 'sure': 'ADJ', 'watch': 'NOUN', 'color': 'NOUN', 'face': 'VERB', 'wood': 'NOUN', 'main': 'ADJ', 'enough': 'ADJ', 'plain': 'ADJ', 'girl': 'NOUN', 'usual': 'ADJ', 'young': 'ADJ', 'ready': 'ADJ', 'above': 'ADP', 'ever': 'ADV', 'red': 'ADJ', 'list': 'NOUN', 'though': 'ADV', 'feel': 'VERB', 'talk': 'NOUN', 'bird': 'NOUN', 'soon': 'ADV', 'body': 'NOUN', 'dog': 'NOUN', 'family': 'NOUN', 'direct': 'ADJ', 'pose': 'NOUN', 'leave': 'VERB', 'song': 'NOUN', 'measure': 'NOUN', 'state': 'NOUN', 'product': 'NOUN', 'black': 'ADJ', 'short': 'ADJ', 'numeral': 'ADJ', 'class': 'NOUN', 'wind': 'NOUN', 'question': 'NOUN', 'happen': 'VERB', 'complete': 'ADJ', 'ship': 'NOUN', 'area': 'NOUN', 'half': 'ADJ', 'rock': 'NOUN', 'order': 'NOUN', 'fire': 'NOUN', 'south': 'ADJ', 'problem': 'NOUN', 'piece': 'NOUN', 'told': 'VERB', 'knew': 'VERB', 'pass': 'VERB', 'farm': 'NOUN', 'top': 'ADJ', 'whole': 'ADJ', 'king': 'NOUN', 'size': 'NOUN', 'heard': 'VERB', 'best': 'ADJ', 'hour': 'NOUN', 'better': 'ADV', 'TRUE': 'ADV', 'during': 'ADP', 'hundred': 'NUM', 'am': 'VERB', 'remember': 'VERB', 'step': 'NOUN', 'early': 'ADV', 'hold': 'VERB', 'west': 'ADJ', 'ground': 'NOUN', 'interest': 'NOUN', 'reach': 'VERB', 'fast': 'ADV', 'five': 'NUM', 'sing': 'VERB', 'listen': 'NOUN', 'six': 'NUM', 'table': 'NOUN', 'travel': 'NOUN', 'less': 'ADJ', 'morning': 'NOUN', 'ten': 'NUM', 'simple': 'ADJ', 'several': 'ADJ', 'vowel': 'NOUN', 'toward': 'ADP', 'war': 'NOUN', 'lay': 'VERB', 'against': 'ADP', 'pattern': 'NOUN', 'slow': 'ADJ', 'center': 'NOUN', 'love': 'VERB', 'person': 'NOUN', 'money': 'NOUN', 'serve': 'VERB', 'appear': 'VERB', 'road': 'NOUN', 'map': 'NOUN', 'science': 'NOUN', 'rule': 'NOUN', 'govern': 'NOUN', 'pull': 'VERB', 'cold': 'ADJ', 'notice': 'NOUN', 'voice': 'NOUN', 'fall': 'VERB', 'power': 'NOUN', 'town': 'NOUN', 'fine': 'ADJ', 'certain': 'ADJ', 'fly': 'NOUN', 'unit': 'NOUN', 'lead': 'VERB', 'cry': 'VERB', 'dark': 'ADJ', 'machine': 'NOUN', 'note': 'NOUN', 'wait': 'VERB', 'plan': 'NOUN', 'figure': 'NOUN', 'star': 'NOUN', 'box': 'NOUN', 'noun': 'NOUN', 'field': 'NOUN', 'rest': 'NOUN', 'correct': 'ADJ', 'able': 'ADJ', 'pound': 'NOUN', 'done': 'VERB', 'beauty': 'NOUN', 'drive': 'NOUN', 'stood': 'VERB', 'contain': 'VERB', 'front': 'NOUN', 'teach': 'NOUN', 'week': 'NOUN', 'final': 'ADJ', 'gave': 'VERB', 'green': 'ADJ', 'oh': 'INTJ', 'quick': 'ADJ', 'develop': 'VERB', 'sleep': 'NOUN', 'warm': 'ADJ', 'free': 'ADJ', 'minute': 'NOUN', 'strong': 'ADJ', 'special': 'ADJ', 'mind': 'NOUN', 'behind': 'ADP', 'clear': 'ADJ', 'tail': 'NOUN', 'produce': 'VERB', 'fact': 'NOUN', 'street': 'NOUN', 'inch': 'NOUN', 'lot': 'NOUN', 'nothing': 'PRON', 'course': 'NOUN', 'stay': 'VERB', 'wheel': 'NOUN', 'full': 'ADJ', 'force': 'NOUN', 'blue': 'ADJ', 'object': 'NOUN', 'decide': 'VERB', 'surface': 'NOUN', 'deep': 'ADJ', 'moon': 'NOUN', 'island': 'NOUN', 'foot': 'NOUN', 'yet': 'ADV', 'busy': 'ADJ', 'test': 'NOUN', 'record': 'NOUN', 'boat': 'NOUN', 'common': 'ADJ', 'gold': 'NOUN', 'possible': 'ADJ', 'plane': 'NOUN', 'age': 'NOUN', 'dry': 'ADJ', 'wonder': 'NOUN', 'laugh': 'NOUN', 'thousand': 'NUM', 'ago': 'ADV', 'ran': 'VERB', 'check': 'NOUN', 'game': 'NOUN', 'shape': 'NOUN', 'yes': 'INTJ', 'cool': 'ADJ', 'miss': 'NOUN', 'brought': 'VERB', 'heat': 'NOUN', 'snow': 'NOUN', 'bed': 'NOUN', 'bring': 'VERB', 'sit': 'VERB', 'perhaps': 'ADV', 'fill': 'VERB', 'east': 'NOUN', 'weight': 'NOUN', 'language': 'NOUN', 'among': 'ADP'}

        word_dict = {k.lower(): v for k, v in word_dict.items()}

        # Edit to include the Six
        word_dict["who"] = 'Q'
        word_dict["what"] = 'Q'
        word_dict["where"] = 'Q'
        word_dict["why"] = 'Q'
        word_dict["when"] = 'Q'
        word_dict["how"] = 'Q'

        return word_dict
