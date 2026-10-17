"""Deterministic large fixture: expected IDs declared before actual retrieval, no model calls."""
import json
from pathlib import Path
import sys
import tempfile
import time

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import memory_retrieval as mem
import validate_memory


def run():
    expected={'L-line','L-motion','L-shared'}
    with tempfile.TemporaryDirectory() as temp:
        root=Path(temp)
        def write(rel,text):
            p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');return p
        write('03-Projects/test/PROJECT.md','ID: test\n')
        write('00-Standards/memory-policy.md','Fixture policy, no activation inference')
        write('fixture-evidence.md','Synthetic objective evidence and explicit fixture-only activation authority')
        write('05-Memory/INDEX.md','[test](projects/test/INDEX.md) [shared](shared/INDEX.md)')
        for prefix in ['05-Memory/projects/test','05-Memory/shared']:
            write(prefix+'/INDEX.md','# Fixture namespace\n')
            for state in ['active','candidates','retired']:
                (root/prefix/state).mkdir(parents=True,exist_ok=True)
        write('00-Standards/memory-taxonomy.json',(mem.ROOT/'00-Standards/memory-taxonomy.json').read_text(encoding='utf-8'))
        paths=[]
        for i in range(1000):
            name,task,topic,scope=(('line','video-review','tackle-continuity','project') if i==0 else
                ('motion','video-review','animal-motion','project') if i==1 else
                ('shared','video-review','tackle-continuity','shared') if i==2 else
                (f'caption-{i}','caption','caption','project'))
            d=dict(id='L-'+name,version='1.0',status='active',scope=scope,
                   project_id=None if scope=='shared' else 'test',action='Check '+topic,
                   kind='procedural',origin_project_ids=['test'],production_ids=[],
                   transfer_rationale='Synthetic shared fixture' if scope=='shared' else None,
                   publication=dict(visibility='private',reviewed=False),evidence=['fixture-evidence.md'],
                   validation=dict(result='not_checked',method='not_checked',records=[],
                                   regression_checked=False,unresolved_conflicts=[],changes_policy=False),
                   activation=dict(method='user',date='2026-10-17',authority='fixture-evidence.md'),
                   conditions=dict(tasks=[task],models=[],interfaces=[],formats=[]),
                   retrieval=dict(schema=1,summary='Inspect '+topic+' and exceptions in original.',
                                  topics=[topic],entities=[],interactions=[]))
            prefix='05-Memory/shared' if scope=='shared' else '05-Memory/projects/test'
            paths.append(write(prefix+'/active/L-'+name+'.md','---\n'+json.dumps(d)+'\n---\n'+'Detailed condition and evidence. '*160))
            with (root/prefix/'INDEX.md').open('a',encoding='utf-8') as f:
                f.write('[lesson](active/L-'+name+'.md)\n')
        validity=validate_memory.validate(root)
        assert validity['valid'],validity
        original=sum(p.stat().st_size for p in paths)
        begin=time.perf_counter();q=mem.query(root,'test',tasks=['video-review'],topics=['tackle-continuity','animal-motion']);elapsed=time.perf_counter()-begin
        actual={r['id'] for r in q['active']}
        assert actual==expected,(expected,actual)
        chosen=mem.load_lessons(root,'test',q,sorted(expected))
        descriptors=len(json.dumps(q,ensure_ascii=False).encode('utf-8'))
        bodies=sum(len(r['text'].encode('utf-8')) for r in chosen)
        assert q['remaining']==0 and q['excluded_conditions']==997 and not q['errors']
        assert descriptors+bodies < original/10
        broad=mem.query(root,'test',broad=True,page_size=100)
        count=0
        while True:
            count+=len(broad['active'])
            if not broad['next_cursor']:break
            broad=mem.query(root,'test',broad=True,page_size=100,cursor=broad['next_cursor'])
        assert count==1000 and broad['discovery_complete']
        return dict(fixture_lessons=1000,fixture_metadata_valid=validity['valid'],expected_ids=sorted(expected),actual_ids=sorted(actual),
                    expected_recall=1.0,excluded_explicit_task=997,baseline_body_bytes=original,
                    descriptor_bytes=descriptors,selected_body_bytes=bodies,total_loaded_bytes=descriptors+bodies,
                    reduction_ratio=1-(descriptors+bodies)/original,query_seconds=elapsed,
                    broad_paginated_count=count,token_measurement='not measured; bytes only',
                    scope='synthetic metadata retrieval fixture, not semantic/model quality or real-workload token guarantee')


if __name__=='__main__':print(json.dumps(run(),indent=2))
