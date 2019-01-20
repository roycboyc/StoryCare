import json
import credentials
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
import Features, EntitiesOptions, KeywordsOptions


def requestWatsonSentence(sentences):

    nlu = NaturalLanguageUnderstandingV1(version='2017-02-27',username=credentials.nluKey,password=credentials.nluId)

    keywords = dict()
    entities = dict()



    for i in range(len(sentences)):
        tmp = nlu.analyze(text=sentences[i],
                          features=Features(entities=EntitiesOptions(emotion=True,sentiment=True,limit=2),
                              keywords=KeywordsOptions(emotion=True,sentiment=True,limit=2)))
        keywords[len(keywords)] = [item.get('text',{}) for item in tmp.get('keywords',{}) if item.get("relevance") > 0.1]
        entities[len(entities)] = [item.get('text',{}) for item in tmp.get('entities',{}) if item.get("relevance") > 0.75]

    # return keywords, tones #'rtype': dictionary
    return entities, keywords
