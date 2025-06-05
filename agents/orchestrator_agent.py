class OrchestratorAgent:
    def __init__(self):
        self.logger = setup_logger()
        self.agents = {
            "audience_analyst": AudienceAnalystAgent(),
            "content_strategist": ContentStrategistAgent(),
            "copywriter": CopywriterAgent(),
            "formatter": FormatterAgent(),
            "reviewer": ReviewerAgent(),
            "scheduler": SchedulerAgent(),
        }

    def run(self, product_description, campaign_goal):
        try:
            self.logger.info("🔍 Step 1: Analyzing audience...")
            audience = self.agents["audience_analyst"].analyze(product_description)

            self.logger.info("🧠 Step 2: Creating content strategy...")
            strategy = self.agents["content_strategist"].plan(audience, campaign_goal)

            self.logger.info("✍️ Step 3: Generating copy...")
            copy = self.agents["copywriter"].generate(strategy)

            self.logger.info("🧼 Step 4: Formatting content...")
            formatted = self.agents["formatter"].format(copy)

            self.logger.info("🔎 Step 5: Reviewing content...")
            reviewed = self.agents["reviewer"].review(formatted)

            self.logger.info("📆 Step 6: Scheduling content...")
            calendar = self.agents["scheduler"].schedule(reviewed)

            self.logger.info("✅ Pipeline complete!")
            return calendar

        except Exception as e:
            self.logger.error("❌ Pipeline failed:", exc_info=True)
            return {"error": str(e)}
