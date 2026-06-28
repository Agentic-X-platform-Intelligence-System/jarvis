## Epic Summary

Foundation agentic loop with hybrid LLM, Pydantic tool registry, agent loop kernel, Jarvis CLI, and P1 tools.

## Goals

- [ ] Multi-provider LLM layer (Anthropic, OpenAI, Ollama)
- [ ] Hybrid router (local-first with cloud escalation)
- [ ] Pydantic tool framework and P1 tools
- [ ] Jarvis CLI with smoke evals

## Sub-Epics

- E1.1: Multi-provider LLM layer
- E1.2: Hybrid router
- E1.3: Pydantic tool framework
- E1.4: Agent loop kernel
- E1.5: Jarvis CLI (Typer + Rich)
- E1.6: P1 tools (filesystem, shell, Wikipedia, weather)
- E1.7: Smoke tests and evals

## Success Criteria

- [ ] `jarvis "What's the weather in Mumbai?"` uses tool and returns answer
- [ ] `jarvis "Read my README.md"` uses filesystem tool
- [ ] Hybrid router switches to Ollama for simple tasks, Claude for complex
- [ ] Smoke eval suite passes (5 test cases)

## Out of Scope

- LangChain / LangGraph integration
- Sub-project routing (Friday, Edith, etc.)

## Dependencies

- Blocks: E2 (Aura on shared stem)

## Estimated Timeline

2 weeks (Sprints 1–2)

## Portfolio Mapping

**Project:** P1 — Smart CLI + tool use  
**Phase:** 1  
**Sub-project:** stem, jarvis
