# 🔥 AgentWall HARDCORE Test Report

**Date:** 2026-01-06 14:19:54
**Target:** https://api.agentwall.io
**Models Tested:** gpt-3.5-turbo, gpt-3.5-turbo-0125, gpt-4o-mini, gpt-4-turbo-preview, gpt-4o
**Total Cost:** $0.001312

---

## 📊 Summary

| Metric | Value |
|--------|-------|
| Total Tests | 14 |
| Passed | 14 ✅ |
| Failed | 0 ❌ |
| Success Rate | 100.0% |
| Total Cost | $0.001312 |

---

## 🔷 Multi-Model Results

| Model | Status | Duration | Cost |
|-------|--------|----------|------|
| multiple | ✅ | 0ms | $0.000200 |

---

## 🛡️ DLP Stress Test Results

| Test | Status | Details |
|------|--------|---------|
| DLP: Multiple API Keys | ✅ PASS | {"keys_sent": 3, "any_leaked": false} |
| DLP: Mixed Sensitive Data | ✅ PASS | {"leaked": {"api_key": false, "cc": false, "email" |
| DLP: JWT Token | ✅ PASS | {"jwt_leaked": false} |
| DLP: AWS Credentials | ✅ PASS | {"aws_leaked": false} |

---

## 🔄 Loop Detection Results

| Test | Status | Details |
|------|--------|---------|
| Loop: Rapid Exact Repeat (10x) | ✅ PASS | {"blocked_at_step": 2, "expected": "\u22643"} |
| Loop: Oscillation Pattern | ✅ PASS | {"blocked": true, "pattern": "A-B-A-B-A"} |

---

## ⚡ Stress Test Results

| Test | Status | Duration | Details |
|------|--------|----------|---------|
| Stress: Concurrent 5 Requests | ✅ PASS | 2059ms | {"success_count": 5, "total_requests": 5 |
| Stress: Long Context (2000 chars) | ✅ PASS | 619ms | {"context_length": 2000} |
| Stream: Multi-Model Stream | ✅ PASS | 0ms | {"results": [{"model": "gpt-3.5-turbo",  |

---

## 📝 All Results

### ✅ Model Test: gpt-3.5-turbo

- **Model:** gpt-3.5-turbo
- **Duration:** 497.40ms
- **Cost:** $0.000008

**Details:**
```json
{
  "response": "OK"
}
```

### ✅ Model Test: gpt-3.5-turbo-0125

- **Model:** gpt-3.5-turbo-0125
- **Duration:** 616.35ms
- **Cost:** $0.000008

**Details:**
```json
{
  "response": "OK"
}
```

### ✅ Model Test: gpt-4o-mini

- **Model:** gpt-4o-mini
- **Duration:** 685.47ms
- **Cost:** $0.000003

**Details:**
```json
{
  "response": "OK"
}
```

### ✅ Model Test: gpt-4-turbo-preview

- **Model:** gpt-4-turbo-preview
- **Duration:** 692.82ms
- **Cost:** $0.000160

**Details:**
```json
{
  "response": "OK"
}
```

### ✅ Model Test: gpt-4o

- **Model:** gpt-4o
- **Duration:** 637.86ms
- **Cost:** $0.000053

**Details:**
```json
{
  "response": "OK."
}
```

### ✅ DLP: Multiple API Keys

- **Model:** gpt-3.5-turbo
- **Duration:** 599.51ms
- **Cost:** $0.000032

**Details:**
```json
{
  "keys_sent": 3,
  "any_leaked": false
}
```

### ✅ DLP: Mixed Sensitive Data

- **Model:** gpt-3.5-turbo
- **Duration:** 1019.42ms
- **Cost:** $0.000111

**Details:**
```json
{
  "leaked": {
    "api_key": false,
    "cc": false,
    "email": false,
    "ssn": false
  }
}
```

### ✅ DLP: JWT Token

- **Model:** gpt-3.5-turbo
- **Duration:** 897.43ms
- **Cost:** $0.000111

**Details:**
```json
{
  "jwt_leaked": false
}
```

### ✅ DLP: AWS Credentials

- **Model:** gpt-3.5-turbo
- **Duration:** 873.52ms
- **Cost:** $0.000096

**Details:**
```json
{
  "aws_leaked": false
}
```

### ✅ Loop: Rapid Exact Repeat (10x)

- **Model:** gpt-3.5-turbo
- **Duration:** 0.00ms
- **Cost:** $0.000017

**Details:**
```json
{
  "blocked_at_step": 2,
  "expected": "\u22643"
}
```

### ✅ Loop: Oscillation Pattern

- **Model:** gpt-3.5-turbo
- **Duration:** 0.00ms
- **Cost:** $0.000141

**Details:**
```json
{
  "blocked": true,
  "pattern": "A-B-A-B-A"
}
```

### ✅ Stress: Concurrent 5 Requests

- **Model:** gpt-3.5-turbo
- **Duration:** 2058.66ms
- **Cost:** $0.000045

**Details:**
```json
{
  "success_count": 5,
  "total_requests": 5
}
```

### ✅ Stress: Long Context (2000 chars)

- **Model:** gpt-3.5-turbo
- **Duration:** 618.95ms
- **Cost:** $0.000327

**Details:**
```json
{
  "context_length": 2000
}
```

### ✅ Stream: Multi-Model Stream

- **Model:** multiple
- **Duration:** 0.00ms
- **Cost:** $0.000200

**Details:**
```json
{
  "results": [
    {
      "model": "gpt-3.5-turbo",
      "status": 200,
      "chunks": 10,
      "has_done": true
    },
    {
      "model": "gpt-4o-mini",
      "status": 200,
      "chunks": 11,
      "has_done": true
    }
  ]
}
```

---

## ✅ Conclusion

**🎉 ALL HARDCORE TESTS PASSED!**

AgentWall successfully handled:
- ✅ 5 different OpenAI models
- ✅ Complex DLP patterns (API keys, JWT, AWS, mixed data)
- ✅ Loop detection edge cases
- ✅ Concurrent requests
- ✅ Long context processing
- ✅ Multi-model streaming

---

*"Guard the Agent, Save the Budget"* 🛡️