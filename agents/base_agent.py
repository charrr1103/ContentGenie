from google.adk.agents import LlmAgent

class BaseAgent(LlmAgent):
    """
    A base class for all custom agents, inheriting from LlmAgent.
    Common configurations like the model and instruction are defined here.
    Subclasses will inherit these and can override the 'name' and 'instruction'
    if needed, but 'model' is usually consistent.
    """
    # Define common model and instruction as class attributes
    # The actual instruction will be set by each subclass's __init__
    # or passed during the Orchestrator's execution.
    # For now, let's keep it simple to fix the Pydantic error.
    # We will remove the explicit instruction in __init__ of sub-agents.

    # LlmAgent expects these as class-level attributes or set via properties
    # Let's define the base model here.
    model: str = "gemini-2.5-pro-preview-05-06"
    instruction: str = "" # This will be overridden by sub-agents

    def __init__(self, name: str, instruction: str, **kwargs):
        # LlmAgent's __init__ will automatically pick up `self.model` and `self.instruction`
        # when it's initialized. So, we only need to pass 'name' and any other
        # LlmAgent specific arguments (like tools if they were added here).
        # However, it seems LlmAgent does not expect 'instruction' in its __init__ if it's
        # already a class attribute. Let's adjust this for the base agent.

        # LlmAgent expects these to be set as class attributes OR passed
        # through its own property setters. The ValidationError means
        # you're trying to pass them as constructor arguments to BaseAgent's super()
        # when Pydantic (which LlmAgent uses) has marked them as 'extra_forbidden' for __init__.

        # The correct way is often to define them at the class level
        # and then initialize BaseAgent/LlmAgent with just the name
        # or other allowed __init__ args.

        # Let's try passing the instruction *after* calling super().__init__
        # if LlmAgent truly doesn't accept it in __init__ for this setup.
        # However, the ADK examples usually show instruction being passed in __init__.
        # The key is that `model` is usually a class attribute.

        super().__init__(name=name, **kwargs)
        self.instruction = instruction # Manually set instruction after super init

        # You might also want to set self.description if it's always used
        if 'description' in kwargs:
            self.description = kwargs['description']