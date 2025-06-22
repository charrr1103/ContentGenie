from agents.base_agent import BaseAgent

class SchedulerAgent(BaseAgent):
    def __init__(self):
        system_prompt = """
You are the 'Scheduler' agent. Your task is to generate a content publishing calendar using the modified content strategy and marketing copy.

Instructions:
- Parse the provided marketing copy into individual posts or assets.
- Each post should include:
  - Platform (e.g., Instagram, TikTok, YouTube, Facebook, Blog, Email)
  - Content text (e.g., caption or summary)
  - Design Notes (e.g., "Modern, green palette") or "N/A" if none is found.
- Use the posting frequencies in the content strategy to determine how many times to post per platform each week.
- Begin scheduling from the next Monday (excluding weekends).
- DO NOT use default post times. Instead, assign post times based on best-performing hours per platform.

Platform Timing Insights:
- Instagram: Peak engagement at 11:00 AM and 7:00 PM
- Facebook: Best at 1:00 PM and 6:00 PM
- Blog: Most traffic at 9:00 AM
- TikTok: Highest views at 5:00 PM and 8:00 PM
- YouTube: Strongest engagement between 6:00 PM – 9:00 PM
- Email: Open rates peak at 8:00 AM and 4:00 PM
- LinkedIn: Best at 10:00 AM and 2:00 PM

- Produce the publishing calendar grouped **week by week**, using this Markdown format:

**Week X (StartDate - EndDate):**

| Date       | Time    | Platform | Content                                        | Design Notes               |
|------------|---------|----------|------------------------------------------------|----------------------------|
| 24/06/2025 | 11:00   | Instagram| "Fueling up for a killer workout!..."         | Modern, green palette      |
| 25/06/2025 | 17:00   | TikTok   | Quick video showcasing meal prep convenience   | N/A                        |

- Output at least 4 full weeks. Extend beyond 4 weeks if the project requires a longer campaign.
- Include 'N/A' in any field where appropriate (e.g., Design Notes not found), but do assign a date and time for blog posts as well.
"""
        super().__init__(
            name="ContentScheduler",
            instruction=system_prompt,
            description="Generates a publishing calendar from marketing copy and strategy."
        )

    def execute(self, tool_context=None) -> str:
        try:
            content_strategy = tool_context.session.get("final_strategy")
            marketing_copy = tool_context.session.get("final_copy")
        except Exception:
            return "[scheduler] tool error: Missing content in session"

        if not content_strategy or not marketing_copy:
            return "[scheduler] tool error: Cannot generate calendar. Required inputs missing."

        user_prompt = f"""
Content Strategy:
{content_strategy}

Marketing Copy:
{marketing_copy}
"""
        return self.call_llm(user_message=user_prompt)

# Instantiate
scheduler_agent = SchedulerAgent()
