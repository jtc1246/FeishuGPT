import tiktoken


def get_tokens(text):
    enc = tiktoken.encoding_for_model('gpt-4')
    l = len(enc.encode(text))
    return l


def safe_token_count(text):
    return round(get_tokens(text) * 1.025) + 10


def tokens_score(preferred_max, preferred_min):
    def func1(token_num):
        if (token_num < 50):
            return -100000000.0
        if (preferred_min <= token_num and token_num <= preferred_max):
            return (65 + (token_num - preferred_min) / (preferred_max - preferred_min) * 25)
        if (token_num >= preferred_max):
            return (90 + (token_num - preferred_max) / (preferred_max - preferred_min) * 25 * 0.4)
        if (token_num >= preferred_min - (preferred_max - preferred_min)):
            return (65 - (preferred_min - token_num) / (preferred_max - preferred_min) * 25 * 2)
        return (65 - (preferred_min - token_num) / (preferred_max - preferred_min) * 25 * 3.5)

    score_2048 = func1(2048)

    def func2(token_num):
        return min(score_2048, func1(token_num))

    return func2


# 根据历史聊天记录，根据token数量限制，返回合适的聊天记录
# 输入格式与 openai.ChatCompletion.create 中的 messages 相同（不考虑长度限制）
# 输出为一个tuple，第一项为一个正整数，表示保留几条信息（包含最后用户提问的，不包含system），第二项为回答可用token
# 对回答长度、保留聊天记录数量使用打分机制，采用分数最高的结果
def get_msg_count(history):
    assistant = history[2::2]
    l = len(assistant)
    all = 0
    for a in assistant:
        all += safe_token_count(a['content'])
    avg_length = round(all / l)
    stdev = 0
    if (l == 1):
        stdev = safe_token_count(assistant[-1]['content']) / 2.5
    else:
        for a in assistant:
            stdev += safe_token_count(a['content'])**2
        stdev = (stdev / (l - 1))**0.5
    near_avg_length = -1
    if (l <= 3):
        near_avg_length = avg_length
    else:
        near_avg_length = round((safe_token_count(assistant[-1]['content']) + safe_token_count(
            assistant[-2]['content']) + safe_token_count(assistant[-3]['content'])) / 3)
    highest_score = -100000000
    highest_index = -1
    highest_score_tokens = -1
    preferred_max = max(avg_length, near_avg_length) + 2 * stdev  # 90分
    preferred_min = min(avg_length, near_avg_length) + stdev  # 65分
    score_func = tokens_score(preferred_max, preferred_min)
    l = len(history)
    msg_tokens = []
    for h in history:
        msg_tokens.append(safe_token_count(h['content']))
    for i in range(1, l):
        msg_count_score = 0
        for j in range(0, i):
            msg_count_score += 1 / (j + 3)
        msg_count_score = msg_count_score / 1.7516 * 100
        tokens = 8182 - msg_tokens[0]
        for j in range(-1, -i - 1, -1):
            tokens -= msg_tokens[j]
        token_score = score_func(tokens)
        final_score = msg_count_score + token_score
        if (final_score > highest_score):
            highest_score = final_score
            highest_index = i
            highest_score_tokens = round(tokens)
    return (highest_index, highest_score_tokens)

def filter_history(history):
    num, token = get_msg_count(history)
    messages = [history[0]] + history[-num:]
    return (messages, min(token, 2048))
