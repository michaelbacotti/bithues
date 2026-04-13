import { Plur } from '@plur-ai/core';

interface AgentMessage {
    role: string;
    content: string;
    [key: string]: unknown;
}
interface ContextEngineInfo {
    id: string;
    name: string;
    version?: string;
    ownsCompaction?: boolean;
}
interface BootstrapResult {
    bootstrapped: boolean;
    importedMessages?: number;
    reason?: string;
}
interface IngestResult {
    ingested: boolean;
}
interface AssembleResult {
    messages: AgentMessage[];
    estimatedTokens: number;
    systemPromptAddition?: string;
    injected_ids?: string[];
}
interface CompactResult {
    ok: boolean;
    compacted: boolean;
    reason?: string;
    result?: {
        summary?: string;
        firstKeptEntryId?: string;
        tokensBefore: number;
        tokensAfter?: number;
    };
}
interface SubagentSpawnPreparation {
    rollback: () => void | Promise<void>;
}
type SubagentEndReason = 'deleted' | 'completed' | 'swept' | 'released';
interface ContextEngine {
    readonly info: ContextEngineInfo;
    bootstrap?(params: {
        sessionId: string;
        sessionKey?: string;
        sessionFile: string;
    }): Promise<BootstrapResult>;
    ingest(params: {
        sessionId: string;
        sessionKey?: string;
        message: AgentMessage;
        isHeartbeat?: boolean;
    }): Promise<IngestResult>;
    ingestBatch?(params: {
        sessionId: string;
        sessionKey?: string;
        messages: AgentMessage[];
        isHeartbeat?: boolean;
    }): Promise<{
        ingested: boolean;
    }>;
    afterTurn?(params: {
        sessionId: string;
        sessionKey?: string;
        sessionFile: string;
        messages: AgentMessage[];
        prePromptMessageCount: number;
        autoCompactionSummary?: string;
        isHeartbeat?: boolean;
        tokenBudget?: number;
    }): Promise<void>;
    assemble(params: {
        sessionId: string;
        sessionKey?: string;
        messages: AgentMessage[];
        tokenBudget?: number;
    }): Promise<AssembleResult>;
    compact(params: {
        sessionId: string;
        sessionKey?: string;
        sessionFile: string;
        tokenBudget?: number;
        force?: boolean;
        currentTokenCount?: number;
    }): Promise<CompactResult>;
    prepareSubagentSpawn?(params: {
        parentSessionKey: string;
        childSessionKey: string;
        ttlMs?: number;
    }): Promise<SubagentSpawnPreparation | undefined>;
    onSubagentEnded?(params: {
        childSessionKey: string;
        reason: SubagentEndReason;
    }): Promise<void>;
    dispose?(): Promise<void>;
}

interface PlurContextEngineOptions {
    path?: string;
    auto_learn?: boolean;
    auto_capture?: boolean;
    injection_budget?: number;
}
declare class PlurContextEngine implements ContextEngine {
    readonly info: ContextEngineInfo;
    readonly plur: Plur;
    private options;
    private sessionScopes;
    private sessionMessages;
    private sessionLearned;
    constructor(options?: PlurContextEngineOptions);
    /** Bootstrap: inject relevant engrams for the session */
    bootstrap(params: {
        sessionId: string;
        sessionKey?: string;
        sessionFile: string;
    }): Promise<BootstrapResult>;
    /** Ingest: process each message for real-time corrections */
    ingest(params: {
        sessionId: string;
        sessionKey?: string;
        message: AgentMessage;
        isHeartbeat?: boolean;
    }): Promise<IngestResult>;
    /** Assemble: build context with injected engrams */
    assemble(params: {
        sessionId: string;
        sessionKey?: string;
        messages: AgentMessage[];
        tokenBudget?: number;
    }): Promise<AssembleResult>;
    /** Compact: extract learnings from context being compacted */
    compact(params: {
        sessionId: string;
        sessionKey?: string;
        sessionFile: string;
        tokenBudget?: number;
        force?: boolean;
        currentTokenCount?: number;
    }): Promise<CompactResult>;
    /** AfterTurn: extract learnings from LLM self-report + regex fallback, capture episode */
    afterTurn(params: {
        sessionId: string;
        sessionKey?: string;
        sessionFile: string;
        messages: AgentMessage[];
        prePromptMessageCount: number;
        autoCompactionSummary?: string;
        isHeartbeat?: boolean;
        tokenBudget?: number;
    }): Promise<void>;
    /** PrepareSubagentSpawn: inject scoped engrams for child agent */
    prepareSubagentSpawn(params: {
        parentSessionKey: string;
        childSessionKey: string;
        ttlMs?: number;
    }): Promise<SubagentSpawnPreparation | undefined>;
    /** OnSubagentEnded: absorb child learnings */
    onSubagentEnded(params: {
        childSessionKey: string;
        reason: SubagentEndReason;
    }): Promise<void>;
    /** Dispose: clean up */
    dispose(): Promise<void>;
    getSessionScope(sessionKey: string): string | undefined;
    /** Learn a statement only if it hasn't been learned in this session already (prevents triple-learning). */
    private _learnIfNew;
}

/**
 * The PLUR memory section appended to SYSTEM.md during plugin installation.
 * Teaches the agent how to use PLUR tools and the learning format.
 *
 * Kept in sync with CLI init CLAUDE.md section and MCP init CLAUDE.md section.
 * When updating, bump the version marker at the bottom.
 */
