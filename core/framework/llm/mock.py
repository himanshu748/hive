"""Mock LLM Provider for testing agents without API calls."""

from typing import Any

from framework.llm.provider import LLMProvider, LLMResponse, Tool


class MockLLMProvider(LLMProvider):
    """
    Mock LLM provider that returns deterministic responses for testing.

    Use this provider when:
    - Running examples without API keys
    - Testing agent graph execution flow
    - Development and debugging
    - CI/CD pipelines

    The mock provider generates contextual responses based on the input,
    allowing agents to execute without actual LLM API calls.

    Example:
        >>> from framework.llm import MockLLMProvider
        >>> llm = MockLLMProvider()
        >>> response = llm.complete([{"role": "user", "content": "Hello"}])
        >>> print(response.content)
        [Mock] Processed request successfully...
    """

    def __init__(
        self,
        model: str = "mock-model",
        default_response: str | None = None,
    ):
        """
        Initialize the mock LLM provider.

        Args:
            model: Model name to report in responses
            default_response: Default response content (optional)
        """
        self.model = model
        self.default_response = default_response
        self._call_count = 0

    def complete(
        self,
        messages: list[dict[str, Any]],
        system: str = "",
        tools: list[Tool] | None = None,
        max_tokens: int = 1024,
        response_format: dict[str, Any] | None = None,
        json_mode: bool = False,
    ) -> LLMResponse:
        """
        Generate a mock completion.

        Returns a deterministic response based on the input messages.
        If json_mode is True, returns a valid JSON structure.
        """
        self._call_count += 1

        # Extract context from the last user message
        last_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_message = str(msg.get("content", ""))
                break

        # Use custom response if provided
        if self.default_response:
            content = self.default_response
        elif json_mode:
            content = '{"status": "success", "mock": true, "message": "Mock response"}'
        else:
            content = self._generate_contextual_response(last_message, system)

        return LLMResponse(
            content=content,
            model=self.model,
            input_tokens=len(str(messages)) // 4,
            output_tokens=len(content) // 4,
            stop_reason="end_turn",
            raw_response={"mock": True, "call_count": self._call_count},
        )

    def complete_with_tools(
        self,
        messages: list[dict[str, Any]],
        system: str,
        tools: list[Tool],
        tool_executor: callable,
        max_iterations: int = 10,
    ) -> LLMResponse:
        """
        Mock tool-use loop.

        In mock mode, returns a response acknowledging the tools without
        actually invoking them.
        """
        self._call_count += 1

        # Extract context
        last_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_message = str(msg.get("content", ""))[:100]
                break

        tool_names = [t.name for t in tools] if tools else []
        content = (
            f"[Mock] Processed with tools: {tool_names}. "
            f"Context: {last_message}..."
        )

        return LLMResponse(
            content=content,
            model=self.model,
            input_tokens=len(str(messages)) // 4,
            output_tokens=len(content) // 4,
            stop_reason="end_turn",
            raw_response={"mock": True, "tools_available": tool_names},
        )

    def _generate_contextual_response(self, user_message: str, system: str) -> str:
        """Generate a contextual mock response based on input."""
        combined = (user_message + system).lower()

        if "search" in combined:
            return (
                "[Mock] Search results: Found 3 relevant sources. "
                "1) Example article, 2) Research paper, 3) Documentation."
            )

        if "summar" in combined:
            return (
                "[Mock] Summary: Key points extracted from the content. "
                "Main findings and conclusions included."
            )

        if "parse" in combined or "extract" in combined:
            return "[Mock] Parsed: topic='example', keywords=['mock', 'test']"

        if "evaluat" in combined or "quality" in combined:
            return "[Mock] Evaluation: Score 85/100. Quality: Good. Status: Approved."

        if "write" in combined or "report" in combined:
            return (
                "[Mock] Report generated with introduction, findings, "
                "and conclusion sections."
            )

        return (
            f"[Mock] Processed request (call #{self._call_count}). "
            "This is a mock response for testing without API calls."
        )

    @property
    def call_count(self) -> int:
        """Return the number of times the provider has been called."""
        return self._call_count

    def reset(self) -> None:
        """Reset the call counter."""
        self._call_count = 0
