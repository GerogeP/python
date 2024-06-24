import json
import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

# 从环境变量中获取 API 密钥
gpt_api_key = os.getenv("EC_TK_DEV1")

client = AsyncOpenAI(
    api_key=gpt_api_key,
)

llm_role = """You are a Business Development (BD) professional at an e-commerce company, responsible for establishing connections with TikTok influencers to facilitate collaborations and promote products.
"""
bd_header = "<BD's message>:\n"
inf_header = "<influencer's reply>:\n"


def get_prompt(facts: str, dialog: str) -> str:
    return (
            facts
            + """
The dialogue between BD and influencer is listed below:
```
"""
            + dialog
            + """
```
First, please help classify the influencer's intent based on the following categories:
1) Agree to collaborate - Agrees to cooperate without any conditions or additional requirements. Suggested reply: encourage the influencer to request a sample.
2) Request higher commission - Requests a higher commission rate. Suggested reply: we need internal discussion.
3) Request for samples - Requests samples to be sent without specifying the sample specifications. Suggested reply: encourage the influencer to request via the sample request URL.
4) Specification request - Requests samples with specified characteristics (such as size, color). Suggested reply: we need further confirmation for the availability of any specification.
5) Confirm the specification -  Confirm the sample spec. Suggested reply: thanks, we'll ship it ASAP.
6) Refuse to collaborate - Refuses to collaborate with us. Suggested reply: encourage the influencer to contact us when mind changed.
7) Shipment status inquiry - Query the shipment status. Suggested reply: we need further confirmation.
8) Other - Default category for responses that do not fit the above categories. 

Then, please write a message to reply the influencer (refer to the influencer's intent and corresponding reply suggestions). Please use the style of an instant messaging chat and make it very concise. Do NOT use any placeholders like [Your Name], [Brand Name], etc.
Please write message based on the materials in the previous text and indicate your confidence level in the answer as either 'confirmed' or 'uncertain'. And give the materials you referenced to write the message.


Please provide a response in JSON format as follows: {"intent_category": "influencer's intent", "message": "suggested message to the influencer", "confidence": "confirmed or uncertain", "referenced_materials":["Masterial 1", "Material 3"]}.
"""
    )


async def get_completion(prompt, model="gpt-3.5-turbo") -> AsyncGenerator[str, None]:
    print("-------- prompt----------")
    print(prompt)
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": llm_role,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model=model,
    )

    print("--------response --------")
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content


def format_rsp(rsp):
    if len(rsp):
        jstr = rsp.replace("```json", "").replace("```", "")
        js = json.loads(jstr)
        return js
    return {}


async def send_to_influencer(influencer_name, influencer_tags, materials, dialog):
    inf_param = f"The influencer's name is {influencer_name}, and their content primarily focuses on {influencer_tags}.\n"
    materials = f"\nYou have the following materials available:\n{materials}\n"
    facts = inf_param + materials
    model = "gpt-4o"
    if len(dialog) == 0:
        # first msg
        first_msg_request = """This is your first contact with the influencer to introduce this product. 
        You need to write a message to send to the influencer via TikTok's online messaging. 
        Please highlight the product brief and commission with emoji. 
        Please use the style of an instant messaging chat and make it very concise. 
        And the message should NOT contain any placeholders like [Your Name], [Brand Name], etc.
        Please provide a response in JSON format as follows: {"intent_category": "BD's msg", "message": "the message to the influencer", "confidence": "", "referenced_materials":[]}.
"""
        msg = await get_completion(facts + first_msg_request, model=model)
        # message = format_rsp(msg)
        # return Success(data=message)
        return format_rsp(msg)
    else:
        msg = await get_completion(get_prompt(facts, dialog), model=model)
        # message = format_rsp(msg)
        # return Success(data=message)
        return format_rsp(msg)