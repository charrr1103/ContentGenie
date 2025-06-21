import os
import re
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict
from agents.base_agent import BaseAgent


class SchedulerAgent(BaseAgent):
    def __init__(self):
        system_prompt = """
You are the 'Scheduler' agent. Your job is to schedule campaign content for publishing.

Instructions:
1. Parse the text input to extract each content item.
2. Focus on the modified "Content Strategy" and modified "Marketing Copy"
3. For each item, extract:
   - Platform (e.g. Instagram, LinkedIn, Facebook, Blog, Email, TikTok, YouTube, Website)
   - Post content
   - Media/Asset name (if present)
   - Design notes (if present)
4. Auto-schedule each item by:
   - Starting from the next working day (Mon–Fri)
   - Follow the posting frequency listed in modified "Content Strategy"
   - Default time: 10:00 AM for Instagram, 2:00 PM for LinkedIn, 4:00 PM for Facebook, 9:00 AM for Email, 6:00 PM for TikTok/YouTube
5. Format the output as a readable schedule, grouped by week.
6. Save both a CSV file and a readable .txt file in the local output directory.

REQUIRED OUTPUT FORMAT:
Week 1 (<24/06/2025 - 28/06/2025>):
Date                 Time     Platform     Content                       Design Notes
Monday (24/06/2025)  10.00am  Instagram    “Sample Caption...”           “Design: Modern, green palette”
*******
Do not remove content or say “pattern continues”.
Print at least 4 weeks explicitly.
*******
"""
        super().__init__(
            name="ContentScheduler",
            instruction=system_prompt,
            description="Parses strategy and copy to auto-generate a publishing calendar."
        )

    def execute(self, raw_text: str) -> str:
        platforms = ["Instagram", "Facebook", "Blog", "TikTok", "YouTube", "Email", "Website", "LinkedIn"]
        post_pattern = re.compile(rf"({'|'.join(platforms)})(?: Post \d+)?:\s*(.*?)(?=\n(?:{'|'.join(platforms)})(?: Post \d+)?:|\Z)", re.DOTALL)
        matches = post_pattern.findall(raw_text)

        content_blocks = []
        for platform, block in matches:
            image_match = re.search(r"Image:\s*(.+)", block)
            video_match = re.search(r"Video:\s*(.+)", block)
            design_match = re.search(r"Design:\s*(.+)", block)
            caption_match = re.search(r"Caption:\s*\"(.*?)\"", block, re.DOTALL)

            if caption_match:
                content = caption_match.group(1).strip()
            else:
                lines = block.strip().splitlines()
                lines = [line for line in lines if not line.strip().lower().startswith(("image:", "video:", "design:"))]
                content = " ".join(lines).strip() if lines else "No caption found"

            media = image_match.group(1) if image_match else video_match.group(1) if video_match else "None"
            design_notes = design_match.group(1).strip() if design_match else "N/A"

            content_blocks.append({
                "platform": platform,
                "content": content,
                "media": media,
                "design_notes": design_notes
            })

        strategy_match = re.search(r'Modified "Content Strategy":(.*?)(?=Marketing Copy:)', raw_text, re.DOTALL)
        frequency_map = self._extract_platform_frequencies(strategy_match.group(1)) if strategy_match else {}

        post_counts = {k: 0 for k in frequency_map}
        filtered_blocks = []
        for item in content_blocks:
            platform = item["platform"]
            if platform not in frequency_map or post_counts[platform] < frequency_map[platform] * 4:
                filtered_blocks.append(item)
                post_counts[platform] += 1

        start_date = self._next_weekday(datetime.today())
        calendar = []
        for i, item in enumerate(filtered_blocks):
            post_date = self._next_weekday(start_date + timedelta(days=i))
            calendar.append({
                "date": post_date.strftime("%d/%m/%Y"),
                "time": self._suggest_time(item['platform']),
                "platform": item['platform'],
                "content": item['content'],
                "design_notes": item['design_notes'],
                "media": item['media']
            })

        # Existing CSV and TXT output (unchanged)
        output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(output_dir, exist_ok=True)
        csv_path = os.path.join(output_dir, "content_schedule.csv")
        txt_path = os.path.join(output_dir, "content_schedule.txt")

        df = pd.DataFrame(calendar)
        df.to_csv(csv_path, index=False)

        # Group posts by week
        from collections import defaultdict

        weeks = defaultdict(list)
        for row in calendar:
            delta = (datetime.strptime(row["date"], "%d/%m/%Y") - start_date).days
            week_num = (delta // 5) + 1
            weeks[week_num].append(row)

        # >>> CHANGE START: generate markdown table output for chat
        markdown_output = []
        for week_num in sorted(weeks.keys()):
            week_posts = weeks[week_num]
            week_start = week_posts[0]["date"]
            week_end = week_posts[-1]["date"]
            markdown_output.append(f"**Week {week_num} ({week_start} - {week_end}):**")
            week_df = pd.DataFrame(week_posts)[["date","time","platform","content","design_notes"]]
            week_df.columns = ["Date","Time","Platform","Content","Design Notes"]
            markdown_output.append(week_df.to_markdown(index=False))
            markdown_output.append("")
        return "\n".join(markdown_output)
        # <<< CHANGE END <<<

    def _extract_platform_frequencies(self, strategy_text: str) -> Dict[str, int]:
        platform_map = {}
        lines = strategy_text.strip().splitlines()
        for line in lines:
            match = re.match(r"(\w+)\s*:\s*(\d+)\s*(?:post|video|article|newsletter)s?/week", line, re.IGNORECASE)
            if match:
                platform = match.group(1).capitalize()
                count = int(match.group(2))
                platform_map[platform] = count
        return platform_map

    def _suggest_time(self, platform: str) -> str:
        platform = platform.lower()
        if "instagram" in platform:
            return "10:00"
        elif "linkedin" in platform:
            return "14:00"
        elif "facebook" in platform:
            return "16:00"
        elif "email" in platform:
            return "09:00"
        elif "tiktok" in platform or "youtube" in platform:
            return "18:00"
        else:
            return "12:00"

    def _next_weekday(self, d: datetime) -> datetime:
        while d.weekday() >= 5:
            d += timedelta(days=1)
        return d

scheduler_agent = SchedulerAgent()
