import logging
import re
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
                + "COMBAT: Average enemy health is {avg_enemy_health}. Most enemies require ~{hits_to_kill} hits to kill. Elite enemies often have {elite_health_multiplier} * no of player health. "
                + "Most enemies deal {enemy_damage_range} damage and {enemy_horror_range} horror when they attack. "
                + "INVESTIGATION: Average location clues per investigator is {avg_clues_per_location}. Average shroud value is {avg_shroud}. "
                + "Investigation tests typically need {investigation_target_number} total skill to reliably pass. Each +1 skill icon is worth ~{skill_icon_value} resources. "
                + "CHAOS BAG: Base test success rate is ~{base_success_rate}% for balanced tests. Each +1 skill bonus increases success by ~{skill_bonus_success_rate}%. "
                + "Chaos token mitigation (ignore/redraw) is worth ~{chaos_token_mitigation_value} resources per use. Auto-success effects are worth ~{auto_success_value} resources. "
                + "SURVIVABILITY: Each health/sanity point is worth ~{health_sanity_value} resources. Horror healing is worth ~{horror_heal_value} resources per point. "
                + "Damage healing is worth ~{damage_heal_value} resources per point. Trauma prevention is worth ~{trauma_prevention_value} resources per point avoided. "
                + "RESOURCES: One action is worth ~{action_value} resources. One card is worth ~{card_value} resources, depending on draw engine. "
                + "Each resource gained is worth 1 resource (baseline). Resource acceleration (gaining >1 per action) is worth ~{resource_acceleration_value} per extra resource. "
                + "TIMING: Fast cards save one action (≈{fast_card_value} resources). Reaction effects usually trigger once per round, conditional. "
                + "FACTIONS: Guardian focuses on fighting and protection. Seeker focuses on clue gathering and card draw. "
                + "Rogue focuses on action efficiency and resource generation. Mystic focuses on spell power and willpower tests. "
                + "Survivor focuses on fail-to-win effects and resource-light play. "
                + "CARD TYPES: Assets provide repeatable or passive effects. Events give one-time, powerful effects. "
                + "Charges, secrets, ammo limit how many times an effect can be used. Each turn gives 3 actions, 1 card, 1 resource. "
                + "Clues are worth ~{clue_value} resources each (context-adjusted). Damage dealt or avoided is worth ~{damage_value} resources (context-adjusted). "
                + "Fast and reaction abilities depend on timing but don't cost actions. Exceptional cards have stronger effects but cost more XP. "
                + "Here are edge case: - Only evaluate on special effects if the card have extra effect(like increased test success, encounter avoidance, chaos bag control, token manipulation, healing boosts, etc.) that do not applicable to existing value (actions,damage... etc), "
                + "estimate their approximate resource-equivalent value and include it as a separate entry under key 17 ('special_effect').  - Report 'actions' only if the card directly gives or removes actions. "
                + "Do NOT report 'fast actions' unless the card has the Fast keyword. Only report 'player card draws' when the investigator draws from their own player deck. Only report 'encounter card draw' when drawing from the encounter deck. "
                + "For 'trigger condition', explain the board condition required to play or resolve the card (e.g., 'requires x'). For 'pass condition', explain only if the card includes a skill test or chaos bag check. "
                + "Best-case means the best possible encounter or outcome, but it still counts all card actions (even encounter draws), just with ideal effects. Typical-case means the normal outcome most investigators would get. Worst-case means the outcome if everything goes badly, including harsh encounter effects. "
                + "Step 1. Identify and summarize its **base effects** postive value means gain, negative value means loss 1.actions, 2.player_card_draws, 3.damage, 4.clues, 5.skill_icon, 6.horror, 7.health, 8.uses (charges, ammo, secrets), 9.movement, 10.doom, 11.fast_actions, 12.reactions, 13.exhaust_costs, 14.encounter_card_draw, 15.enemy, 16.XP. 17. special effect. "
                + "Step 2. Describe its **best-case scenario**: maximum value assuming the most favorable conditions. "
                + "Step 3. Describe its **typical-case scenario**: average expected value across normal game states. "
                + "Step 4. Describe its **worse-case scenario**: worst value across game states. Only show value that are not equal to zero. "
                + "return the result in JSON format as: {'name': '...','best_case_quantities': { 'clues': x, 'encounter': y, ...,'context': 'str' },'typical_case_quantities': { ... },'worse_case_quantities': {...},'notes': '...','have_trigger_prob': 'bool','trigger_condition': 'str','have_pass_prob': 'bool','pass_condition': 'str'}"
            ),
        }

    def clean_gpt_json(self, output: str):
        cleaned = re.sub(r"^json\\n", "", output.strip())  # remove leading json\n
        cleaned = re.sub(r"^```json\s*", "", cleaned)  # remove ```json
        cleaned = re.sub(r"```$", "", cleaned)  # remove closing ```
        return cleaned.strip()

    async def async_request(self, request: OpenAIRequest):
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
                            "content": self.clean_gpt_json(
                                choice.message.content or ""
                            ),
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
                    chat_completetion_response.usage.model_dump()
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
