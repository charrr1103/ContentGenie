import asyncio
import json

class MockLLM:
    async def generate_content(self, prompt: str) -> str:
        print(f"\n--- Mock LLM Prompt ---\n{prompt[:500]}...\n")
        await asyncio.sleep(0.5)

        if "AUDIENCE ANALYSIS REPORT" in prompt or "Audience Analyst" in prompt:
            return json.dumps({
                "1. Target Audience Persona Summary": {
                    "Name (Archetype)": "Urban Professional",
                    "Demographics": {
                        "Age Range": "28-45",
                        "Gender Split": "55% Female, 45% Male",
                        "Location (Geographic)": "Major metros (NYC, London, Singapore)",
                        "Income Level/Socioeconomic Status": "Mid to High",
                        "Education Level": "Bachelor’s+",
                        "Occupation/Industry": "Tech, Finance, Consulting"
                    },
                    "Psychographics": {
                        "Interests & Hobbies": "Travel, productivity, fitness",
                        "Values & Beliefs": "Efficiency, innovation",
                        "Lifestyle": "Busy, mobile-first, outcome-oriented",
                        "Personality Traits": "Ambitious, discerning",
                        "Attitudes towards new tech/services": "Open if it saves time"
                    },
                    "Goals & Aspirations": "Time-saving, career growth",
                    "Pain Points & Challenges": "Too busy, digital overload"
                },
                "2. Key Insights & Behaviors": {
                    "Information Sources/Channels": "LinkedIn, Podcasts, Newsletters",
                    "Preferred Communication Styles": "Concise, benefit-driven",
                    "Online Behavior": "Subscribes, skims articles, uses tools",
                    "Buying Behavior/Decision-Making Process": "Reviews ROI, asks peers"
                },
                "3. Language & Tone Recommendations": {
                    "Specific keywords, phrases, or jargon they use": "ROI, productivity, scalable",
                    "Tone": "Professional, efficient, empathetic",
                    "What language to avoid": "Fluff, complexity"
                },
                "4. Content/Marketing Message Themes": {
                    "Core messages that will resonate with them": "Save time, boost results",
                    "Benefits to highlight": "Integration, intuitive UX, automation"
                },
                "5. Gaps in Information/Further Research Needs": "Budgeting preferences",
                "Confidence Score (1-10)": 8
            })
        else:
            return "Generic LLM response."

mock_llm = MockLLM()

async def call_llm_with_prompt(prompt: str) -> str:
    return await mock_llm.generate_content(prompt)
