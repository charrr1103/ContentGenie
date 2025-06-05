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
            audience = self.agents["audience_analyst"].analyze(product_description)
            strategy = self.agents["content_strategist"].plan(audience, campaign_goal)
            copy = self.agents["copywriter"].generate(strategy)
            formatted = self.agents["formatter"].format(copy)
            reviewed = self.agents["reviewer"].review(formatted)
            calendar = self.agents["scheduler"].schedule(reviewed)
            return calendar
        except Exception as e:
            self.logger.error("Pipeline failed:", e)
            return None
