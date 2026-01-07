# JavaScript/TypeScript SDK Guide

Learn how to integrate AgentWall with your JavaScript/TypeScript agent frameworks.

## Installation

```bash
npm install agentwall-sdk
# or
yarn add agentwall-sdk
# or use fetch (built-in)
```

## Basic Usage

### Simple Chat Completion

```javascript
const API_KEY = "aw-your-api-key";
const BASE_URL = "https://api.agentwall.io";

async function chatWithAgentWall(messages, model = "gpt-4o-mini") {
  const response = await fetch(`${BASE_URL}/v1/chat/completions`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model,
      messages,
      temperature: 0.7
    })
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

// Example
const messages = [
  { role: "user", content: "What is 2+2?" }
];

const result = await chatWithAgentWall(messages);
console.log(result.choices[0].message.content);
```

## TypeScript Client

```typescript
interface Message {
  role: "user" | "assistant" | "system";
  content: string;
}

interface ChatResponse {
  choices: Array<{
    message: Message;
    finish_reason: string;
  }>;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

class AgentWallClient {
  private apiKey: string;
  private baseUrl: string;

  constructor(apiKey: string, baseUrl = "https://api.agentwall.io") {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
  }

  private getHeaders(): HeadersInit {
    return {
      "Authorization": `Bearer ${this.apiKey}`,
      "Content-Type": "application/json"
    };
  }

  async chat(
    messages: Message[],
    options?: {
      model?: string;
      temperature?: number;
      runId?: string;
    }
  ): Promise<ChatResponse> {
    const payload: any = {
      model: options?.model || "gpt-4o-mini",
      messages,
      temperature: options?.temperature || 0.7
    };

    if (options?.runId) {
      payload.agentwall_run_id = options.runId;
    }

    const response = await fetch(`${this.baseUrl}/v1/chat/completions`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`API error: ${response.status} - ${error.detail}`);
    }

    return response.json();
  }

  async stream(
    messages: Message[],
    options?: {
      model?: string;
      temperature?: number;
      runId?: string;
      onChunk?: (chunk: string) => void;
    }
  ): Promise<void> {
    const payload: any = {
      model: options?.model || "gpt-4o-mini",
      messages,
      temperature: options?.temperature || 0.7,
      stream: true
    };

    if (options?.runId) {
      payload.agentwall_run_id = options.runId;
    }

    const response = await fetch(`${this.baseUrl}/v1/chat/completions`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const reader = response.body?.getReader();
    if (!reader) throw new Error("No response body");

    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const data = line.slice(6);
          if (data === "[DONE]") continue;

          try {
            const chunk = JSON.parse(data);
            const content = chunk.choices?.[0]?.delta?.content;
            if (content && options?.onChunk) {
              options.onChunk(content);
            }
          } catch (e) {
            // Ignore parse errors
          }
        }
      }
    }
  }
}

export default AgentWallClient;
```

## Run-Level Tracking

Track multi-step agent tasks:

```typescript
import { v4 as uuidv4 } from "uuid";

class AgentWithTracking {
  private client: AgentWallClient;
  private runId: string;

  constructor(apiKey: string) {
    this.client = new AgentWallClient(apiKey);
    this.runId = uuidv4();
  }

  async executeMultiStepTask(initialPrompt: string): Promise<string> {
    const messages: Message[] = [];

    // Step 1: Analyze
    console.log("📊 Step 1: Analyzing...");
    messages.push({ role: "user", content: initialPrompt });

    const step1 = await this.client.chat(messages, {
      runId: this.runId
    });

    const analysis = step1.choices[0].message.content;
    messages.push({ role: "assistant", content: analysis });
    console.log("✅ Analysis complete");

    // Step 2: Generate solution
    console.log("🔧 Step 2: Generating solution...");
    messages.push({
      role: "user",
      content: "Now generate a detailed solution based on your analysis"
    });

    const step2 = await this.client.chat(messages, {
      runId: this.runId
    });

    const solution = step2.choices[0].message.content;
    messages.push({ role: "assistant", content: solution });
    console.log("✅ Solution generated");

    // Step 3: Refine
    console.log("✨ Step 3: Refining...");
    messages.push({
      role: "user",
      content: "Please refine and optimize the solution"
    });

    const step3 = await this.client.chat(messages, {
      runId: this.runId
    });

    const refined = step3.choices[0].message.content;
    console.log("✅ Refinement complete");

    return refined;
  }
}

// Example
const agent = new AgentWithTracking("aw-your-api-key");
const result = await agent.executeMultiStepTask(
  "Analyze this dataset and provide insights: [1,2,3,4,5]"
);
console.log("Final result:", result);
```

