import logging
from fastapi import HTTPException
from openai import AsyncOpenAI, OpenAI, RateLimitError
from app.schemas.gpt_schema import OpenAIHeaders, OpenAIRequest, OpenAIResponse
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from typing import List, cast

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GPTService:
    def __init__(self):
        self.client = AsyncOpenAI()
        self.system_messages = {
            "role": "system",
            "content": (
                "You already know all keywords in Arkham Horror. Use the following axioms when analyzing: "
                + "Average enemy health is 3. Average location clues per investigator is 2. "
                + "Most enemies require ~2 hits to kill. Elite enemies often have 5–6 * no of player health. "
                "Most enemies deal 1–2 damage and horror when they attack. "
                + "Guardian focuses on fighting and protection. Seeker focuses on clue gathering and card draw. "
                + "Rogue focuses on action efficiency and resource generation. Mystic focuses on spell power and willpower tests. "
                + "Survivor focuses on fail-to-win effects and resource-light play. Assets provide repeatable or passive effects. "
                + "Events give one-time, powerful effects. Fast cards save one action (≈2 resources). Reaction effects usually trigger once per round, conditional. "
                + "Charges, secrets, ammo limit how many times an effect can be used. One action is worth ~2 resources. "
                + "One card is worth ~1–2 resources, depending on draw engine. Each turn gives 3 actions, 1 card, 1 resource. "
                + "Clues are worth ~2.5 resources each (for seekers). Damage dealt or avoided is worth ~2–2.5 resources (for fighters). Some effects only trigger if the right situation appears. "
                + "Fast and reaction abilities depend on timing but don't cost actions. Exceptional cards have stronger effects but cost more XP. "
                + "Here are edge case: - When evaluating special effects described in card text (like increased test success, extra draws, extra actions, encounter avoidance, chaos bag control, token manipulation, healing boosts, etc.), "
                + "estimate their approximate resource-equivalent value and include it as a separate entry under key 20 ('special_effect').  - Report 'actions' only if the card directly gives or removes actions. "
                + "Do NOT report 'fast actions' unless the card has the Fast keyword. Only report 'player card draws' when the investigator draws from their own player deck. Only report 'encounter card draw' when drawing from the encounter deck. "
                + "For 'trigger condition', explain the board condition required to play or resolve the card (e.g., 'requires x'). For 'pass condition', explain only if the card includes a skill test or chaos bag check. "
                + "Best-case means the best possible encounter or outcome, but it still counts all card actions (even encounter draws), just with ideal effects. Typical-case means the normal outcome most investigators would get. Worst-case means the outcome if everything goes badly, including harsh encounter effects. "
                + "Step 1. Identify and summarize its **base effects** postive value means gain, negative value means loss 1.actions, 2.player card draws, 3.damage, 4.clues, 5.skill_icon, 6.horror, 7.health, 8.uses (charges, ammo, secrets), 9.movement, 10.doom, 11.fast actions, 12.reactions, 13.exhaust costs, 14.blessed tokens, 15.cursed tokens, 16.sealing tokens, 17.encounter card draw, 18.enemy, 19.XP. 20 special effect. "
                + "Step 2. Describe its **best-case scenario**: maximum value assuming the most favorable conditions. "
                + "Step 3. Describe its **typical-case scenario**: average expected value across normal game states. "
                + "Step 4. Describe its **worse-case scenario**: worst value across game states. Only show value that are not euqal to zero. "
                + "return the result in format as: {'name': '...','best_case_quantities': { 'clues': x, 'encounter': y, ...,'context': 'str' },'typical_case_quantities': { ... },'worse_case_quantities': {...},'notes': '...','have_trigger_prob': 'bool','trigger_condition': 'str','have_pass_prob': 'bool','pass_condition': 'str'}"
            ),
        }

    async def async_request(self, request: OpenAIRequest, db):
        try:
            print("async_request")
            # await self.check_gpt_avalibility()
            # session = await self.handle_gpt_user_session(request, db)

            messages = cast(
                List[ChatCompletionMessageParam],
                [
                    ChatCompletionSystemMessageParam(
                        role="system", content=self.system_messages["content"]
                    ),
                    ChatCompletionUserMessageParam(
                        role="user", content=request.content
                    ),
                ],
            )

            legacy_response = await self.client.chat.completions.with_raw_response.create(
                model="gpt-4o-mini",
                messages=messages,
                # max_tokens=1000,
                store=True,
            )
            # legacy_response = (
            #     await asyncClient.chat.completions.with_raw_response.create(
            #         model="gpt-4o-mini",
            #         messages=[
            #             {"role": "user", "content": "Hello"},
            #         ],
            #         max_tokens=5,
            #     )
            # )

            chat_completetion_response = legacy_response.parse()
            response_dict = {
                "id": chat_completetion_response.id,
                "choices": [
                    {
                        "finish_reason": choice.finish_reason,
                        "index": choice.index,
                        "logprobs": choice.logprobs,
                        "message": {
                            "content": choice.message.content,
                            "role": choice.message.role,
                            "refusal": choice.message.refusal,
                            "function_call": choice.message.function_call,
                            "tool_calls": choice.message.tool_calls,
                        },
                    }
                    for choice in chat_completetion_response.choices
                ],
                "created": chat_completetion_response.created,
                "model": chat_completetion_response.model,
                "object": chat_completetion_response.object,
                "service_tier": chat_completetion_response.service_tier,
                "system_fingerprint": chat_completetion_response.system_fingerprint,
                "usage": (
                    chat_completetion_response.usage.dict()
                    if chat_completetion_response.usage
                    else {}
                ),
            }

            print("response xd", response_dict, legacy_response.headers)
            # res_data = await asyncClient.chat.completions.create(
            #     model="gpt-3.5-turbo",
            #     messages=[self.system_messages, {"role": "user", "content": usr_input}],
            #     stream=False,
            #     temperature=0.7,
            #     # max_tokens=1000,
            #     top_p=0.9,
            #     presence_penalty=0,
            #     frequency_penalty=0,
            # )
            # parsed_response = await self.handle_gpt_request(usr_input)
            response = OpenAIResponse.from_dict(response_dict)
            print("openaiResponse", response)
            headers = OpenAIHeaders.from_headers(legacy_response.headers)
            print("headers", headers)
            return response
        except RateLimitError as e:
            logger.error("Rate limit exceeded")
            # await self.post_process(request, None, None, None, 429, str(e))
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            # await self.post_process(request, None, None, None, 500, str(e))
            raise HTTPException(status_code=500, detail=str(e))
