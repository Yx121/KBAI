import string
import time
from collections import defaultdict


class LinguisticAnalysis:
    def __init__(self):
        # If you want to do any initial processing, add it here.
        pass

    def load(self):
        word_dict = {'Serena': 'PROPN', 'Andrew': 'PROPN', 'Bobbie': 'PROPN', 'Cason': 'PROPN', 'David': 'PROPN',
                     'Farzana': 'PROPN', 'Frank': 'PROPN', 'Hannah': 'PROPN', 'Ida': 'PROPN', 'Irene': 'PROPN',
                     'Jim': 'PROPN', 'Jose': 'PROPN', 'Keith': 'PROPN', 'Laura': 'PROPN', 'Lucy': 'PROPN',
                     'Meredith': 'PROPN', 'Nick': 'PROPN', 'Ada': 'PROPN', 'Yeeling': 'PROPN', 'Yan': 'PROPN',
                     'the': 'DET', 'of': 'ADP', 'to': 'ADP', 'and': 'CCONJ', 'a': 'DET', 'in': 'NOUN', 'is': 'AUX',
                     'it': 'PRON', 'you': 'PRON', 'that': 'SCONJ', 'he': 'PRON', 'was': 'AUX', 'for': 'ADP',
                     'on': 'ADV', 'are': 'AUX', 'with': 'ADP', 'as': 'ADP', 'I': 'PRON', 'his': 'PRON',
                     'they': 'PRON', 'be': 'VERB', 'at': 'ADP', 'one': 'NUM', 'have': 'VERB', 'this': 'DET',
                     'from': 'ADP', ' or ': 'CCONJ', 'had': 'VERB', 'by': 'ADP', 'hot': 'ADJ', 'but': 'CCONJ',
                     'some': 'DET', 'what': 'PRON', 'there': 'ADV', 'we': 'PRON', 'can': 'AUX', 'out': 'ADV',
                     'other': 'ADJ', 'were': 'AUX', 'all': 'DET', 'your': 'PRON', 'when': 'ADV', 'up': 'ADP',
                     'use': 'VERB', 'word': 'NOUN', 'how': 'ADV', 'said': 'VERB', 'an': 'DET', 'each': 'DET',
                     'she': 'PRON', 'which': 'DET', 'do': 'VERB', 'their': 'PRON', 'time': 'NOUN', 'if': 'SCONJ',
                     'will': 'AUX', 'way': 'VERB', 'about': 'ADV', 'many': 'ADJ', 'then': 'ADV', 'them': 'PRON',
                     'would': 'AUX', 'write': 'VERB', 'like': 'ADP', 'so': 'ADV', 'these': 'DET', 'her': 'PRON',
                     'long': 'ADJ', 'make': 'NOUN', 'thing': 'NOUN', 'see': 'VERB', 'him': 'PRON', 'two': 'NUM',
                     'has': 'AUX', 'look': 'VERB', 'more': 'ADJ', 'day': 'NOUN', 'could': 'AUX', 'go': 'VERB',
                     'come': 'VERB', 'did': 'VERB', 'my': 'PRON', 'sound': 'NOUN', 'no': 'DET', 'most': 'ADJ',
                     'number': 'NOUN', 'who': 'PRON', 'over': 'ADP', 'know': 'VERB', 'water': 'NOUN',
                     'than': 'SCONJ', 'call': 'VERB', 'first': 'ADJ', 'people': 'NOUN', 'may': 'AUX', 'down': 'ADV',
                     'side': 'NOUN', 'been': 'AUX', 'now': 'ADV', 'find': 'VERB', 'any': 'DET', 'new': 'ADJ',
                     'work': 'NOUN', 'part': 'NOUN', 'take': 'VERB', 'get': 'VERB', 'place': 'NOUN', 'made': 'VERB',
                     'live': 'ADJ', 'where': 'ADV', 'after': 'ADP', 'back': 'ADV', 'little': 'ADJ', 'only': 'ADJ',
                     'round': 'ADJ', 'man': 'NOUN', 'year': 'TIME', 'came': 'VERB', 'show': 'VERB', 'every': 'DET',
                     'good': 'ADJ', 'me': 'PRON', 'give': 'VERB', 'our': 'PRON', 'under': 'ADP', 'name': 'NOUN',
                     'very': 'ADV', 'through': 'ADP', 'just': 'ADV', 'form': 'VERB', 'much': 'ADV', 'great': 'ADJ',
                     'think': 'NOUN', 'say': 'VERB', 'help': 'VERB', 'low': 'ADJ', 'line': 'NOUN', 'before': 'ADP',
                     'turn': 'NOUN', 'cause': 'VERB', 'same': 'ADJ', 'mean': 'NOUN', 'differ': 'VERB',
                     'move': 'NOUN', 'right': 'ADJ', 'boy': 'INTJ', 'old': 'ADJ', 'too': 'ADV', 'does': 'AUX',
                     'tell': 'VERB', 'sentence': 'NOUN', 'set': 'NOUN', 'three': 'NUM', 'want': 'ADJ',
                     'air': 'NOUN', 'well': 'ADV', 'also': 'ADV', 'play': 'VERB', 'small': 'ADJ', 'end': 'NOUN',
                     'put': 'VERB', 'home': 'ADV', 'read': 'VERB', 'hand': 'NOUN', 'port': 'NOUN', 'large': 'ADJ',
                     'spell': 'NOUN', 'add': 'VERB', 'even': 'ADV', 'land': 'NOUN', 'here': 'ADV', 'must': 'AUX',
                     'big': 'ADJ', 'high': 'ADJ', 'such': 'ADJ', 'follow': 'NOUN', 'act': 'NOUN', 'why': 'ADV',
                     'ask': 'VERB', 'men': 'NOUN', 'change': 'VERB', 'went': 'VERB', 'light': 'ADJ', 'kind': 'NOUN',
                     'off': 'ADV', 'need': 'VERB', 'house': 'NOUN', 'picture': 'NOUN', 'try': 'VERB', 'us': 'PRON',
                     'again': 'ADV', 'animal': 'NOUN', 'point': 'NOUN', 'mother': 'NOUN', 'world': 'NOUN',
                     'near': 'SCONJ', 'build': 'VERB', 'self': 'NOUN', 'earth': 'NOUN', 'father': 'NOUN',
                     'head': 'NOUN', 'stand': 'VERB', 'own': 'ADJ', 'page': 'NOUN', 'should': 'AUX',
                     'country': 'NOUN', 'found': 'VERB', 'answer': 'NOUN', 'school': 'NOUN', 'grow': 'NOUN',
                     'study': 'NOUN', 'still': 'ADV', 'learn': 'VERB', 'plant': 'NOUN', 'cover': 'VERB',
                     'food': 'NOUN', 'sun': 'NOUN', 'four': 'NUM', 'thought': 'VERB', 'let': 'VERB', 'keep': 'VERB',
                     'eye': 'NOUN', 'never': 'ADV', 'last': 'ADJ', 'door': 'NOUN', 'between': 'ADP', 'city': 'NOUN',
                     'tree': 'NOUN', 'cross': 'NOUN', 'since': 'SCONJ', 'hard': 'ADJ', 'start': 'NOUN',
                     'might': 'AUX', 'story': 'NOUN', 'saw': 'VERB', 'far': 'ADJ', 'sea': 'NOUN', 'draw': 'NOUN',
                     'left': 'VERB', 'late': 'ADJ', 'run': 'NOUN', 'donít': 'NOUN', 'while': 'SCONJ',
                     'press': 'NOUN', 'close': 'ADJ',
                     'night': 'NOUN', 'real': 'ADJ', 'life': 'NOUN', 'few': 'ADJ', 'stop': 'VERB', 'open': 'ADJ',
                     'seem': 'VERB', 'together': 'ADV', 'next': 'ADP', 'white': 'ADJ', 'children': 'NOUN',
                     'begin': 'VERB', 'got': 'VERB', 'walk': 'VERB', 'example': 'NOUN', 'ease': 'NOUN',
                     'paper': 'NOUN', 'often': 'ADV', 'always': 'ADV', 'music': 'VERB', 'those': 'DET',
                     'both': 'DET', 'mark': 'NOUN', 'book': 'NOUN', 'letter': 'NOUN', 'until': 'ADP',
                     'mile': 'NOUN', 'river': 'NOUN', 'car': 'NOUN', 'feet': 'NOUN', 'care': 'VERB',
                     'second': 'ADJ', 'group': 'NOUN', 'carry': 'NOUN', 'took': 'VERB', 'rain': 'NOUN',
                     'eat': 'NOUN', 'room': 'NOUN', 'friend': 'NOUN', 'began': 'VERB', 'idea': 'NOUN',
                     'fish': 'NOUN', 'mountain': 'NOUN', 'north': 'NOUN', 'once': 'ADV', 'base': 'NOUN',
                     'hear': 'VERB', 'horse': 'NOUN', 'cut': 'VERB', 'sure': 'ADJ', 'watch': 'NOUN',
                     'color': 'NOUN', 'face': 'VERB', 'wood': 'NOUN', 'main': 'ADJ', 'enough': 'ADJ',
                     'plain': 'ADJ', 'girl': 'NOUN', 'usual': 'ADJ', 'young': 'ADJ', 'ready': 'ADJ', 'above': 'ADP',
                     'ever': 'ADV', 'red': 'ADJ', 'list': 'NOUN', 'though': 'ADV', 'feel': 'VERB', 'talk': 'NOUN',
                     'bird': 'NOUN', 'soon': 'ADV', 'body': 'NOUN', 'dog': 'NOUN', 'family': 'NOUN',
                     'direct': 'ADJ', 'pose': 'NOUN', 'leave': 'VERB', 'song': 'NOUN', 'measure': 'NOUN',
                     'state': 'NOUN', 'product': 'NOUN', 'black': 'ADJ', 'short': 'ADJ', 'numeral': 'ADJ',
                     'class': 'NOUN', 'wind': 'NOUN', 'question': 'NOUN', 'happen': 'VERB', 'complete': 'ADJ',
                     'ship': 'NOUN', 'area': 'NOUN', 'half': 'ADJ', 'rock': 'NOUN', 'order': 'NOUN', 'fire': 'NOUN',
                     'south': 'ADJ', 'problem': 'NOUN', 'piece': 'NOUN', 'told': 'VERB', 'knew': 'VERB',
                     'pass': 'VERB', 'farm': 'NOUN', 'top': 'ADJ', 'whole': 'ADJ', 'king': 'NOUN', 'size': 'NOUN',
                     'heard': 'VERB', 'best': 'ADJ', 'hour': 'NOUN', 'better': 'ADV', 'TRUE': 'ADV',
                     'during': 'ADP', 'hundred': 'NUM', 'am': 'VERB', 'remember': 'VERB', 'step': 'NOUN',
                     'early': 'ADV', 'hold': 'VERB', 'west': 'ADJ', 'ground': 'NOUN', 'interest': 'NOUN',
                     'reach': 'VERB', 'fast': 'ADV', 'five': 'NUM', 'sing': 'VERB', 'listen': 'NOUN', 'six': 'NUM',
                     'table': 'NOUN', 'travel': 'NOUN', 'less': 'ADJ', 'morning': 'NOUN', 'ten': 'NUM',
                     'simple': 'ADJ', 'several': 'ADJ', 'vowel': 'NOUN', 'toward': 'ADP', 'war': 'NOUN',
                     'lay': 'VERB', 'against': 'ADP', 'pattern': 'NOUN', 'slow': 'ADJ', 'center': 'NOUN',
                     'love': 'VERB', 'person': 'NOUN', 'money': 'NOUN', 'serve': 'VERB', 'appear': 'VERB',
                     'road': 'NOUN', 'map': 'NOUN', 'science': 'NOUN', 'rule': 'NOUN', 'govern': 'NOUN',
                     'pull': 'VERB', 'cold': 'ADJ', 'notice': 'NOUN', 'voice': 'NOUN', 'fall': 'VERB',
                     'power': 'NOUN', 'town': 'NOUN', 'fine': 'ADJ', 'certain': 'ADJ', 'fly': 'NOUN',
                     'unit': 'NOUN', 'lead': 'VERB', 'cry': 'VERB', 'dark': 'ADJ', 'machine': 'NOUN',
                     'note': 'NOUN', 'wait': 'VERB', 'plan': 'NOUN', 'figure': 'NOUN', 'star': 'NOUN',
                     'box': 'NOUN', 'noun': 'NOUN', 'field': 'NOUN', 'rest': 'NOUN', 'correct': 'ADJ',
                     'able': 'ADJ', 'pound': 'NOUN', 'done': 'VERB', 'beauty': 'NOUN', 'drive': 'NOUN',
                     'stood': 'VERB', 'contain': 'VERB', 'front': 'NOUN', 'teach': 'NOUN', 'week': 'NOUN',
                     'final': 'ADJ', 'gave': 'VERB', 'green': 'ADJ', 'oh': 'INTJ', 'quick': 'ADJ',
                     'develop': 'VERB', 'sleep': 'NOUN', 'warm': 'ADJ', 'free': 'ADJ', 'minute': 'NOUN',
                     'strong': 'ADJ', 'special': 'ADJ', 'mind': 'NOUN', 'behind': 'ADP', 'clear': 'ADJ',
                     'tail': 'NOUN', 'produce': 'VERB', 'fact': 'NOUN', 'street': 'NOUN', 'inch': 'NOUN',
                     'lot': 'NOUN', 'nothing': 'PRON', 'course': 'NOUN', 'stay': 'VERB', 'wheel': 'NOUN',
                     'full': 'ADJ', 'force': 'NOUN', 'blue': 'ADJ', 'object': 'NOUN', 'decide': 'VERB',
                     'surface': 'NOUN', 'deep': 'ADJ', 'moon': 'NOUN', 'island': 'NOUN', 'foot': 'NOUN',
                     'yet': 'ADV', 'busy': 'ADJ', 'test': 'NOUN', 'record': 'NOUN', 'boat': 'NOUN', 'common': 'ADJ',
                     'gold': 'NOUN', 'possible': 'ADJ', 'plane': 'NOUN', 'age': 'NOUN', 'dry': 'ADJ',
                     'wonder': 'NOUN', 'laugh': 'NOUN', 'thousand': 'NUM', 'ago': 'ADV', 'ran': 'VERB',
                     'check': 'NOUN', 'game': 'NOUN', 'shape': 'NOUN', 'yes': 'INTJ', 'cool': 'ADJ', 'miss': 'NOUN',
                     'brought': 'VERB', 'heat': 'NOUN', 'snow': 'NOUN', 'bed': 'NOUN', 'bring': 'VERB',
                     'sit': 'VERB', 'perhaps': 'ADV', 'fill': 'VERB', 'east': 'NOUN', 'weight': 'NOUN',
                     'language': 'NOUN', 'among': 'ADP'}

        word_dict = {key.lower(): tag for key, tag in word_dict.items()}
        word_dict.update(dict.fromkeys(['who', 'what', 'where', 'why', 'when', 'how'], 'Q'))
        return word_dict


