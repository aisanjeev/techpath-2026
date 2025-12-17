"""Azure OpenAI service for AI-powered features."""
import logging
from typing import List, Optional

from app.core.config import settings
from app.core.exceptions import ExternalServiceError
from app.schemas.ai import ChatMessage, ServiceSuggestion

logger = logging.getLogger(__name__)


class AIService:
    """Service for Azure OpenAI interactions."""

    def __init__(self) -> None:
        self._client = None

    def _get_client(self):
        """Get or create the OpenAI client."""
        if self._client is None:
            if not settings.has_openai_config:
                raise ExternalServiceError(
                    "Azure OpenAI",
                    "Azure OpenAI is not configured. Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY.",
                )

            try:
                from openai import AzureOpenAI

                self._client = AzureOpenAI(
                    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                    api_key=settings.AZURE_OPENAI_KEY,
                    api_version=settings.AZURE_OPENAI_API_VERSION,
                )
            except ImportError:
                raise ExternalServiceError(
                    "Azure OpenAI",
                    "openai package not installed",
                )
            except Exception as e:
                raise ExternalServiceError("Azure OpenAI", str(e))

        return self._client

    async def chat(
        self,
        message: str,
        conversation_history: Optional[List[ChatMessage]] = None,
        context: Optional[str] = None,
        max_tokens: int = 1000,
    ) -> str:
        """
        Send a chat message and get a response.

        Args:
            message: User's message
            conversation_history: Previous messages in the conversation
            context: Additional context about services
            max_tokens: Maximum tokens in response

        Returns:
            AI response text
        """
        try:
            client = self._get_client()

            # Build messages list
            messages = []

            # System message with context
            system_message = (
                "You are a helpful assistant for TechPath, an IT services company "
                "specializing in AI solutions, cloud services, web development, "
                "data analytics, and cybersecurity. Be professional, helpful, and concise."
            )
            if context:
                system_message += f"\n\nAdditional context: {context}"

            messages.append({"role": "system", "content": system_message})

            # Add conversation history
            if conversation_history:
                for msg in conversation_history:
                    messages.append({"role": msg.role, "content": msg.content})

            # Add current message
            messages.append({"role": "user", "content": message})

            # Call Azure OpenAI
            response = client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7,
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error calling Azure OpenAI: {e}")
            raise ExternalServiceError("Azure OpenAI", str(e))

    async def suggest_services(
        self,
        query: str,
        available_services: List[dict],
        industry: Optional[str] = None,
        budget: Optional[str] = None,
        timeline: Optional[str] = None,
    ) -> tuple[List[ServiceSuggestion], str]:
        """
        Get AI-powered service suggestions based on user needs.

        Args:
            query: User's description of their needs
            available_services: List of available services with name, slug, description
            industry: Optional industry context
            budget: Optional budget range
            timeline: Optional project timeline

        Returns:
            Tuple of (list of suggestions, reasoning text)
        """
        try:
            client = self._get_client()

            # Build services context
            services_context = "\n".join(
                f"- {s['name']} ({s['slug']}): {s['description']}"
                for s in available_services
            )

            # Build prompt
            prompt = f"""Based on the user's requirements, suggest the most relevant services from our offerings.

User's Requirements: {query}
"""
            if industry:
                prompt += f"Industry: {industry}\n"
            if budget:
                prompt += f"Budget: {budget}\n"
            if timeline:
                prompt += f"Timeline: {timeline}\n"

            prompt += f"""
Available Services:
{services_context}

Respond in JSON format with:
{{
    "suggestions": [
        {{
            "service_name": "Service Name",
            "service_slug": "service-slug",
            "relevance_score": 0.95,
            "explanation": "Why this service is relevant"
        }}
    ],
    "reasoning": "Overall analysis of the user's needs and recommendations"
}}

Return up to 3 most relevant services, ordered by relevance."""

            response = client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a service recommendation assistant. Always respond with valid JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,
                temperature=0.3,
            )

            # Parse response
            import json

            response_text = response.choices[0].message.content
            # Try to extract JSON from response
            try:
                # Handle potential markdown code blocks
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0]

                result = json.loads(response_text.strip())

                suggestions = [
                    ServiceSuggestion(
                        service_name=s["service_name"],
                        service_slug=s["service_slug"],
                        relevance_score=s.get("relevance_score", 0.8),
                        explanation=s["explanation"],
                    )
                    for s in result.get("suggestions", [])
                ]

                return suggestions, result.get("reasoning", "")

            except json.JSONDecodeError:
                logger.warning("Failed to parse AI response as JSON")
                return [], response_text

        except Exception as e:
            logger.error(f"Error getting service suggestions: {e}")
            raise ExternalServiceError("Azure OpenAI", str(e))


# Global AI service instance
ai_service = AIService()