## Streaming with React

```typescript
import React, { useState } from "react";
import AgentWallClient from "./AgentWallClient";

export function ChatComponent() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [streaming, setStreaming] = useState("");

  const client = new AgentWallClient("aw-your-api-key");

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages([...messages, userMessage]);
    setInput("");
    setLoading(true);
    setStreaming("");

    try {
      await client.stream([...messages, userMessage], {
        onChunk: (chunk) => {
          setStreaming((prev) => prev + chunk);
        }
      });

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: streaming }
      ]);
      setStreaming("");
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
        {streaming && (
          <div className="message assistant streaming">
            {streaming}
            <span className="cursor">▌</span>
          </div>
        )}
      </div>
      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && handleSend()}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
}
```

## LangChain.js Integration

```typescript
import { ChatOpenAI } from "langchain/chat_models/openai";
import { HumanMessage, SystemMessage } from "langchain/schema";

const chat = new ChatOpenAI({
  openAIApiKey: "aw-your-api-key",
  modelName: "gpt-4o-mini",
  configuration: {
    baseURL: "https://api.agentwall.io/v1"
  }
});

const messages = [
  new SystemMessage("You are a helpful assistant."),
  new HumanMessage("What is 2+2?")
];

const response = await chat.call(messages);
console.log(response.content);
```

## Error Handling

```typescript
async function safeChat(messages: Message[], runId?: string) {
  const client = new AgentWallClient("aw-your-api-key");

  try {
    return await client.chat(messages, { runId });
  } catch (error) {
    if (error instanceof Error) {
      // Handle loop detection
      if (error.message.includes("loop_detected")) {
        console.warn("⚠️ Loop detected! Agent is repeating the same prompt.");
        return null;
      }

      // Handle authentication errors
      if (error.message.includes("401")) {
        console.error("❌ Authentication failed. Check your API key.");
        return null;
      }

      // Handle validation errors
      if (error.message.includes("422")) {
        console.error("❌ Validation error:", error.message);
        return null;
      }

      console.error("❌ Error:", error.message);
    }
    return null;
  }
}
```

## Budget Tracking

```typescript
class BudgetAwareClient {
  private client: AgentWallClient;
  private spent: number = 0;
  private budgetLimit: number;

  constructor(apiKey: string, budgetLimit: number = 10.0) {
    this.client = new AgentWallClient(apiKey);
    this.budgetLimit = budgetLimit;
  }

  async chat(messages: Message[], runId?: string): Promise<ChatResponse | null> {
    try {
      const response = await this.client.chat(messages, { runId });

      // Calculate cost
      const tokens = response.usage.total_tokens;
      const cost = tokens * 0.000001; // Example: $1 per 1M tokens
      this.spent += cost;

      console.log(
        `💰 Cost: $${cost.toFixed(6)} | Total: $${this.spent.toFixed(6)} / $${this.budgetLimit}`
      );

      if (this.spent > this.budgetLimit) {
        console.warn("⚠️ Budget limit exceeded!");
      }

      return response;
    } catch (error) {
      console.error("Error:", error);
      return null;
    }
  }

  getSpent(): number {
    return this.spent;
  }

  getRemainingBudget(): number {
    return Math.max(0, this.budgetLimit - this.spent);
  }
}

// Example
const budgetClient = new BudgetAwareClient("aw-your-api-key", 5.0);
const result = await budgetClient.chat([
  { role: "user", content: "What is AI?" }
]);
console.log(`Remaining budget: $${budgetClient.getRemainingBudget()}`);
```

## Best Practices

1. **Always use run IDs for multi-step tasks** - Enables loop detection and cost tracking
2. **Handle streaming properly** - Use async iterators for better performance
3. **Implement error boundaries** - Catch and handle API errors gracefully
4. **Monitor costs** - Track spending to stay within budget
5. **Use TypeScript** - Better type safety and IDE support
6. **Implement retry logic** - Handle transient failures with exponential backoff

## Troubleshooting

### Loop Detection Blocking Requests

If you see `429 Loop detected` errors:
- Check if you're sending the same prompt repeatedly
- Use different run IDs for different tasks
- Verify your agent logic isn't stuck in a loop

### Streaming Not Working

If streaming responses aren't working:
- Ensure `stream: true` is set in the payload
- Check that your client supports streaming
- Verify the response body is readable

### Authentication Errors

If you see `401 Unauthorized`:
- Verify your API key is correct
- Check the key hasn't been revoked
- Ensure the key is passed in the Authorization header

## Next Steps

- Check out [LangChain Integration](../integrations/langchain.md)
- Read [API Reference](../../api/chat-completions.md)
- Explore [Concepts](../concepts.md)
