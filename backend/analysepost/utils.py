def sentiment_analysis(text):
    pass

def entity_extraction(text):
    pass

def data_source_verification(text):
    pass

def source_credibility_analysis(user):
    pass


def detect_fake_news(data):
    if isinstance(data, list) and len(data) > 0:
        data = data[0]  

    text = data['content']
    is_fake = False

    sentiment = sentiment_analysis(text)
    entities = entity_extraction(text)
    verified = data_source_verification(text)
    credible = source_credibility_analysis(data['user'])
    if not (sentiment and entities and verified and credible):
        is_fake = True

    return is_fake

