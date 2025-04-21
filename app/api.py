from openai import OpenAI
import os

def xhs_note_gen(seed_dic, model="sonar-reasoning-pro"):
    LLM_API_KEY = os.getenv("LLM_API_KEY")

    #unpack the seed_dic
    location = seed_dic["location"]
    subject = seed_dic["subject"]
    count = seed_dic["count"]
    attributes = seed_dic["attributes"]
    options = seed_dic["options"]

    attributes_str = ', '.join(attributes)

    messages = [
    {
        "role": "system",
        "content": (
            "你是小红书著名的网红旅游经验干货分享类博主，你的职责是写出诚恳干货的小红书笔记"
        ),
    },

    {
        "role": "user",
        "content": (
            f"""
    小红书网红笔记,躺平慢生活轻奢风格篇关于 {location} {str(count)}{subject}
    的旅游笔记攻略，分类列出每个对象的信息比如{attributes_str}诚恳干货风格，
    并添加更多内容，多用表情，多表达自己的见解和建议。
    文章要超过2000字，分成 bullet points, 每个介绍不超过 12 行
                """
            ),
        },
    ]

    client = OpenAI(api_key=LLM_API_KEY, base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    print(response.choices[0].message.content)

    return response.choices[0].message.content
