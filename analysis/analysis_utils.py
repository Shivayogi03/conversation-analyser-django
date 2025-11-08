# analysis/analysis_utils.py
import re
import math
from collections import Counter

FALLBACK_PHRASES = [
    "i don't know", "i do not know", "sorry, i can't", "i'm not sure",
    "can't help with that", "i'm sorry i don't", "i don't have that info"
]

RESOLUTION_KEYWORDS = [
    "resolved", "fixed", "delivered", "shipped", "completed", "done", "closed", "refunded"
]

EMPATHY_KEYWORDS = [
    "sorry to hear", "i'm sorry", "i understand", "that must be", "i can help", "i understand how"
]

POSITIVE_WORDS = ["thanks","thank you","great","good","awesome","perfect","happy","love"]
NEGATIVE_WORDS = ["not happy","angry","disappointed","bad","terrible","hate","upset","frustrat"]

def simple_sentiment(text):
    t = text.lower()
    pos = sum(1 for w in POSITIVE_WORDS if w in t)
    neg = sum(1 for w in NEGATIVE_WORDS if w in t)
    if pos > neg: return "positive"
    if neg > pos: return "negative"
    return "neutral"

def count_fallbacks(messages):
    text = " ".join(m.text.lower() for m in messages)
    return sum(text.count(fr) for fr in FALLBACK_PHRASES)

def detect_resolution(messages):
    text = " ".join(m.text.lower() for m in messages)
    for kw in RESOLUTION_KEYWORDS:
        if kw in text:
            return True
    return False

def empathy_score(messages):
    ai_text = " ".join(m.text.lower() for m in messages if m.sender.lower()=="ai")
    matches = sum(1 for kw in EMPATHY_KEYWORDS if kw in ai_text)
    # normalize to 0-1
    return min(1.0, matches / 2.0)

def clarity_score(messages):
    # heuristics: average sentence length and presence of short directives
    ai_msgs = [m.text for m in messages if m.sender.lower()=="ai"]
    if not ai_msgs: return 0.0
    lengths = []
    for t in ai_msgs:
        words = re.findall(r"\w+", t)
        lengths.append(len(words))
    avg = sum(lengths)/len(lengths)
    # ideal avg sentence length for clarity: 10-25 words. Map to 0-1
    if avg <= 5: score = 0.5
    elif avg <=25:
        score = 1.0 - abs(avg-15)/15  # peak at 15
    else:
        score = max(0.0, 1.0 - (avg-25)/50)
    return round(max(0.0, min(1.0, score)),3)

def relevance_score(messages):
    # simple: fraction of AI messages containing words from user messages
    user_text = " ".join(m.text.lower() for m in messages if m.sender.lower()=="user")
    ai_msgs = [m.text.lower() for m in messages if m.sender.lower()=="ai"]
    if not ai_msgs or not user_text: return 0.0
    user_words = set(re.findall(r"\w+", user_text))
    scores=[]
    for a in ai_msgs:
        a_words = set(re.findall(r"\w+", a))
        inter = user_words.intersection(a_words)
        scores.append(len(inter)/(len(a_words)+1))
    return round(sum(scores)/len(scores),3)

def accuracy_score(messages):
    # placeholder heuristic: penalize when AI uses "probably", "maybe", "might" or fallback
    ai_text = " ".join(m.text.lower() for m in messages if m.sender.lower()=="ai")
    uncertainty = sum(ai_text.count(w) for w in ["probably","maybe","might","unsure","can't verify"])
    fallback = count_fallbacks(messages)
    # map to 0-1
    score = 1.0 - min(1.0, (uncertainty*0.3 + fallback*0.6))
    return round(max(0.0, score),3)

def completeness_score(messages):
    # heuristic: does AI ask clarifying questions? if yes, lower completeness
    ai_text = " ".join(m.text.lower() for m in messages if m.sender.lower()=="ai")
    clarifying = sum(ai_text.count(q) for q in ["can you", "could you", "please share", "please provide", "what is"])
    # completeness decreases with clarifying questions; normalize
    score = max(0.0, 1.0 - min(0.9, clarifying * 0.15))
    return round(score,3)

def avg_response_time_mock(messages):
    # we accept mock: if timestamps exist compute, else random-ish deterministic based on length
    times = []
    ts = [m.timestamp for m in messages if m.timestamp]
    if len(ts) >= 2:
        # compute average diff between alternating messages
        import datetime
        diffs=[]
        for i in range(1,len(ts)):
            d = (ts[i] - ts[i-1]).total_seconds()
            diffs.append(abs(d))
        return round(sum(diffs)/len(diffs),2)
    # otherwise mock: base on number of messages
    return round(max(1.0, len(messages)*2.5),2)

def escalation_need(messages):
    # escalate if many negative user messages and no resolution
    user_texts = " ".join(m.text.lower() for m in messages if m.sender.lower()=="user")
    negs = sum(user_texts.count(w) for w in NEGATIVE_WORDS)
    resolved = detect_resolution(messages)
    return bool(negs >=2 and not resolved)

def resolution_rate(messages):
    # proportion of AI messages containing resolution keywords
    ai_texts = [m.text.lower() for m in messages if m.sender.lower()=="ai"]
    if not ai_texts: return 0.0
    hits = sum(1 for t in ai_texts if any(kw in t for kw in RESOLUTION_KEYWORDS))
    return round(hits/len(ai_texts),3)

def perform_analysis(conversation):
    """
    conversation: Conversation model instance with .messages queryset
    returns: dict with all metrics
    """
    messages = list(conversation.messages.all().order_by('id'))
    clarity = clarity_score(messages)
    relevance = relevance_score(messages)
    accuracy = accuracy_score(messages)
    completeness = completeness_score(messages)
    empathy = empathy_score(messages)
    sentiment = simple_sentiment(" ".join(m.text for m in messages if m.sender.lower()=="user"))
    fallback = count_fallbacks(messages)
    resolved = detect_resolution(messages)
    avg_rt = avg_response_time_mock(messages)
    escalate = escalation_need(messages)
    res_rate = resolution_rate(messages)
    # overall score: weighted average (customize weights)
    weights = {
        'clarity': 0.18, 'relevance':0.18, 'accuracy':0.18,
        'completeness':0.12, 'empathy':0.12, 'resolution_rate':0.12
    }
    overall = (
        clarity*weights['clarity'] +
        relevance*weights['relevance'] +
        accuracy*weights['accuracy'] +
        completeness*weights['completeness'] +
        empathy*weights['empathy'] +
        res_rate*weights['resolution_rate']
    )
    overall = round(overall,3)
    return {
        'clarity_score': clarity,
        'relevance_score': relevance,
        'accuracy_score': accuracy,
        'completeness_score': completeness,
        'empathy_score': empathy,
        'sentiment': sentiment,
        'fallback_count': fallback,
        'resolution': resolved,
        'avg_response_time': avg_rt,
        'escalation_need': escalate,
        'resolution_rate': res_rate,
        'overall_score': overall,
    }
