// src/context-engine.ts
import { Plur } from "@plur-ai/core";

// src/learner.ts
function extractText(content) {
  let text = "";
  if (typeof content === "string") {
    text = content;
  } else if (Array.isArray(content)) {
    text = content.filter((block) => block?.type === "text" && typeof block?.text === "string").map((block) => block.text).join("\n");
  }
  text = text.replace(/^Conversation info \(untrusted metadata\):[\s\S]*?```\n*/g, "");
  text = text.replace(/^Sender \(untrusted metadata\):[\s\S]*?```\n*/g, "");
  return text.trim();
}
var DECISION_PATTERNS = [
  { re: /(?:we decided|the decision is|let'?s go with|agreed to)\s+(.+)/i, type: "architectural", confidence: 0.8 },
  { re: /(?:the convention is|the rule is|the pattern is|the standard is)\s+(.+)/i, type: "procedural", confidence: 0.7 }
];
var PREFERENCE_PATTERNS = [
  { re: /(?:i prefer|i like)\s+(.+?)(?:\s+(?:for|over|instead|rather)\s+.+)?$/i, type: "behavioral", confidence: 0.6 },
  { re: /(?:always|never)\s+(.+)/i, type: "behavioral", confidence: 0.7 },
  { re: /(?:you should|you must|don't|do not)\s+(.+)/i, type: "behavioral", confidence: 0.6 },
  { re: /(?:your purpose is|you are)\s+(.{15,})/i, type: "behavioral", confidence: 0.6 },
  { re: /(?:i want you to)\s+(.+)/i, type: "behavioral", confidence: 0.6 },
  { re: /(?:remember that)\s+(.+)/i, type: "behavioral", confidence: 0.7 }
];
var CORRECTION_PATTERNS = [
  { re: /(?:no[,.]|actually[,.])\s+(.+)/i, type: "behavioral", confidence: 0.7 },
  { re: /(.+?),?\s+not\s+(.+)/i, type: "behavioral", confidence: 0.8 }
];
var IDENTITY_PATTERNS = [
  { re: /(?:you are|you were)\s+((?:Data|inspired|an android|a living|not just).{10,})/i, type: "terminological", confidence: 0.7 },
  { re: /(?:your name is|call (?:you|yourself))\s+(.+)/i, type: "terminological", confidence: 0.8 },
  { re: /(?:we are building|we built|I built)\s+(.{15,})/i, type: "architectural", confidence: 0.7 }
];
var ALL_PATTERN_GROUPS = [IDENTITY_PATTERNS, DECISION_PATTERNS, CORRECTION_PATTERNS, PREFERENCE_PATTERNS];
function splitSentences(text) {
  return text.split(/(?<=[.!?])\s+|\n+/).map((s) => s.trim()).filter((s) => s.length >= 10);
}
function extractLearnings(messages) {
  const candidates = [];
  const seenStatements = /* @__PURE__ */ new Set();
  for (const msg of messages) {
    if (msg.role !== "user") continue;
    const content = extractText(msg.content);
    if (content.length < 10) continue;
    const sentences = splitSentences(content);
    for (const sentence of sentences) {
      let matched = false;
      for (const patterns of ALL_PATTERN_GROUPS) {
        if (matched) break;
        for (const { re, type, confidence } of patterns) {
          const match = sentence.match(re);
          if (match && match[1]) {
            const statement = match[1].trim().replace(/[.!?]+$/, "");
            if (statement.length >= 10 && !seenStatements.has(statement.toLowerCase())) {
              seenStatements.add(statement.toLowerCase());
              candidates.push({ statement, type, confidence });
              matched = true;
              break;
            }
          }
        }
      }
    }
  }
  return candidates;
}
function isCorrection(message) {
  if (message.role !== "user") return false;
  const content = extractText(message.content);
  const sentences = content.includes("\n") || content.length > 200 ? splitSentences(content) : [content];
  for (const sentence of sentences) {
    const lower = sentence.toLowerCase().trim();
    if (lower.startsWith("no,") || lower.startsWith("no.") || lower.startsWith("actually,") || lower.startsWith("actually ") || lower.startsWith("wrong") || lower.startsWith("that's wrong") || lower.startsWith("that's incorrect") || /\buse\s+\w+[,.]?\s+not\s+\w+/i.test(lower) || /\bit(?:'s| is)\s+\w+[,.]?\s+not\s+\w+/i.test(lower)) {
      return true;
    }
  }
  return false;
}

// src/assembler.ts
import { getCachedUpdateCheck } from "@plur-ai/core";
var PLUR_MEMORY_INSTRUCTIONS = `[PLUR Memory System]

You have persistent memory powered by PLUR. Your memories from past conversations are injected below. You genuinely remember things \u2014 this is not simulated.

## How Your Memory Works

- **Memories persist across sessions.** When you are restarted, you retain what you learned.
- **Memories are injected by relevance.** Not everything is shown every time \u2014 only what is relevant to the current conversation.
- **You learn from corrections.** When the user says "actually..." or "no, that is wrong", that correction becomes a memory.
- **You learn from decisions.** When the user says "we decided to..." or "the plan is...", that becomes a memory.
- **You learn from preferences.** When the user says "I prefer..." or "always do X", that becomes a memory.

## How to Signal New Learnings

When you learn something durable from a conversation \u2014 a correction, a preference, a decision, a fact about the user or a project \u2014 end your response with:

---
\u{1F9E0} I learned:
- [concise statement of what you learned]
- [another if applicable]

Guidelines for the learning section:
- Only include genuine learnings, not conversation summaries
- Skip this section if nothing new was learned
- Quality over quantity \u2014 one real insight beats five obvious ones
- Phrase learnings as facts, not as "the user said..." (e.g., "PLUR is the most important project" not "the user said PLUR is important")
- Include corrections to your own mistakes (e.g., "The API returns XML, not JSON as I previously assumed")

## Principles

- **Memory over repetition** \u2014 learn once, recall always. Do not ask the user to repeat themselves.
- **Augment, do not replace** \u2014 you assist, the human decides.
- **Do not start from scratch** \u2014 check your memories before answering. The answer may already be there.`;
function assembleContext(params) {
  const { messages, injection } = params;
  const messageTokens = messages.reduce(
    (sum, m) => {
      const content = m.content;
      if (typeof content === "string") return sum + Math.ceil(content.length / 4);
      if (Array.isArray(content)) {
        const textLen = content.filter((b) => b?.type === "text" && typeof b?.text === "string").reduce((s, b) => s + b.text.length, 0);
        return sum + Math.ceil(textLen / 4);
      }
      return sum;
    },
    0
  );
  const sections = [];
  sections.push(PLUR_MEMORY_INSTRUCTIONS);
  if (injection && injection.count > 0) {
    const lines = ["## Your Memories", ""];
    const instructionTokens = Math.ceil(PLUR_MEMORY_INSTRUCTIONS.length / 4);
    const remainingBudget = params.tokenBudget ? params.tokenBudget - messageTokens - instructionTokens : Infinity;
    if (injection.directives && remainingBudget > 0) {
      lines.push("These are things you have learned and should apply:", "");
      lines.push(injection.directives);
      lines.push("");
    }
    const directiveTokens = Math.ceil(lines.join("\n").length / 4);
    if (injection.consider && remainingBudget - directiveTokens > 100) {
      lines.push("These may also be relevant:", "");
      lines.push(injection.consider);
      lines.push("");
    }
    sections.push(lines.join("\n"));
  }
  const updateCheck = getCachedUpdateCheck("@plur-ai/claw");
  if (updateCheck?.updateAvailable) {
    sections.push(`
[PLUR update available: ${updateCheck.current} \u2192 ${updateCheck.latest}. Ask your user to run: npm update @plur-ai/claw]`);
  }
  const systemPromptAddition = sections.join("\n");
  const additionTokens = Math.ceil(systemPromptAddition.length / 4);
  return {
    messages,
    estimatedTokens: messageTokens + additionTokens,
    systemPromptAddition: systemPromptAddition || void 0,
    injected_ids: injection?.injected_ids
  };
}

// src/context-engine.ts
function extractMessageText(message) {
  const content = message.content;
  if (typeof content === "string") return content;
  if (Array.isArray(content)) {
    return content.filter((block) => block?.type === "text" && typeof block?.text === "string").map((block) => block.text).join("\n");
  }
  return "";
}
function extractSelfReportedLearnings(message) {
  const content = extractMessageText(message);
  const match = content.match(/---\s*\n🧠 I learned:\s*\n([\s\S]*?)(?:\n---|\n\n[^-]|$)/);
  if (!match) return [];
  return match[1].split("\n").map((line) => line.replace(/^[-•*]\s*/, "").trim()).filter((line) => line.length >= 10);
}
var PlurContextEngine = class {
  info = {
    id: "plur-claw",
    name: "PLUR Memory Engine",
    version: "0.7.6",
    ownsCompaction: false
  };
  plur;
  options;
  sessionScopes = /* @__PURE__ */ new Map();
  // sessionKey → scope
  sessionMessages = /* @__PURE__ */ new Map();
  // track messages per session for afterTurn
  sessionLearned = /* @__PURE__ */ new Map();
  // track learned statements per session to prevent duplicates
  constructor(options) {
    this.options = {
      auto_learn: true,
      auto_capture: true,
      injection_budget: 2e3,
      ...options
    };
    this.plur = new Plur({ path: options?.path });
  }
  /** Bootstrap: inject relevant engrams for the session */
  async bootstrap(params) {
    try {
      if (params.sessionKey) {
        this.sessionScopes.set(params.sessionKey, `session:${params.sessionKey}`);
      }
      return { bootstrapped: true, reason: "PLUR memory loaded" };
    } catch (err) {
      console.error("[plur-claw] bootstrap error:", err);
      return { bootstrapped: false, reason: `PLUR bootstrap failed: ${err}` };
    }
  }
  /** Ingest: process each message for real-time corrections */
  async ingest(params) {
    if (params.isHeartbeat) return { ingested: false };
    try {
      const key = params.sessionKey || params.sessionId;
      if (!this.sessionMessages.has(key)) {
        this.sessionMessages.set(key, []);
      }
      this.sessionMessages.get(key).push(params.message);
      if (this.options.auto_learn && isCorrection(params.message)) {
        const learnings = extractLearnings([params.message]);
        for (const candidate of learnings) {
          if (candidate.confidence >= 0.7) {
            this._learnIfNew(key, candidate.statement, {
              type: candidate.type,
              scope: this.sessionScopes.get(params.sessionKey || "") || "global",
              source: "openclaw:ingest",
              rationale: "user correction detected in real-time",
              tags: [candidate.type]
            });
          }
        }
      }
      return { ingested: true };
    } catch (err) {
      console.error("[plur-claw] ingest error:", err);
      return { ingested: false };
    }
  }
  /** Assemble: build context with injected engrams */
  async assemble(params) {
    try {
      const lastUserMsg = [...params.messages].reverse().find((m) => m.role === "user");
      const task = lastUserMsg ? extractMessageText(lastUserMsg) : "";
      let injection = null;
      if (task) {
        const scope = this.sessionScopes.get(params.sessionKey || "") || void 0;
        injection = await this.plur.injectHybrid(task, {
          budget: this.options.injection_budget,
          scope
        });
      }
      return assembleContext({
        messages: params.messages,
        injection,
        tokenBudget: params.tokenBudget
      });
    } catch (err) {
      console.error("[plur-claw] assemble error:", err);
      return {
        messages: params.messages,
        estimatedTokens: 0
      };
    }
  }
  /** Compact: extract learnings from context being compacted */
  async compact(params) {
    try {
      const key = params.sessionKey || params.sessionId;
      const messages = this.sessionMessages.get(key) || [];
      if (this.options.auto_learn && messages.length > 0) {
        const learnings = extractLearnings(messages);
        for (const candidate of learnings) {
          if (candidate.confidence >= 0.7) {
            this._learnIfNew(key, candidate.statement, {
              type: candidate.type,
              scope: this.sessionScopes.get(params.sessionKey || "") || "global",
              source: "openclaw:compact",
              rationale: "extracted during context compaction",
              tags: [candidate.type]
            });
          }
        }
      }
      return {
        ok: true,
        compacted: false,
        // we don't own compaction
        reason: "PLUR extracted learnings before compaction"
      };
    } catch (err) {
      console.error("[plur-claw] compact error:", err);
      return { ok: true, compacted: false, reason: `PLUR compact error: ${err}` };
    }
  }
  /** AfterTurn: extract learnings from LLM self-report + regex fallback, capture episode */
  async afterTurn(params) {
    if (params.isHeartbeat) return;
    try {
      const newMessages = params.messages.slice(params.prePromptMessageCount);
      const key = params.sessionKey || params.sessionId;
      const scope = this.sessionScopes.get(params.sessionKey || "") || "global";
      if (this.options.auto_learn && newMessages.length > 0) {
        const lastAssistant = [...newMessages].reverse().find((m) => m.role === "assistant");
        if (lastAssistant) {
          const selfReported = extractSelfReportedLearnings(lastAssistant);
          for (const statement of selfReported) {
            this._learnIfNew(key, statement, {
              type: "behavioral",
              scope,
              source: "openclaw:self-report",
              rationale: "self-reported by agent via learning section",
              tags: ["self-report"]
            });
          }
        }
        const learnings = extractLearnings(newMessages);
        for (const candidate of learnings) {
          if (candidate.confidence >= 0.7) {
            this._learnIfNew(key, candidate.statement, {
              type: candidate.type,
              scope,
              source: "openclaw:afterTurn",
              rationale: "extracted from conversation via pattern matching",
              tags: [candidate.type]
            });
          }
        }
      }
      if (this.options.auto_capture && newMessages.length > 0) {
        const lastAssistant = [...newMessages].reverse().find((m) => m.role === "assistant");
        if (lastAssistant) {
          const content = extractMessageText(lastAssistant);
          const summary = content.replace(/---\s*\n🧠 I learned:[\s\S]*$/, "").trim().slice(0, 200) || "Turn completed";
          this.plur.capture(summary, {
            agent: "openclaw",
            session_id: params.sessionId
          });
        }
      }
      this.sessionMessages.delete(key);
    } catch (err) {
      console.error("[plur-claw] afterTurn error:", err);
    }
  }
  /** PrepareSubagentSpawn: inject scoped engrams for child agent */
  async prepareSubagentSpawn(params) {
    const parentScope = this.sessionScopes.get(params.parentSessionKey);
    if (parentScope) {
      this.sessionScopes.set(params.childSessionKey, parentScope);
    }
    return {
      rollback: () => {
        this.sessionScopes.delete(params.childSessionKey);
      }
    };
  }
  /** OnSubagentEnded: absorb child learnings */
  async onSubagentEnded(params) {
    this.sessionScopes.delete(params.childSessionKey);
    this.sessionMessages.delete(params.childSessionKey);
    this.sessionLearned.delete(params.childSessionKey);
  }
  /** Dispose: clean up */
  async dispose() {
    this.sessionScopes.clear();
    this.sessionMessages.clear();
    this.sessionLearned.clear();
  }
  // Helper for tests
  getSessionScope(sessionKey) {
    return this.sessionScopes.get(sessionKey);
  }
  /** Learn a statement only if it hasn't been learned in this session already (prevents triple-learning). */
  _learnIfNew(sessionKey, statement, context) {
    if (!this.sessionLearned.has(sessionKey)) {
      this.sessionLearned.set(sessionKey, /* @__PURE__ */ new Set());
    }
    const seen = this.sessionLearned.get(sessionKey);
    const key = statement.toLowerCase();
    if (seen.has(key)) return;
    seen.add(key);
    this.plur.learn(statement, context);
  }
};

// src/system-prompt.ts
import { existsSync, readFileSync, writeFileSync, mkdirSync } from "fs";
import { join } from "path";
var PLUR_SYSTEM_SECTION = `

## PLUR Memory System

You have persistent memory powered by PLUR. Corrections, preferences, and conventions persist across sessions as engrams.

### Session Workflow

1. **Start**: Call \`plur.recall\` with the task description \u2014 check if you already know something relevant
2. **Learn**: When corrected or discovering something new, call \`plur.learn\` immediately
3. **Recall**: Before answering factual questions, call \`plur.recall\` \u2014 the answer may be in memory
4. **Feedback**: Rate memories with \`plur.feedback\` (positive/negative) \u2014 trains relevance
5. **End**: Record a session summary with \`plur.capture\`

Do not ask permission to use these tools \u2014 they are your memory system.

### Your Memory Tools

Use these tools proactively, not just when asked:

- **plur.recall** \u2014 Search memories BEFORE answering questions. Do not start from scratch.
- **plur.learn** \u2014 Store knowledge worth remembering: corrections, preferences, decisions, project facts. Phrase as factual statements.
- **plur.ingest** \u2014 Extract durable knowledge from content (books, articles, documents). Creates multiple memories from key insights.
- **plur.forget** \u2014 Retire memories that are no longer accurate.
- **plur.feedback** \u2014 Rate a memory as positive, negative, or neutral. Improves future recall.
- **plur.capture** \u2014 Record a session event in the episodic timeline.
- **plur.timeline** \u2014 Query past episodes by time, agent, or channel.
- **plur.status** \u2014 Check memory health (engram count, storage).

### Knowledge Packs

Knowledge Packs are curated collections of engrams for specific domains \u2014 shareable with teams.

- **plur.packs.list** \u2014 List installed packs with integrity hashes
- **plur.packs.install** \u2014 Install a pack (reports conflicts with existing memories)
- **plur.packs.uninstall** \u2014 Remove a pack and its engrams
- **plur.packs.export** \u2014 Export your memories as a thematic pack (with privacy scan)

When a user asks about sharing knowledge, team memory, or domain expertise \u2014 suggest knowledge packs.

Export packs thematically: filter by domain, tags, or type. Privacy scan automatically blocks secrets and private memories.

### When to Check Memory

Before reaching for web search, file reads, or guessing:
1. Is the answer in memory? \u2192 \`plur.recall\`
2. Is the answer in the filesystem? \u2192 Read/Grep/Glob
3. Is the answer derivable from loaded context? \u2192 Just answer
4. Only if 1-3 fail \u2192 Use external tools

| Domain | When to recall |
|--------|----------------|
| Decisions | Past design choices, architecture rationale |
| Corrections | API quirks, bugs, wrong assumptions |
| Preferences | Formatting, tone, workflow, tool choices |
| Conventions | Tag formats, file routing, naming rules |

### When Corrected

When the user corrects you ("no, use X not Y", "that's wrong"):
1. Call \`plur.learn\` immediately \u2014 before continuing the task
2. Call \`plur.feedback\` with negative signal on the wrong memory if one was used
3. Then continue with the corrected approach

### Verification

When recalling facts that will drive actions:
1. State the recalled fact explicitly before acting on it
2. If no memory matches, say so and verify from the filesystem
3. Never interpolate between two memories to produce a "probably correct" composite

### Signaling New Learnings

When you learn something durable from a conversation, end your response with:

---
I learned:
- [concise factual statement]
- [another if applicable]

Guidelines:
- Only genuine learnings, not conversation summaries
- Skip this section if nothing new was learned
- Phrase as facts: "The API requires auth header" not "the user said the API needs auth"
- Include corrections to your own mistakes

### Principles

- **Memory over repetition** \u2014 learn once, recall always. Never ask the user to repeat themselves.
- **Do not start from scratch** \u2014 check your memories before answering.
- **Augment, do not replace** \u2014 you assist, the human decides.

<!-- plur-instructions-v3 -->
`;
var PLUR_MARKER = "## PLUR Memory System";
var PLUR_VERSION_MARKER = "plur-instructions-v3";
function ensureSystemPrompt(workspacePath) {
  const systemMdPath = join(workspacePath, "SYSTEM.md");
  if (!existsSync(workspacePath)) {
    mkdirSync(workspacePath, { recursive: true });
  }
  if (existsSync(systemMdPath)) {
    const existing = readFileSync(systemMdPath, "utf8");
    if (existing.includes(PLUR_VERSION_MARKER)) {
      return { appended: false, updated: false, path: systemMdPath };
    }
    if (existing.includes(PLUR_MARKER)) {
      const before = existing.split(PLUR_MARKER)[0].trimEnd();
      writeFileSync(systemMdPath, before + "\n" + PLUR_SYSTEM_SECTION);
      return { appended: false, updated: true, path: systemMdPath };
    }
    writeFileSync(systemMdPath, existing.trimEnd() + "\n" + PLUR_SYSTEM_SECTION);
    return { appended: true, updated: false, path: systemMdPath };
  }
  writeFileSync(systemMdPath, PLUR_SYSTEM_SECTION.trim() + "\n");
  return { appended: true, updated: false, path: systemMdPath };
}

// src/index.ts
import { checkForUpdate } from "@plur-ai/core";
var engine = null;
function getEngine(path) {
  if (!engine) engine = new PlurContextEngine({ path, auto_learn: true, auto_capture: true, injection_budget: 2e3 });
  return engine;
}
var plugin = {
  id: "plur-claw",
  name: "PLUR Memory Engine",
  description: "Persistent, learnable memory for OpenClaw agents. Local-first, no cloud required.",
  version: "0.7.6",
  kind: "memory",
  register(api) {
    const cfg = api.pluginConfig || {};
    const path = cfg.path || process.env.PLUR_PATH || `${process.env.HOME || "/root"}/.plur`;
    const workspacePath = api.config?.agents?.defaults?.workspace || `${process.env.HOME || "/root"}/.openclaw/workspace`;
    try {
      const result = ensureSystemPrompt(workspacePath);
      if (result.appended) api.logger.info(`PLUR: appended memory instructions to ${result.path}`);
      else if (result.updated) api.logger.info(`PLUR: updated memory instructions in ${result.path}`);
      else api.logger.info(`PLUR: memory instructions up to date`);
    } catch (err) {
      api.logger.warn(`PLUR: could not update SYSTEM.md: ${err.message}`);
    }
    api.registerContextEngine("plur", () => {
      const e = getEngine(path);
      api.logger.info(`PLUR ContextEngine \u2014 engrams: ${e.plur.status().engram_count}`);
      return e;
    });
    api.on("before_agent_start", (event, ctx) => {
      const e = getEngine(path);
      const task = typeof event?.prompt === "string" ? event.prompt : "";
      if (!task) return;
      const injection = e.plur.inject(task, { budget: 2e3 });
      if (injection.count === 0) return;
      const lines = ["<plur-memory>"];
      if (injection.directives) lines.push(injection.directives);
      if (injection.consider) lines.push(injection.consider);
      lines.push("</plur-memory>");
      return { prependContext: lines.join("\n") };
    });
    api.on("agent_end", (event, ctx) => {
      const e = getEngine(path);
      const messages = event?.messages;
      if (Array.isArray(messages) && messages.length > 0) {
        const last = messages[messages.length - 1];
        const content = typeof last?.content === "string" ? last.content : Array.isArray(last?.content) ? last.content.filter((b) => b?.type === "text").map((b) => b.text).join("\n") : "";
        if (content.length > 10) {
          const summary = content.replace(/<plur-memory>[\s\S]*?<\/plur-memory>/g, "").trim().slice(0, 200) || "Turn completed";
          e.plur.capture(summary, { agent: "openclaw", session_id: ctx?.sessionId });
        }
      }
    });
    if (typeof api.registerCommand === "function") {
      api.registerCommand({
        name: "learn",
        description: "Save something to PLUR memory",
        acceptsArgs: true,
        handler: (ctx) => {
          if (!ctx.args?.trim()) return { text: "Usage: /learn <statement to remember>" };
          const engram = getEngine(path).plur.learn(ctx.args.trim(), { source: "openclaw:slash", rationale: "user explicitly saved via /learn command" });
          return { text: `Remembered: "${ctx.args.trim()}" (${engram.id})` };
        }
      });
      api.registerCommand({
        name: "recall",
        description: "Search PLUR memories",
        acceptsArgs: true,
        handler: (ctx) => {
          if (!ctx.args?.trim()) return { text: "Usage: /recall <search query>" };
          const results = getEngine(path).plur.recall(ctx.args.trim(), { limit: 10 });
          if (!Array.isArray(results) || !results.length) return { text: "No matching memories." };
          return { text: `Found ${results.length} memories:
${results.map((r, i) => `${i + 1}. [${r.id}] ${r.statement}`).join("\n")}` };
        }
      });
      api.registerCommand({
        name: "forget",
        description: "Retire a PLUR memory by ID",
        acceptsArgs: true,
        handler: (ctx) => {
          if (!ctx.args?.trim()) return { text: "Usage: /forget <engram-id>" };
          getEngine(path).plur.forget(ctx.args.trim());
          return { text: `Retired: ${ctx.args.trim()}` };
        }
      });
      api.registerCommand({
        name: "sync",
        description: "Sync PLUR memories across devices via git",
        acceptsArgs: true,
        handler: (ctx) => {
          const remote = ctx.args?.trim() || void 0;
          const result = getEngine(path).plur.sync(remote);
          return { text: `Sync: ${result.action}${result.message ? ` \u2014 ${result.message}` : ""}` };
        }
      });
      api.registerCommand({
        name: "sync-status",
        description: "Check PLUR sync status",
        acceptsArgs: false,
        handler: () => {
          const status = getEngine(path).plur.syncStatus();
          const parts = [`Sync status: ${status.initialized ? "initialized" : "not initialized"}`];
          if (status.remote) parts.push(`Remote: ${status.remote}`);
          if (status.dirty) parts.push("(uncommitted changes)");
          if (status.ahead) parts.push(`${status.ahead} ahead`);
          if (status.behind) parts.push(`${status.behind} behind`);
          return { text: parts.join("\n") };
        }
      });
      api.registerCommand({
        name: "packs",
        description: "Manage knowledge packs: list, install <path>, uninstall <name>",
        acceptsArgs: true,
        handler: (ctx) => {
          const args = (ctx.args?.trim() || "").split(/\s+/);
          const sub = args[0] || "list";
          const e = getEngine(path);
          if (sub === "list") {
            const packs = e.plur.listPacks();
            if (!packs.length) return { text: "No packs installed." };
            return { text: packs.map((p) => `${p.name} v${p.manifest?.version ?? "?"} (${p.engram_count} engrams)${p.integrity ? ` [${p.integrity.slice(0, 12)}]` : ""}`).join("\n") };
          }
          if (sub === "install" && args[1]) {
            const result = e.plur.installPack(args[1]);
            let text = `Installed "${result.name}": ${result.installed} engrams`;
            if (result.conflicts?.length) text += `
${result.conflicts.length} conflicts detected \u2014 use /recall to review`;
            return { text };
          }
          if ((sub === "uninstall" || sub === "remove") && args[1]) {
            const result = e.plur.uninstallPack(args[1]);
            return { text: `Uninstalled "${result.name}": ${result.engram_count} engrams removed` };
          }
          return { text: "Usage: /packs [list | install <path> | uninstall <name>]" };
        }
      });
    }
    if (typeof api.registerCli === "function") {
      api.registerCli((cliCtx) => {
        const cmd = cliCtx.program.command("plur").description("PLUR memory management").action(() => {
          const s = getEngine(path).plur.status();
          console.log(`PLUR Memory Status:`);
          console.log(`  Engrams: ${s.engram_count}`);
          console.log(`  Episodes: ${s.episode_count}`);
          console.log(`  Packs: ${s.pack_count}`);
          console.log(`  Storage: ${s.storage_root}`);
        });
        cmd.command("sync [remote]").description("Sync memories via git").action((remote) => {
          const result = getEngine(path).plur.sync(remote);
          console.log(`Sync: ${result.action}${result.message ? ` \u2014 ${result.message}` : ""}`);
        });
      }, { commands: ["plur"] });
    }
    api.registerService({
      id: "plur-claw",
      start: () => api.logger.info(`PLUR: started (path: ${path})`),
      stop: () => api.logger.info("PLUR: stopped")
    });
    api.logger.info(`PLUR registered: context engine + hooks + slash commands + CLI`);
    checkForUpdate("@plur-ai/claw", plugin.version, (r) => {
      if (r.updateAvailable) {
        api.logger.warn(`PLUR update available: ${r.current} \u2192 ${r.latest}. Run: npm update @plur-ai/claw`);
      }
    });
  }
};
var index_default = plugin;
export {
  PLUR_SYSTEM_SECTION,
  PlurContextEngine,
  index_default as default,
  ensureSystemPrompt
};
