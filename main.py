import spacy
import os
from thefuzz import fuzz
from rouge import Rouge

#######################STOP WORDS##############################################

STOP_WORDS = set(
    """
a about above across after afterwards again against all almost alone along
already also although always am among amongst amount an and another any anyhow
anyone anything anyway anywhere are around as at

back be became because become becomes becoming been before beforehand behind
being below beside besides between beyond both bottom but by

call can cannot ca could

did do does doing done down due during

each eight either eleven else elsewhere empty enough even ever every
everyone everything everywhere except

few fifteen fifty first five for former formerly forty four from front full
further

get give go

had has have he hence her here hereafter hereby herein hereupon hers herself
him himself his how however hundred

i if in indeed into is it its itself

keep

last latter latterly least less

just

made make many may me meanwhile might mine more moreover most mostly move much
must my myself

name namely neither never nevertheless next nine no nobody none noone nor not
nothing now nowhere

of off often on once one only onto or other others otherwise our ours ourselves
out over own

part per perhaps please put

quite

rather re really regarding

same say see seem seemed seeming seems serious several she should show side
since six sixty so some somehow someone something sometime sometimes somewhere
still such

take ten than that the their them themselves then thence there thereafter
thereby therefore therein thereupon these they third this those though three
through throughout thru thus to together too top toward towards twelve twenty
two

under until up unless upon us used using

various very very via was we well were what whatever when whence whenever where
whereafter whereas whereby wherein whereupon wherever whether which while
whither who whoever whole whom whose why will with within without would

yet you your yours yourself yourselves
""".split()
)

contractions = ["n't", "'d", "'ll", "'m", "'re", "'s", "'ve"]
STOP_WORDS.update(contractions)

for apostrophe in ["‘", "’"]:
    for stopword in contractions:
        STOP_WORDS.add(stopword.replace("'", apostrophe))

###############################################################################

#######################PUNCTUATION#############################################

punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

###############################################################################


def getRatio(metin, ozet):

    #######################SPACY###################################################

    nlp = spacy.load("en_core_web_sm")

    ozetmetin = ozet.read()

    doc = nlp(metin.read())

    ###############################################################################

    #######################KEYWORDS################################################

    keywords = []
    stopwords = list(STOP_WORDS)
    post_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']

    for token in doc:
        if (token.text in stopwords or token.text in punctuation):
            continue

        if (token.pos_ in post_tag):
            keywords.append(token.text)

    # print(keywords)

    ###############################################################################

    #######################FREQ WORDS##############################################

    freq_words = {}

    for keyword in keywords:
        if keyword in freq_words.keys():
            freq_words[keyword] += 1
        else:
            freq_words[keyword] = 1

    freq_list = list(freq_words.items())

    for x in range(len(freq_list)-1, -1, -1):
        swapped = False
        for i in range(x):
            if freq_list[i][1] < freq_list[i+1][1]:
                freq_list[i], freq_list[i+1] = freq_list[i+1], freq_list[i]
                swapped = True
        if not swapped:
            break

    freq_words = dict(freq_list)
    # print(freq_words)

    max_freq = freq_list[0][1]

    for word in freq_words.keys():
        freq_words[word] = (freq_words[word]/max_freq)

    # print(freq_words)

    ###############################################################################

    #######################SENT STRENGTH###########################################

    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_words.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent] += freq_words[word.text]
                else:
                    sent_strength[sent] = freq_words[word.text]

    # print(sent_strength)
    ###############################################################################

    #######################SUMMARY#################################################

    summarized_sentences = sorted(
        sent_strength, key=sent_strength.get, reverse=True)[0:4]

    final_sentences = [w.text for w in summarized_sentences]
    summary = ''.join(final_sentences)

    # print(summary)
    # print("\n\n******\n\n")
    # print(ozetmetin)

    ###############################################################################

    #######################RATIO###################################################

    ROUGE = Rouge()
    rouge = ROUGE.get_scores(summary, ozetmetin)
    print("rouge: {}".format(rouge))

    ratio = fuzz.ratio(summary, ozetmetin)
    print('Benzerlik skoru: {}'.format(ratio))

    return ratio
    ###############################################################################


ratios = []

# sum = 0

# for i in rr:
#     sum = sum + i

# print(sum)
# print(len(rr))

files = ["business", "entertainment", "politics", "sport", "tech"]

for f in files:
    a_path = "C:\\Users\\mss_2\\Desktop\\BBC News Summary\\News Articles\\"+f
    s_path = "C:\\Users\\mss_2\\Desktop\\BBC News Summary\\Summaries\\"+f
    dosyalar = os.listdir(a_path)

    for i in dosyalar:
        print(i)
        metin = open(a_path + "\\" + i, "r")
        ozet = open(s_path + "\\" + i, "r")

        r = getRatio(metin, ozet)
        ratios.append(r)

print(ratios)
