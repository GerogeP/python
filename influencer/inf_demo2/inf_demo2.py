import os
import sys
import json
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量中获取 API 密钥
gpt_api_key = os.getenv('EC_TK_DEV1')

client = OpenAI(
    api_key=gpt_api_key,
)

llm_role = '''You are a Business Development (BD) professional at an e-commerce company, responsible for establishing connections with TikTok influencers to facilitate collaborations and promote products. 
'''


def get_prompt(facts, dialog):
    return facts + '''
The dialogue between BD and influencers is listed below:
```
''' + dialog + '''
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
'''


bd_header = "<BD's message>:\n"
inf_header = "<influencer's reply>:\n"

def ask_gpt(m, q):
    print("-------- prompt----------")
    print(q)

    rsp = chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": llm_role,},
            {"role": "user", "content": q,},
        ],
        model=m,
    )   

    print("--------response --------")
    answer = rsp.choices[0].message.content
    print(answer)
    return answer 

dialog_sample='''<BD's message>:
🌟 Hey BlessedColette! 🌟

Hope you're having an amazing day! ✨ I stumbled upon your TikTok and absolutely love how you bring joy to everyday items. 🎉🪞

I think your followers would adore our latest product: Boho Rugs that are machine washable, non-slip, and beautifully designed for any room! 🏠💖 They're perfect from the kitchen to the bedroom and everything in between. Plus, they're at a steal with prices currently slashed by up to 41%! 🎈

🎁 Check them out here: https://afwjeoi.shop.tiktok.com

Would love to send you a free sample to try out. Just hit this link: https://mvlownoi.sample.shop.tiktok.com 🛍

Also, super exciting, we're offering a 20% commission on every sale through your link! 💸 

Can't wait to possibly work together! Let me know what you think! 😊

Cheers! 🌈

<influencer's reply>:
good, let's start

<BD's message>:
That's fantastic, BlessedColette! 🌟 We're thrilled to have you on board. Please go ahead and request your free sample through this link: https://mvlownoi.sample.shop.tiktok.com 🛍️ Once you get it, we can kick off this exciting collaboration! 💫

<influencer's reply>:
can I get the blue, 9*12 sized?

<BD's message>:
We're delighted you're interested in the blue, 9*12 size! We'll confirm the availability and get back to you shortly. 😊

<BD's message>:
Uh, well, the stock of the rug in blue 9x12 is running pretty low. Would it be okay if we replaced it with an 8x10 instead? I'll go ahead and update the sample info for you.

<influencer's reply>:
8x10 would work

'''


def format_rsp(rsp):
    jstr = rsp.replace("```json", "").replace("```", "")
    js = json.loads(jstr)
    return js


def send_to_influencer(influencer_name, influencer_tags, materials, dialog):
    inf_param = "The influencer's name is {}, and their content primarily focuses on {}.\n".format(influencer_name, influencer_tags)
    mat = "\nYou have the following materials available:\n{}\n".format(materials)
    facts = inf_param + mat
    m = "gpt-4o" # "gpt-4-turbo"
    if len(dialog) == 0:
        # first msg
        first_msg_request = '''This is your first contact with the influencer to introduce this product. You need to write a message to send to the influencer via TikTok's online messaging. Please highlight the product brief and commission with emoji. Please use the style of an instant messaging chat and make it very concise. And the message shoud NOT contain any placeholders like [Your Name], [Brand Name], etc.
Please provide a response in JSON format as follows: {"intent_category": "BD's msg", "message": "the message to the influencer", "confidence": "", "referenced_materials":[]}.
'''
        request1 = facts + first_msg_request
        raw_msg = ask_gpt(m, request1)
        return format_rsp(raw_msg)

    q = get_prompt(facts, dialog)
    raw_msg = ask_gpt(m, q)
    return format_rsp(raw_msg)
    

################### params (由前端传入) ##########################
influencer_name = "BlessedColette"
influencer_tags = "Toys, Kitchenware, Beauty & Personal Care"
materials = '''
Material 1: Product-related information: Machine Washable Area Rugs for Living Room Boho Rugs Carpet Non-Slip Easy Care Rugs Distressed Vintage Area Rugs Carpet for Bedroom Kitchen Indoor Washable Carpet, Non Slip No Pile 
Home Decor Floor Mat

Material 2: Pricing information: Promotional price ranges from $14.87 to $111.24, originally priced at $24.99 to $159.99, save up to 41%

Material 3: The commission rate is 20%

Material 4: The link of the product with photo is https://afwjeoi.shop.tiktok.com

Material 5: The link of the sample request is https://mvlownoi.sample.shop.tiktok.com

'''
# dialog -- 对话历史


def main():
    dialog = ""
    js = send_to_influencer(influencer_name, influencer_tags, materials, dialog)
    dialog += bd_header + js["message"] + "\n\n"

    while True:
        reply = input("input the influencer's reply: ")
        if reply == 'exit':
            break

        dialog += inf_header + reply + "\n\n"
        js = send_to_influencer(influencer_name, influencer_tags, materials, dialog)
        dialog += bd_header + js["message"] + "\n\n"


if __name__ == '__main__':
    main()

