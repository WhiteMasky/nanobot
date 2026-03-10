"""Tool registry for dynamic tool management."""

import asyncio
from typing import Any

from loguru import logger

from nanobot.agent.tools.base import Tool


class ToolRegistry:
    """
    Registry for agent tools.

    Allows dynamic registration and execution of tools.
    Supports parallel execution of independent tools.
    """

    def __init__(self, max_parallel: int = 5):
        self._tools: dict[str, Tool] = {}
        self._max_parallel = max_parallel
        self._semaphore = asyncio.Semaphore(max_parallel)

    def register(self, tool: Tool) -> None:
        """Register a tool."""
        self._tools[tool.name] = tool
        logger.info("Registered tool: {}", tool.name)

    def unregister(self, name: str) -> None:
        """Unregister a tool by name."""
        self._tools.pop(name, None)
        logger.info("Unregistered tool: {}", name)

    def get(self, name: str) -> Tool | None:
        """Get a tool by name."""
        return self._tools.get(name)

    def has(self, name: str) -> bool:
        """Check if a tool is registered."""
        return name in self._tools

    def get_definitions(self) -> list[dict[str, Any]]:
        """Get all tool definitions in OpenAI format."""
        return [tool.to_schema() for tool in self._tools.values()]

    async def execute(self, name: str, params: dict[str, Any]) -> str:
        """Execute a tool by name with given parameters."""
        _HINT = "\n\n[Analyze the error above and try a different approach.]"

        tool = self._tools.get(name)
        if not tool:
            return f"Error: Tool '{name}' not found. Available: {', '.join(self.tool_names)}"

        try:
            params = tool.cast_params(params)
            errors = tool.validate_params(params)
            if errors:
                return f"Error: Invalid parameters for tool '{name}': " + "; ".join(errors) + _HINT
            result = await tool.execute(**params)
            if isinstance(result, str) and result.startswith("Error"):
                return result + _HINT
            return result
        except Exception as e:
            logger.exception("Tool {} failed: {}", name, e)
            return f"Error executing {name}: {str(e)}" + _HINT

    async def execute_parallel(self, tool_calls: list[dict[str, Any]]) -> list[tuple[str, str]]:
        """
        Execute multiple tools in parallel with concurrency control.
        
        Args:
            tool_calls: List of dicts with 'name' and 'params' keys
            
        Returns:
            List of (tool_name, result) tuples
        """
        async def _execute_with_semaphore(tc: dict[str, Any]) -> tuple[str, str]:
            async with self._semaphore:
                name = tc.get("name", "unknown")
                params = tc.get("params", tc.get("arguments", {}))
                result = await self.execute(name, params)
                return (name, result)
        
        tasks = [_execute_with_semaphore(tc) for tc in tool_calls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        output = []
        for i, result in enumerate(results):
            name = tool_calls[i].get("name", "unknown")
            if isinstance(result, Exception):
                output.append((name, f"Error: {result}"))
            else:
                output.append(result)
        return output

    async def execute_batch(self, tool_calls: list[dict[str, Any]], 
                           stop_on_error: bool = False) -> list[tuple[str, str]]:
        """
        Execute tools sequentially or in parallel based on dependencies.
        
        Args:
            tool_calls: List of tool call dicts
            stop_on_error: If True, stop execution on first error
            
        Returns:
            List of (tool_name, result) tuples
        """
        results = []
        for tc in tool_calls:
            name = tc.get("name", "unknown")
            result = await self.execute(name, tc.get("params", tc.get("arguments", {})))
            results.append((name, result))
            if stop_on_error and result.startswith("Error"):
                break
        return results

    @property
    def tool_names(self) -> list[str]:
        """Get list of registered tool names."""
        return list(self._tools.keys())

    @property
    def tools_count(self) -> int:
        """Get number of registered tools."""
        return len(self._tools)

    def __len__(self) -> int:
        return len(self._tools)

    def __contains__(self, name: str) -> bool:
        return name in self._tools
