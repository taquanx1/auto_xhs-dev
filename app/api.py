from openai import OpenAI
import os
from pydantic import BaseModel, create_model


def xhs_note_gen(seed_dic, model="sonar-reasoning-pro"):
    LLM_API_KEY = os.getenv("LLM_API_KEY")

    #unpack the seed_dic
    location = seed_dic["location"]
    subject = seed_dic["subject"]
    count = seed_dic["count"]
    attributes = seed_dic["attributes"]
    options = seed_dic["options"]

    attributes_str = ', '.join(attributes)

    #contruct schema
    fields = {
        'main_title': (str, ...)
    }
    # Add dynamic fields like item_title_1, item_title_2, ...
    for i in range(1, int(count) + 1):
        field_name = f'item_title_{i}'
        fields[field_name] = (str, ...)
        field_name = f'item_content_{i}'
        fields[field_name] = (str, ...)
    # Create the model
    ResponseFormat = create_model('DynamicResponseFormat', **fields)

    messages = [
        {
            "role": "system",
            "content": (
                "你是小红书著名的网红旅游经验干货分享类博主，你的职责是写出诚恳干货的小红书笔记，你的风格是诚恳体贴爱使用表情"
            ),
        },
        {
            "role": "user",
            "content": (
                f"""
        小红书网红笔记,躺平慢生活轻奢风格篇关于 {location} {str(count)}{subject}
        的旅游笔记攻略，分类列出每个对象的信息比如{attributes_str}诚恳干货风格，
        并添加更多内容，多用表情，多表达自己的见解和建议。
        分成{str(count)}个 bullet points, 
        每个 bullet points 的标题只包含对象名的英语名称, 每个介绍写得很详细，带有个人主观意见
        
        每个 bullet points 满足这个格式
        [英语名称]
        [attributes 1]
        [attributes 2]
        [attributes 3]
        ...
                    """
                ),
            },
    ]


    response_format = {
            "type": "json_schema",
            "json_schema": {
                "schema": ResponseFormat.model_json_schema()
            }
    }

    client = OpenAI(api_key=LLM_API_KEY, base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format=response_format,
    )
    print(response.choices[0].message.content)

    return response.choices[0].message.content
