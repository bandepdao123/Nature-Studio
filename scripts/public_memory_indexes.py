"""Rebuild Markdown indexes from an explicitly selected public export, never local indexes."""
from collections import Counter
import json
from pathlib import PurePosixPath


def rebuild(files, read):
    files = set(files)
    namespaces = {'05-Memory/shared': []}
    for path in files:
        if path.startswith('03-Projects/') and path.endswith('/PROJECT.md'):
            namespaces['05-Memory/projects/' + PurePosixPath(path).parent.name] = []
    for path in sorted(files):
        if not path.startswith('05-Memory/') or PurePosixPath(path).name in ('README.md', 'INDEX.md') or not path.endswith('.md'):
            continue
        data = json.loads(read(path).decode('utf-8-sig').split('---', 2)[1])
        public = data.get('publication', {})
        if public.get('visibility') != 'public' or public.get('reviewed') is not True:
            raise ValueError('Refuse to index a private/unreviewed lesson: ' + path)
        namespace = str(PurePosixPath(path).parent.parent)
        if namespace not in namespaces:
            raise ValueError('Unknown public namespace: ' + namespace)
        namespaces[namespace].append((path, data))
    output = {}
    all_counts = Counter()
    for namespace, lessons in sorted(namespaces.items()):
        counts = Counter(d['status'] for _, d in lessons); all_counts.update(counts)
        relative = '../' if namespace == '05-Memory/shared' else '../../'
        text = '# Bộ nhớ công khai\n\nChỉ mục dựng từ tập bài public/reviewed thực được xuất. '
        text += 'Active: {} | Candidates: {} | Retired: {}\n\n'.format(counts['active'], counts['candidate'], counts['retired'])
        text += f'[Truy xuất chọn lọc]({relative}../00-Standards/memory-retrieval.md); đọc gốc trước áp dụng, candidate không là luật.\n\n'
        for path, d in lessons:
            text += '- [{} v{} — {}]({}/{})\n'.format(d['id'], d['version'], d['status'], PurePosixPath(path).parent.name, PurePosixPath(path).name)
        output[namespace+'/INDEX.md'] = text.encode('utf-8')
    text = '# Bộ nhớ Nature Studio — tập công khai\n\nActive: {} | Candidates: {} | Retired: {}\n\n'.format(all_counts['active'], all_counts['candidate'], all_counts['retired'])
    for namespace in sorted(namespaces):
        rel = namespace.removeprefix('05-Memory/')
        text += f'- [{rel}]({rel}/INDEX.md)\n'
    text += '\n[Truy xuất bài học](../00-Standards/memory-retrieval.md). Cache/query runtime không phân phối.\n'
    output['05-Memory/INDEX.md'] = text.encode('utf-8')
    return output
