"""
Pydantic models for OpenAI-compatible requests
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal, Union


class Message(BaseModel):
    """Chat message"""
    role: Literal["system", "user", "assistant", "function", "tool"]
    content: Optional[str] = None
    name: Optional[str] = None
    function_call: Optional[Dict[str, Any]] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None


class FunctionDefinition(BaseModel):
    """Function definition for function calling"""
    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None


class ToolDefinition(BaseModel):
    """Tool definition"""
    type: Literal["function"]
    function: FunctionDefinition


class ChatCompletionRequest(BaseModel):
    """OpenAI chat completion request"""
    
    # Required
    model: str
    messages: List[Message]
    
    # Optional - Generation
    temperature: Optional[float] = Field(default=1.0, ge=0, le=2)
    top_p: Optional[float] = Field(default=1.0, ge=0, le=1)
    n: Optional[int] = Field(default=1, ge=1)
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = Field(default=0, ge=-2, le=2)
    frequency_penalty: Optional[float] = Field(default=0, ge=-2, le=2)
    logit_bias: Optional[Dict[str, float]] = None
    
    # Optional - Function/Tool calling
    functions: Optional[List[FunctionDefinition]] = None
    function_call: Optional[Union[str, Dict[str, str]]] = None
    tools: Optional[List[ToolDefinition]] = None
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None
    
    # Optional - Other
    user: Optional[str] = None  # End-user identifier
    seed: Optional[int] = None
    response_format: Optional[Dict[str, str]] = None
    
    # AgentWall Extensions (not sent to OpenAI)
    agentwall_run_id: Optional[str] = Field(default=None, exclude=True)
    agentwall_agent_id: Optional[str] = Field(default=None, exclude=True)
    agentwall_metadata: Optional[Dict[str, Any]] = Field(default=None, exclude=True)
    
    class Config:
        extra = "allow"  # Allow extra fields (forward compatibility)


class EmbeddingRequest(BaseModel):
    """OpenAI embedding request"""
    
    model: str
    input: Union[str, List[str], List[int], List[List[int]]]
    encoding_format: Optional[Literal["float", "base64"]] = "float"
    user: Optional[str] = None
    
    # AgentWall Extensions
    agentwall_run_id: Optional[str] = Field(default=None, exclude=True)
    
    class Config:
        extra = "allow"
