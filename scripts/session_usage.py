"""Summarize token usage of local Codex/Claude sessions; reads counters only, never chat text or files outside the logs."""
import argparse
import json
from pathlib import Path

CODEX = Path.home() / '.codex' / 'sessions'
CLAUDE = Path.home() / '.claude' / 'projects'
TOOL_ITEMS = {'function_call', 'custom_tool_call', 'local_shell_call'}


def new_turn():
    return {'requests': 0, 'tool_calls': 0, 'input': 0, 'cached': 0, 'output': 0, 'context_start': None, 'context_end': 0}


def add_request(turn, context, cached, output):
    turn['requests'] += 1
    turn['input'] += context
    turn['cached'] += cached
    turn['output'] += output
    if turn['context_start'] is None:
        turn['context_start'] = context
    turn['context_end'] = context


def codex_session(path):
    cwd, model, turns, compactions = None, None, [], 0
    with path.open(encoding='utf-8', errors='replace') as stream:
        lines = list(stream)
    for line in lines:
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind, payload = item.get('type'), item.get('payload') or {}
        sub = payload.get('type')
        if kind == 'session_meta':
            cwd = payload.get('cwd')
        elif kind == 'turn_context':
            cwd, model = cwd or payload.get('cwd'), payload.get('model') or model
        elif kind == 'compacted' or sub == 'context_compacted':
            compactions += 1
        elif kind == 'response_item' and sub == 'message' and payload.get('role') == 'user':
            text = ' '.join(c.get('text', '') for c in payload.get('content') or [] if isinstance(c, dict)).lstrip()
            if text and not text.startswith('<') and not text.lower().startswith('# agents'):
                turns.append(new_turn())
        elif kind == 'response_item' and sub in TOOL_ITEMS and turns:
            turns[-1]['tool_calls'] += 1
        elif kind == 'event_msg' and sub == 'token_count' and (payload.get('info') or {}).get('last_token_usage'):
            if not turns:
                turns.append(new_turn())
            last = payload['info']['last_token_usage']
            add_request(turns[-1], last.get('input_tokens', 0), last.get('cached_input_tokens', 0), last.get('output_tokens', 0))
    return {'tool': 'codex', 'file': path.name, 'cwd': cwd, 'model': model, 'compactions': compactions, 'turns': turns}


def claude_session(path):
    cwd, model, turns, compactions, seen = None, None, [], 0, set()
    with path.open(encoding='utf-8', errors='replace') as stream:
        lines = list(stream)
    for line in lines:
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind, message = item.get('type'), item.get('message') or {}
        cwd = cwd or item.get('cwd')
        if kind == 'system' and item.get('subtype') == 'compact_boundary':
            compactions += 1
        elif kind == 'user' and not item.get('isSidechain') and isinstance(message.get('content'), str):
            turns.append(new_turn())
        elif kind == 'assistant' and not item.get('isSidechain') and message.get('usage'):
            if not turns:
                turns.append(new_turn())
            model = message.get('model') or model
            turns[-1]['tool_calls'] += sum(1 for c in message.get('content') or [] if isinstance(c, dict) and c.get('type') == 'tool_use')
            key = item.get('requestId') or item.get('uuid')
            if key in seen:
                continue
            seen.add(key)
            usage = message['usage']
            cached = usage.get('cache_read_input_tokens', 0)
            context = usage.get('input_tokens', 0) + cached + usage.get('cache_creation_input_tokens', 0)
            add_request(turns[-1], context, cached, usage.get('output_tokens', 0))
    return {'tool': 'claude', 'file': path.name, 'cwd': cwd, 'model': model, 'compactions': compactions, 'turns': turns}


def summarize(session, with_turns=False):
    turns = [t for t in session['turns'] if t['requests']]
    total = {key: sum(t[key] for t in turns) for key in ('requests', 'tool_calls', 'input', 'cached', 'output')}
    result = {key: session[key] for key in ('tool', 'file', 'model', 'compactions')}
    result.update(total, turns=len(turns), peak_context=max((t['context_end'] for t in turns), default=0))
    if with_turns:
        result['per_turn'] = turns
    return result


def collect(codex_root=CODEX, claude_root=CLAUDE, match='nature studio', since=''):
    sessions = [codex_session(p) for p in sorted(Path(codex_root).rglob('rollout-*.jsonl'))] if Path(codex_root).is_dir() else []
    sessions += [claude_session(p) for p in sorted(Path(claude_root).glob('*/*.jsonl'))] if Path(claude_root).is_dir() else []
    matched = [s for s in sessions if s['cwd'] and match.lower() in s['cwd'].lower().replace('\\', '/')]
    return [s for s in matched if not since or s['file'].replace('rollout-', '')[:10] >= since or s['tool'] == 'claude']


if __name__ == '__main__':
    import ns_console
    ns_console.utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--match', default='nature studio', help='substring of the session working directory')
    parser.add_argument('--since', default='', help='YYYY-MM-DD, Codex sessions only')
    parser.add_argument('--file', default='', help='only sessions whose log file name contains this text')
    parser.add_argument('--turns', action='store_true', help='include per-turn breakdown')
    parser.add_argument('--codex-root', type=Path, default=CODEX)
    parser.add_argument('--claude-root', type=Path, default=CLAUDE)
    args = parser.parse_args()
    rows = [summarize(s, args.turns) for s in collect(args.codex_root, args.claude_root, args.match, args.since) if args.file in s['file']]
    print(json.dumps([r for r in rows if r['requests']], ensure_ascii=False))