def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))


def get_word_dict(words, linguistic_data):
    word_dict = defaultdict(list)
    for word in words:
        tag = linguistic_data.get(word)
        word_dict[tag].append(word)
    return word_dict


class SentenceReadingAgent:
    def __init__(self):
        # If you want to do any initial processing, add it here.
        self.la = LinguisticAnalysis()
        self.d = self.la.load()
        pass

    def process_text(self, text):
        text = remove_punctuation(text)
        words = text.lower().split()
        return get_word_dict(words, self.d), words

    def solve(self, sentence, question):
        words_s, raw_words_s = self.process_text(sentence)
        words_q, raw_words_q = self.process_text(question)
        sentence_split = sentence.split()

        if "who" in raw_words_q:
            sentence_propn_lst = words_s.get('PROPN')
            sentence_noun_lst = words_s.get('NOUN')
            question_propn_lst = words_q.get('PROPN')

            if not question_propn_lst and sentence_propn_lst:
                return sentence_propn_lst[0].capitalize()
            elif question_propn_lst and len(question_propn_lst) == 1 and question_propn_lst[0] in sentence_propn_lst:
                sentence_propn_lst.remove(question_propn_lst[0])
                return sentence_propn_lst[0].capitalize()
            elif sentence_propn_lst:
                return sentence_propn_lst[0].capitalize()
            elif sentence_noun_lst:
                return sentence_noun_lst[0]
            else:
                return None

        if "when" in raw_words_q:
            when_keywords = {"day", "night", "morning", "yesterday", "today"}
            matching_word = next((i for i in raw_words_s if i in when_keywords), None)
            if matching_word:
                return matching_word
            return next(iter(words_s.get('ADV', [])), None)

        if "where" in raw_words_q:
            sentence_noun_lst = words_s.get('NOUN', [])
            question_noun_lst = words_q.get('NOUN', [])

            def get_location_index(keyword):
                if keyword in raw_words_s:
                    return raw_words_s.index(keyword) + 2
                return None

            for keyword in ["go", "in"]:
                location_index = get_location_index(keyword)
                if location_index is not None:
                    return raw_words_s[location_index]

            if question_noun_lst and sentence_noun_lst:
                sentence_noun_lst.remove(question_noun_lst[0])
                return sentence_noun_lst[0] if sentence_noun_lst else None

            return next(iter(sentence_noun_lst), None)

        if "time" in raw_words_q:
            return next((i for i in sentence_split if ":" in i), None)

        if "what" in raw_words_q:
            get_first_item = lambda x: next(iter(x or []), None)

            if 'name' in raw_words_q:
                return next((i for i in sentence_split[1:] if i[0].isupper()), None)

            if 'do' in raw_words_q:
                return get_first_item(words_s.get('VERB'))

            if 'color' in raw_words_q:
                color = get_first_item(words_s.get('ADJ'))
                if color:
                    return color

                subject = get_first_item(words_q.get('NOUN'))
                if subject:
                    index = sentence_split.index(subject)
                    return sentence_split[index - 1]

            nouns_diff = list(set(words_q.get('NOUN', [])) ^ set(words_s.get('NOUN', [])))
            return get_first_item(
                nouns_diff or words_s.get('NOUN') or words_s.get('ADJ') or words_s.get('VERB')
            )

        if "how" in raw_words_q:
            after_how = raw_words_q[1]
            tag = self.d.get(after_how)

            def get_first_item(tag):
                return next(iter(words_s.get(tag, [])), None)

            if "many" in raw_words_q:
                sentence_num_lst = words_s.get('NUM', [])
                return ' '.join(sentence_num_lst) if sentence_num_lst else None

            if "much" in raw_words_q:
                return get_first_item('DET')

            if tag == 'ADJ':
                return get_first_item('ADJ') or get_first_item('NOUN') or get_first_item('ADV')

            if tag == 'VERB':
                return get_first_item('VERB')