declare const PLUR_SYSTEM_SECTION = "\n\n## PLUR Memory System\n\nYou have persistent memory powered by PLUR. Corrections, preferences, and conventions persist across sessions as engrams.\n\n### Session Workflow\n\n1. **Start**: Call `plur.recall` with the task description \u2014 check if you already know something relevant\n2. **Learn**: When corrected or discovering something new, call `plur.learn` immediately\n3. **Recall**: Before answering factual questions, call `plur.recall` \u2014 the answer may be in memory\n4. **Feedback**: Rate memories with `plur.feedback` (positive/negative) \u2014 trains relevance\n5. **End**: Record a session summary with `plur.capture`\n\nDo not ask permission to use these tools \u2014 they are your memory system.\n\n### Your Memory Tools\n\nUse these tools proactively, not just when asked:\n\n- **plur.recall** \u2014 Search memories BEFORE answering questions. Do not start from scratch.\n- **plur.learn** \u2014 Store knowledge worth remembering: corrections, preferences, decisions, project facts. Phrase as factual statements.\n- **plur.ingest** \u2014 Extract durable knowledge from content (books, articles, documents). Creates multiple memories from key insights.\n- **plur.forget** \u2014 Retire memories that are no longer accurate.\n- **plur.feedback** \u2014 Rate a memory as positive, negative, or neutral. Improves future recall.\n- **plur.capture** \u2014 Record a session event in the episodic timeline.\n- **plur.timeline** \u2014 Query past episodes by time, agent, or channel.\n- **plur.status** \u2014 Check memory health (engram count, storage).\n\n### Knowledge Packs\n\nKnowledge Packs are curated collections of engrams for specific domains \u2014 shareable with teams.\n\n- **plur.packs.list** \u2014 List installed packs with integrity hashes\n- **plur.packs.install** \u2014 Install a pack (reports conflicts with existing memories)\n- **plur.packs.uninstall** \u2014 Remove a pack and its engrams\n- **plur.packs.export** \u2014 Export your memories as a thematic pack (with privacy scan)\n\nWhen a user asks about sharing knowledge, team memory, or domain expertise \u2014 suggest knowledge packs.\n\nExport packs thematically: filter by domain, tags, or type. Privacy scan automatically blocks secrets and private memories.\n\n### When to Check Memory\n\nBefore reaching for web search, file reads, or guessing:\n1. Is the answer in memory? \u2192 `plur.recall`\n2. Is the answer in the filesystem? \u2192 Read/Grep/Glob\n3. Is the answer derivable from loaded context? \u2192 Just answer\n4. Only if 1-3 fail \u2192 Use external tools\n\n| Domain | When to recall |\n|--------|----------------|\n| Decisions | Past design choices, architecture rationale |\n| Corrections | API quirks, bugs, wrong assumptions |\n| Preferences | Formatting, tone, workflow, tool choices |\n| Conventions | Tag formats, file routing, naming rules |\n\n### When Corrected\n\nWhen the user corrects you (\"no, use X not Y\", \"that's wrong\"):\n1. Call `plur.learn` immediately \u2014 before continuing the task\n2. Call `plur.feedback` with negative signal on the wrong memory if one was used\n3. Then continue with the corrected approach\n\n### Verification\n\nWhen recalling facts that will drive actions:\n1. State the recalled fact explicitly before acting on it\n2. If no memory matches, say so and verify from the filesystem\n3. Never interpolate between two memories to produce a \"probably correct\" composite\n\n### Signaling New Learnings\n\nWhen you learn something durable from a conversation, end your response with:\n\n---\nI learned:\n- [concise factual statement]\n- [another if applicable]\n\nGuidelines:\n- Only genuine learnings, not conversation summaries\n- Skip this section if nothing new was learned\n- Phrase as facts: \"The API requires auth header\" not \"the user said the API needs auth\"\n- Include corrections to your own mistakes\n\n### Principles\n\n- **Memory over repetition** \u2014 learn once, recall always. Never ask the user to repeat themselves.\n- **Do not start from scratch** \u2014 check your memories before answering.\n- **Augment, do not replace** \u2014 you assist, the human decides.\n\n<!-- plur-instructions-v3 -->\n";
/**
 * Append or update PLUR memory instructions in SYSTEM.md.
 * - Creates the file if it doesn't exist.
 * - Appends if no PLUR section present.
 * - Replaces if PLUR section exists but is outdated (version mismatch).
 * - Skips if current version already present.
 */
declare function ensureSystemPrompt(workspacePath: string): {
    appended: boolean;
    updated: boolean;
    path: string;
};

/**
 * PLUR OpenClaw Plugin — default export.
 *
 * When installed via `openclaw plugins install @plur-ai/claw`, OpenClaw
 * loads this as the plugin entry point. Registers:
 * - ContextEngine (memory injection, episode capture, learning extraction)
 * - Event hooks (before_agent_start for recall, agent_end for capture)
 * - SYSTEM.md auto-setup with memory instructions
 * - Service lifecycle
 *
 * Tools and slash commands are registered separately via the .mjs plugin
 * wrapper (which imports TypeBox from OpenClaw's runtime). This default
 * export provides the core memory functionality that works without TypeBox.
 */
declare const plugin: {
    id: string;
    name: string;
    description: string;
    version: string;
    kind: "memory";
    register(api: any): void;
};

export { type AgentMessage, type AssembleResult, type BootstrapResult, type CompactResult, type ContextEngine, type IngestResult, PLUR_SYSTEM_SECTION, PlurContextEngine, type PlurContextEngineOptions, plugin as default, ensureSystemPrompt };
